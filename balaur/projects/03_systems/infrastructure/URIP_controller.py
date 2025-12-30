#!/usr/bin/env python3
"""UBOS Rhythmic Integrity Protocol (URIP) controller."""
from __future__ import annotations

import argparse
import configparser
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULTS = {
    "orchestrion": {
        "spec_path": "/srv/janus/balaur/projects/03_systems/infrastructure/orchestrion_spec_v1.md",
    },
    "urip": {
        "base_interval": "6",
        "min_interval": "2",
        "max_interval": "30",
        "cpu_soft_limit": "0.65",
        "cpu_hard_limit": "0.85",
        "mem_soft_limit": "0.70",
        "mem_hard_limit": "0.90",
        "token_soft_limit": "4000",
        "token_hard_limit": "7000",
        "query_soft_limit": "4",
        "query_hard_limit": "8",
        "beat_bus_dir": "/srv/janus/balaur/signal/clock",
        "oracle_sync_dir": "/srv/janus/balaur/oracle_trinity/sync",
        "semantic_probe_file": "/srv/janus/balaur/signal/clock/semantic_depth.json",
        "task_meter_file": "/srv/janus/balaur/signal/clock/task_meter.json",
        "log_level": "INFO",
    },
}


@dataclass
class Telemetry:
    timestamp: datetime
    cpu_ratio: float
    mem_ratio: float
    query_frequency: float
    semantic_depth: int
    task_intensity: float


