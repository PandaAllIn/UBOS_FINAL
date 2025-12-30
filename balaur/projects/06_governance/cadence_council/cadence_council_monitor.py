#!/usr/bin/env python3
"""Cadence Council Monitor — Article V implementation."""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

COUNCIL_DIR = Path("/srv/janus/balaur/projects/06_governance/cadence_council")
ARTIFACT_DIR = Path("/srv/janus/balaur/projects/05_software/pattern_engine/artifacts")
URIP_CLOCK_DIR = Path("/srv/janus/balaur/signal/clock")
DASHBOARD_DIR = Path("/srv/janus/balaur/projects/04_operations/harmony_dashboard")
RIP_HEALTH_PATH = Path("/srv/janus/balaur/logs/rip/health.json")
LOG_PATH = Path("/srv/janus/balaur/logs/governance/council_activity.log")


@dataclass
class ResonanceSample:
    timestamp: str
    harmony: float
    entropy: float
    cohesion: float
    interval: float
    classification: str
    delta_from_mean: float
    trend: Optional[float]
    notes: List[str]
    stability_band: Dict[str, float]


class CadenceCouncilMonitor:
    def __init__(self) -> None:
        COUNCIL_DIR.mkdir(parents=True, exist_ok=True)
        DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.minutes_path = COUNCIL_DIR / "council_minutes.json"
        self.dashboard_path = DASHBOARD_DIR / "council_resonance_view.json"
        self.rhythm_state_path = URIP_CLOCK_DIR / "rhythm_state.json"
        self.rhythm_history_path = URIP_CLOCK_DIR / "rhythm_history.log"
        self.release_token_path = URIP_CLOCK_DIR / "next_release.token"
        self.logger = logging.getLogger("CadenceCouncil")

    # ------------------------------------------------------------------
    def run(self, watch: bool, force_emit: bool) -> None:
        while True:
            self._respect_release_window()
            sample = self._collect_sample()
            if sample is None:
                self.logger.warning("Unable to collect Cadence Council sample; retrying later")
            else:
                self._persist_minutes(sample)
                self._update_dashboard(sample)
                self._append_log(sample)
                if force_emit:
                    self.logger.info("Forced emission complete: harmony=%.3f", sample.harmony)
            if not watch:
                break
            sleep_interval = (sample.interval if sample else 6.0)
            time.sleep(max(sleep_interval, 4.0))

    # ------------------------------------------------------------------
    def _respect_release_window(self) -> None:
        if not self.release_token_path.is_file():
            return
        try:
            next_ts = self.release_token_path.read_text(encoding="utf-8").strip()
            if not next_ts:
                return
            release_dt = datetime.fromisoformat(next_ts.replace("Z", "+00:00"))
        except (OSError, ValueError):
            return
        now = datetime.now(timezone.utc)
        if release_dt > now:
            wait_s = (release_dt - now).total_seconds()
            self.logger.debug("Waiting %.2fs for URIP escarpment window", wait_s)
            time.sleep(wait_s)

    def _collect_sample(self) -> Optional[ResonanceSample]:
        urip_state = self._read_json(self.rhythm_state_path)
        artifact = self._load_latest_artifact()
        if not urip_state and not artifact:
            return None

        entropy = self._extract_entropy(artifact)
        cohesion = self._extract_cohesion(artifact)
        interval = float(urip_state.get("interval") if urip_state else 6.0)
        if not math.isfinite(interval) or interval <= 0:
            interval = float(urip_state.get("interval", 6.0)) if urip_state else 6.0
            if interval <= 0:
                interval = 6.0

        mode = None
        if urip_state:
            mode = urip_state.get("mode") or urip_state.get("resonance", {}).get("mode")
            mode_factor = {
                "nominal": 1.0,
                "dampening": 0.9,
                "relief": 0.7,
            }.get(mode, 1.0)
            cohesion *= mode_factor
            entropy = max(entropy, 0.0)

        notes: List[str] = []
        rip_health = self._read_json(RIP_HEALTH_PATH)
        if rip_health:
            uptime = self._clamp(float(rip_health.get("uptime_score", 1.0)), 0.0, 1.0)
            cohesion *= uptime
            incident_level = int(rip_health.get("incident_level", 0))
            if incident_level >= 2:
                notes.append(f"RIP incident level {incident_level}")

        if entropy is None:
            entropy = self._entropy_from_history()
        if cohesion is None:
            cohesion = 0.5

        harmony = cohesion / (entropy + 1.0)
        harmony = self._clamp(harmony, 0.0, 1.5)

        existing_minutes = self._load_minutes()
        recent_values = [entry.get("harmony", 0.0) for entry in existing_minutes[-11:]]
        mean_base = (sum(recent_values) + harmony) / (len(recent_values) + 1 or 1)
        delta = harmony - mean_base
        classification = "within_band"
        if delta > 0.05:
            classification = "alert_high"
            notes.append("Harmony above stability band")
        elif delta < -0.05:
            classification = "alert_low"
            notes.append("Harmony below stability band")

        trend = None
        if existing_minutes:
            trend = harmony - existing_minutes[-1].get("harmony", harmony)

        stability_band = {
            "mean": round(mean_base, 4),
            "lower": round(mean_base - 0.05, 4),
            "upper": round(mean_base + 0.05, 4),
        }

        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        sample = ResonanceSample(
            timestamp=timestamp,
            harmony=round(harmony, 4),
            entropy=round(entropy, 4),
            cohesion=round(cohesion, 4),
            interval=interval,
            classification=classification,
            delta_from_mean=round(delta, 4),
            trend=(round(trend, 4) if trend is not None else None),
            notes=notes,
            stability_band=stability_band,
        )
        return sample

    def _persist_minutes(self, sample: ResonanceSample) -> None:
        minutes = self._load_minutes()
        entry = {
            "timestamp": sample.timestamp,
            "harmony": sample.harmony,
            "entropy": sample.entropy,
            "cohesion": sample.cohesion,
            "interval": sample.interval,
            "classification": sample.classification,
            "delta_from_mean": sample.delta_from_mean,
            "trend": sample.trend,
            "stability_band": sample.stability_band,
            "notes": sample.notes,
        }
        minutes.append(entry)
        minutes = minutes[-50:]
        self._atomic_write(self.minutes_path, json.dumps(minutes, indent=2))

    def _update_dashboard(self, sample: ResonanceSample) -> None:
        minutes = self._load_minutes()
        history = [
            {"timestamp": item.get("timestamp"), "harmony": item.get("harmony")}
            for item in minutes[-12:]
        ]
        payload = {
            "panel": "Council Resonance View",
            "last_updated": sample.timestamp,
            "last_harmony": sample.harmony,
            "classification": sample.classification,
            "stability_band": sample.stability_band,
            "trend": sample.trend,
            "history": history,
            "alerts": sample.notes,
        }
        self._atomic_write(self.dashboard_path, json.dumps(payload, indent=2))

    def _append_log(self, sample: ResonanceSample) -> None:
        line = (
            f"{sample.timestamp} Harmony={sample.harmony:.3f} classification={sample.classification} "
            f"delta={sample.delta_from_mean:+.3f}"
        )
        if sample.notes:
            line += " notes=" + "; ".join(sample.notes)
        with open(LOG_PATH, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    # ------------------------------------------------------------------
    def _load_minutes(self) -> List[Dict[str, Any]]:
        if not self.minutes_path.is_file():
            return []
        try:
            return json.loads(self.minutes_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def _extract_entropy(self, artifact: Optional[Dict[str, Any]]) -> Optional[float]:
        if artifact:
            entropy = artifact.get("signals", {}).get("entropy")
            if isinstance(entropy, (int, float)):
                return float(entropy)
        return None

    def _extract_cohesion(self, artifact: Optional[Dict[str, Any]]) -> float:
        if artifact:
            cohesion = artifact.get("signals", {}).get("cohesion")
            if isinstance(cohesion, (int, float)):
                return float(cohesion)
        return 0.5

    def _entropy_from_history(self, tail: int = 20) -> float:
        if not self.rhythm_history_path.is_file():
            return 0.5
        try:
            lines = self.rhythm_history_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return 0.5
        amplitudes: List[float] = []
        for line in lines[-tail:]:
            amp = self._extract_value(line, "amp=")
            if math.isnan(amp):
                continue
            amplitudes.append(amp)
        if not amplitudes:
            return 0.5
        min_amp = min(amplitudes)
        max_amp = max(amplitudes)
        if math.isclose(min_amp, max_amp):
            return 0.0
        bins = [0] * 8
        for amp in amplitudes:
            normalized = (amp - min_amp) / (max_amp - min_amp)
            idx = min(int(normalized * len(bins)), len(bins) - 1)
            bins[idx] += 1
        total = sum(bins)
        entropy = 0.0
        for count in bins:
            if count == 0:
                continue
            p = count / total
            entropy -= p * math.log(p, 2)
        max_entropy = math.log(len(bins), 2)
        return entropy / max_entropy if max_entropy else entropy

    def _extract_value(self, line: str, token: str) -> float:
        idx = line.find(token)
        if idx == -1:
            return float("nan")
        remainder = line[idx + len(token):].strip()
        fragment = remainder.split()[0]
        fragment = fragment.rstrip("s,")
        try:
            return float(fragment)
        except ValueError:
            return float("nan")

    def _load_latest_artifact(self) -> Optional[Dict[str, Any]]:
        if not ARTIFACT_DIR.exists():
            return None
        artifacts = sorted(ARTIFACT_DIR.glob("pattern_*.json"), key=os.path.getmtime)
        if not artifacts:
            return None
        latest = artifacts[-1]
        try:
            return json.loads(latest.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def _read_json(self, path: Path) -> Dict[str, Any]:
        if not path.is_file():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    @staticmethod
    def _atomic_write(path: Path, content: str) -> None:
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        with open(tmp_path, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp_path, path)

    @staticmethod
    def _clamp(value: float, lower: float, upper: float) -> float:
        return max(lower, min(value, upper))


# ----------------------------------------------------------------------
def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UBOS Cadence Council Monitor")
    parser.add_argument("--watch", action="store_true", help="Continuously audit cadence")
    parser.add_argument("--once", action="store_true", help="Run a single audit")
    parser.add_argument("--emit-now", action="store_true", help="Force output even if data incomplete")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, ...)")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))
    monitor = CadenceCouncilMonitor()
    watch = args.watch and not args.once
    force_emit = args.emit_now
    monitor.run(watch=watch, force_emit=force_emit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