class URIPController:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()
        self.base_interval = self.config.getfloat("urip", "base_interval", fallback=6.0)
        self.min_interval = self.config.getfloat("urip", "min_interval", fallback=2.0)
        self.max_interval = self.config.getfloat("urip", "max_interval", fallback=30.0)
        self.cpu_soft = self.config.getfloat("urip", "cpu_soft_limit", fallback=0.65)
        self.cpu_hard = self.config.getfloat("urip", "cpu_hard_limit", fallback=0.85)
        self.mem_soft = self.config.getfloat("urip", "mem_soft_limit", fallback=0.70)
        self.mem_hard = self.config.getfloat("urip", "mem_hard_limit", fallback=0.90)
        self.token_soft = self.config.getfloat("urip", "token_soft_limit", fallback=4000.0)
        self.token_hard = self.config.getfloat("urip", "token_hard_limit", fallback=7000.0)
        self.query_soft = self.config.getfloat("urip", "query_soft_limit", fallback=4.0)
        self.query_hard = self.config.getfloat("urip", "query_hard_limit", fallback=8.0)
        self.semantic_probe = Path(self.config.get("urip", "semantic_probe_file", fallback=""))
        self.task_meter_file = Path(self.config.get("urip", "task_meter_file", fallback=""))

        beat_dir = Path(self.config.get("urip", "beat_bus_dir", fallback=DEFAULTS["urip"]["beat_bus_dir"]))
        beat_dir.mkdir(parents=True, exist_ok=True)
        self.beat_dir = beat_dir

        oracle_dir = Path(self.config.get("urip", "oracle_sync_dir", fallback=DEFAULTS["urip"]["oracle_sync_dir"]))
        oracle_dir.mkdir(parents=True, exist_ok=True)
        self.oracle_sync_dir = oracle_dir

        self.spec_path = Path(self.config.get("orchestrion", "spec_path", fallback=DEFAULTS["orchestrion"]["spec_path"])).expanduser()
        self.logger = logging.getLogger("URIP")
        self.logger.setLevel(self.config.get("urip", "log_level", fallback="INFO"))
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(handler)

        self.next_release_ts = time.time()

    def _load_config(self) -> configparser.ConfigParser:
        parser = configparser.ConfigParser()
        parser.read_dict(DEFAULTS)
        if not self.config_path.exists():
            return parser
        parser.read(self.config_path)
        return parser

    def run_cycle(self) -> float:
        telemetry = self._collect_telemetry()
        harmonic = self._load_harmonic_seed()
        governor_state = self._apply_governor(telemetry, harmonic)
        heartbeat = self._build_heartbeat(telemetry, governor_state, harmonic)
        self._publish_heartbeat(heartbeat, governor_state)
        return governor_state["interval"]

    def _collect_telemetry(self) -> Telemetry:
        timestamp = datetime.now(timezone.utc)
        cpu_ratio = self._cpu_ratio()
        mem_ratio = self._mem_ratio()
        query_frequency = self._query_frequency()
        semantic_depth = self._semantic_depth(query_frequency)
        task_intensity = self._task_intensity()
        return Telemetry(timestamp, cpu_ratio, mem_ratio, query_frequency, semantic_depth, task_intensity)

    def _cpu_ratio(self) -> float:
        try:
            load_avg = os.getloadavg()[0]
            cores = max(os.cpu_count() or 1, 1)
            return min(load_avg / cores, 2.0)
        except (AttributeError, OSError):
            return 0.0

    def _mem_ratio(self) -> float:
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as fh:
                info = fh.read()
            total_match = re.search(r"MemTotal:\s+(\d+)", info)
            avail_match = re.search(r"MemAvailable:\s+(\d+)", info)
            if not total_match:
                return 0.0
            total = float(total_match.group(1))
            available = float(avail_match.group(1)) if avail_match else total
            used = max(total - available, 0.0)
            return min(used / total, 1.5)
        except OSError:
            return 0.0

    def _query_frequency(self, lookback: int = 60) -> float:
        now = time.time()
        samples = []
        for path in self.oracle_sync_dir.glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                ts = data.get("timestamp")
                if not ts:
                    continue
                beat_ts = self._parse_iso_epoch(ts)
                if beat_ts and now - beat_ts <= lookback:
                    samples.append(beat_ts)
            except (json.JSONDecodeError, OSError):
                continue
        if len(samples) < 2:
            return float(len(samples)) / float(lookback or 1)
        samples.sort()
        diffs = [t2 - t1 for t1, t2 in zip(samples, samples[1:]) if t2 >= t1]
        if not diffs:
            return float(len(samples)) / float(lookback or 1)
        avg_gap = sum(diffs) / len(diffs)
        if avg_gap == 0:
            return self.query_hard
        return min(lookback / avg_gap, self.query_hard * 2)

    def _semantic_depth(self, query_frequency: float) -> int:
        if self.semantic_probe.is_file():
            try:
                data = json.loads(self.semantic_probe.read_text(encoding="utf-8"))
                return int(data.get("semantic_depth", 0))
            except (json.JSONDecodeError, OSError, ValueError):
                pass
        estimated = int(query_frequency * 1000)
        return max(estimated, 0)

    def _task_intensity(self) -> float:
        if self.task_meter_file.is_file():
            try:
                data = json.loads(self.task_meter_file.read_text(encoding="utf-8"))
                pending = float(data.get("pending_jobs", 0))
                avg_weight = float(data.get("avg_weight", 1.0))
                return pending * avg_weight
            except (json.JSONDecodeError, OSError, ValueError):
                return 0.0
        return 0.0

    def _load_harmonic_seed(self) -> Dict[str, Any]:
        seed = {
            "tempo_override": None,
            "priority_bands": [],
        }
        if not self.spec_path.is_file():
            return seed
        try:
            text = self.spec_path.read_text(encoding="utf-8")
        except OSError:
            return seed
        tempo_match = re.search(r"Tempo\s*[:=]\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if tempo_match:
            seed["tempo_override"] = float(tempo_match.group(1))
        band_matches = re.findall(r"Priority\s*(?:Band|Level)?\s*(\w+)\s*[:=]\s*([^\n]+)", text, re.IGNORECASE)
        for level, desc in band_matches:
            seed["priority_bands"].append({"band": level, "description": desc.strip()})
        return seed

    def _apply_governor(self, telemetry: Telemetry, harmonic: Dict[str, Any]) -> Dict[str, Any]:
        interval = harmonic.get("tempo_override") or self.base_interval
        amplitude = self._resonance_index(telemetry)
        scaled_interval = self._clamp(interval * (1 + amplitude), self.min_interval, self.max_interval)
        throttle = self._clamp(1.0 - amplitude, 0.1, 1.0)
        mode = "nominal"
        if amplitude >= 0.7:
            mode = "dampening"
        if amplitude >= 1.0:
            mode = "relief"
        next_release = datetime.now(timezone.utc).timestamp() + scaled_interval
        self.next_release_ts = next_release
        return {
            "interval": scaled_interval,
            "throttle": throttle,
            "mode": mode,
            "amplitude": amplitude,
            "next_release": next_release,
        }

    def _resonance_index(self, telemetry: Telemetry) -> float:
        cpu_factor = self._scaled_ratio(telemetry.cpu_ratio, self.cpu_soft, self.cpu_hard)
        mem_factor = self._scaled_ratio(telemetry.mem_ratio, self.mem_soft, self.mem_hard)
        semantic_factor = self._scaled_ratio(float(telemetry.semantic_depth), self.token_soft, self.token_hard)
        query_factor = self._scaled_ratio(telemetry.query_frequency, self.query_soft, self.query_hard)
        task_factor = self._scaled_ratio(telemetry.task_intensity, max(self.query_soft, 1.0), max(self.query_hard, 1.0))
        return max(cpu_factor, mem_factor, semantic_factor, query_factor, task_factor)

    def _scaled_ratio(self, value: float, soft: float, hard: float) -> float:
        if hard <= soft:
            hard = soft + 0.0001
        if value <= soft:
            return max(value / hard, 0.0)
        over = (value - soft) / (hard - soft)
        return min(over + soft / hard, 2.0)

    def _build_heartbeat(
        self,
        telemetry: Telemetry,
        governor_state: Dict[str, Any],
        harmonic: Dict[str, Any],
    ) -> Dict[str, Any]:
        timestamp = telemetry.timestamp.isoformat()
        next_release_iso = datetime.fromtimestamp(governor_state["next_release"], tz=timezone.utc).isoformat()
        return {
            "timestamp": timestamp,
            "interval": governor_state["interval"],
            "mode": governor_state["mode"],
            "throttle": governor_state["throttle"],
            "next_release": next_release_iso,
            "resonance": {
                "amplitude": governor_state["amplitude"],
                "cpu_ratio": telemetry.cpu_ratio,
                "mem_ratio": telemetry.mem_ratio,
                "query_frequency": telemetry.query_frequency,
                "semantic_depth": telemetry.semantic_depth,
                "task_intensity": telemetry.task_intensity,
            },
            "harmonic_seed": harmonic,
        }

    def _publish_heartbeat(self, heartbeat: Dict[str, Any], governor_state: Dict[str, Any]) -> None:
        state_path = self.beat_dir / "rhythm_state.json"
        history_path = self.beat_dir / "rhythm_history.log"
        release_path = self.beat_dir / "next_release.token"
        alert_path = self.beat_dir / "urip.alert"

        self._atomic_write(state_path, json.dumps(heartbeat, indent=2))

        history_line = (
            f"{heartbeat['timestamp']} | interval={heartbeat['interval']:.2f}s "
            f"amp={heartbeat['resonance']['amplitude']:.2f} mode={heartbeat['mode']}\n"
        )
        with open(history_path, "a", encoding="utf-8") as log_file:
            log_file.write(history_line)

        self._atomic_write(release_path, heartbeat["next_release"])

        if governor_state["mode"] == "relief":
            alert_message = (
                f"Hard limit reached at {heartbeat['timestamp']} — cadence stretched "
                f"to {heartbeat['interval']:.2f}s with throttle {heartbeat['throttle']:.2f}."
            )
            self._atomic_write(alert_path, alert_message)
        else:
            if alert_path.exists():
                alert_path.unlink()

        self.logger.info(
            "beat interval=%.2fs throttle=%.2f amp=%.2f mode=%s",
            heartbeat["interval"],
            heartbeat["throttle"],
            heartbeat["resonance"]["amplitude"],
            heartbeat["mode"],
        )

    def _atomic_write(self, path: Path, content: str) -> None:
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        with open(tmp_path, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_path, path)

    @staticmethod
    def _parse_iso_epoch(value: str) -> Optional[float]:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return None

    @staticmethod
    def _clamp(value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(value, max_value))


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UBOS Rhythmic Integrity Protocol controller")
    parser.add_argument("--config", default="urip_daemon.conf", help="Path to URIP config file")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    controller = URIPController(Path(args.config).expanduser())
    try:
        while True:
            interval = controller.run_cycle()
            if args.once:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        controller.logger.info("URIP controller interrupted; exiting cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
