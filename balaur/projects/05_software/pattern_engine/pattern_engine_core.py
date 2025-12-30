#!/usr/bin/env python3
"""Pattern Engine Core v1.0 (Article IV)."""
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
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


DEFAULT_ORCHESTRION_SPEC = \
    Path("/srv/janus/balaur/projects/03_systems/infrastructure/orchestrion_spec_v1.md")
URIP_CLOCK_DIR = Path("/srv/janus/balaur/signal/clock")
ORACLE_SYNC_DIR = Path("/srv/janus/balaur/oracle_trinity/sync")


@dataclass
class HarmonicSeed:
    tempo: float
    priority_band: Optional[str]
    raw: Dict[str, str]


class PatternEngineCore:
    """Implements Fourier/Wavelet analysis and artifact generation."""

    def __init__(self, project_dir: Path, orchestrion_spec: Path):
        self.project_dir = project_dir
        self.artifacts_dir = self.project_dir / "artifacts"
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.orchestrion_spec = orchestrion_spec
        self.rhythm_state_path = URIP_CLOCK_DIR / "rhythm_state.json"
        self.rhythm_history_path = URIP_CLOCK_DIR / "rhythm_history.log"
        self.release_token_path = URIP_CLOCK_DIR / "next_release.token"
        self.logger = logging.getLogger("PatternEngine")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self, watch: bool, force_emit: bool, window_points: int = 96) -> None:
        while True:
            self._respect_release_window()
            window = self._load_history(window_points)
            metrics: Dict[str, any] = {"interval": 6.0}
            if not window[0].size:
                self.logger.warning("No URIP rhythm history available; skipping cycle")
            else:
                metrics = self._compute_metrics(window)
                if force_emit or self._should_emit(metrics):
                    artifact = self._build_artifact(metrics, window)
                    self._write_artifact(artifact)
                    self.logger.info("Pattern artifact emitted: %s", artifact["id"])
                else:
                    self.logger.info(
                        "Metrics below emission threshold (energy=%.2f, cohesion=%.2f)",
                        metrics["fourier"]["energy"],
                        metrics["cohesion"],
                    )
            if not watch:
                break
            beat_interval = metrics.get("interval", 6.0)
            time.sleep(max(beat_interval, 2.0))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _respect_release_window(self) -> None:
        if not self.release_token_path.is_file():
            return
        try:
            deadline_str = self.release_token_path.read_text(encoding="utf-8").strip()
            if not deadline_str:
                return
            deadline = datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
        except (OSError, ValueError):
            return
        now = datetime.now(timezone.utc)
        if deadline > now:
            wait_s = (deadline - now).total_seconds()
            self.logger.debug("Waiting %.2fs for URIP release window", wait_s)
            time.sleep(wait_s)

    def _load_history(self, max_points: int) -> Tuple[np.ndarray, np.ndarray]:
        if not self.rhythm_history_path.is_file():
            return np.array([]), np.array([])
        try:
            lines = self.rhythm_history_path.read_text(encoding="utf-8").strip().splitlines()
        except OSError:
            return np.array([]), np.array([])
        records: List[Tuple[float, float]] = []
        for line in lines[-max_points:]:
            parts = line.split("|")
            if not parts:
                continue
            ts_str = parts[0].strip()
            amp = self._extract_value(line, "amp=")
            timestamp = self._maybe_epoch(ts_str)
            if timestamp is None or math.isnan(amp):
                continue
            records.append((timestamp, amp))
        if not records:
            return np.array([]), np.array([])
        records.sort(key=lambda item: item[0])
        timestamps = np.array([r[0] for r in records], dtype=float)
        amplitudes = np.array([r[1] for r in records], dtype=float)
        return timestamps, amplitudes

    def _compute_metrics(self, window: Tuple[np.ndarray, np.ndarray]) -> Dict[str, any]:
        timestamps, amplitudes = window
        sample_interval = self._sample_interval(timestamps)
        seed = self._load_harmonic_seed()
        rhythm_state = self._load_rhythm_state()
        interval = float(rhythm_state.get("interval", seed.tempo)) if rhythm_state else seed.tempo
        fourier = self._compute_fourier(amplitudes, sample_interval)
        wavelet = self._compute_wavelet(amplitudes, sample_interval)
        entropy = self._entropy(amplitudes)
        cohesion = self._cohesion(interval)
        metrics = {
            "interval": interval,
            "harmonic_seed": seed,
            "rhythm_state": rhythm_state,
            "fourier": fourier,
            "wavelet": wavelet,
            "entropy": entropy,
            "cohesion": cohesion,
            "window": {
                "start": timestamps[0],
                "end": timestamps[-1],
                "points": len(timestamps),
            },
        }
        return metrics

    def _should_emit(self, metrics: Dict[str, any]) -> bool:
        return (
            metrics["fourier"]["energy"] >= 0.4
            or metrics["wavelet"]["peak_energy"] >= 0.4
            or metrics["cohesion"] >= 0.8
            or metrics["entropy"] <= 0.3
        )

    def _build_artifact(self, metrics: Dict[str, any], window: Tuple[np.ndarray, np.ndarray]) -> Dict[str, any]:
        timestamps, amplitudes = window
        start_iso = self._iso(timestamps[0])
        end_iso = self._iso(timestamps[-1])
        created_at = datetime.now(timezone.utc).replace(microsecond=0)
        created_iso = created_at.isoformat().replace("+00:00", "Z")
        artifact_id = f"pattern_{created_iso.replace(':', '-')}"
        wavelet_info = metrics["wavelet"]
        seed = metrics["harmonic_seed"]
        payload = {
            "id": artifact_id,
            "created_at": created_iso,
            "harmonic_seed": {
                "tempo": seed.tempo,
                "priority_band": seed.priority_band,
                "raw": seed.raw,
            },
            "rhythm_state": metrics.get("rhythm_state"),
            "signals": {
                "dominant_frequency": metrics["fourier"]["frequency"],
                "fourier_energy": metrics["fourier"]["energy"],
                "wavelet_peak_scale": wavelet_info["peak_scale"],
                "wavelet_peak_energy": wavelet_info["peak_energy"],
                "entropy": metrics["entropy"],
                "cohesion": metrics["cohesion"],
            },
            "window": {
                "start": start_iso,
                "end": end_iso,
                "points": metrics["window"]["points"],
            },
            "annotations": self._derive_annotations(metrics),
        }
        return payload

    def _write_artifact(self, artifact: Dict[str, any]) -> None:
        path = self.artifacts_dir / f"{artifact['id']}.json"
        tmp_path = path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as handle:
            json.dump(artifact, handle, indent=2)
        os.replace(tmp_path, path)

    # ------------------------------------------------------------------
    # Metric primitives
    # ------------------------------------------------------------------
    def _compute_fourier(self, amplitudes: np.ndarray, sample_interval: float) -> Dict[str, float]:
        if amplitudes.size < 4:
            return {"frequency": 0.0, "energy": 0.0}
        centered = amplitudes - np.mean(amplitudes)
        spectrum = np.fft.rfft(centered)
        freqs = np.fft.rfftfreq(centered.size, d=sample_interval)
        magnitudes = np.abs(spectrum)
        if magnitudes.size <= 1:
            return {"frequency": 0.0, "energy": 0.0}
        magnitudes[0] = 0.0
        idx = int(np.argmax(magnitudes))
        dom_freq = float(freqs[idx])
        energy = float(magnitudes[idx] / (np.sum(magnitudes) + 1e-9))
        return {"frequency": dom_freq, "energy": energy}

    def _compute_wavelet(self, amplitudes: np.ndarray, sample_interval: float) -> Dict[str, float]:
        if amplitudes.size < 4:
            return {"peak_scale": 0.0, "peak_energy": 0.0}
        centered = amplitudes - np.mean(amplitudes)
        scales = np.array([2, 4, 8, 16, 32], dtype=float)
        energies: Dict[float, float] = {}
        for scale in scales:
            width = max(int(scale * 6), 3)
            t = np.linspace(-3, 3, width)
            wavelet = np.exp(-t**2 / 2) * np.cos(5 * t / scale)
            wavelet /= np.linalg.norm(wavelet) or 1.0
            conv = np.convolve(centered, wavelet, mode="same")
            energy = float(np.mean(conv**2))
            energies[scale * sample_interval] = energy
        peak_scale = max(energies, key=energies.get)
        total = sum(energies.values()) or 1.0
        normalized = {scale: energy / total for scale, energy in energies.items()}
        return {
            "peak_scale": peak_scale,
            "peak_energy": normalized[peak_scale],
            "scale_distribution": normalized,
        }

    def _entropy(self, amplitudes: np.ndarray) -> float:
        if amplitudes.size == 0:
            return 0.0
        values = amplitudes - np.min(amplitudes)
        if np.max(values) > 0:
            values /= np.max(values)
        hist, _ = np.histogram(values, bins=16, range=(0.0, 1.0), density=False)
        total = np.sum(hist)
        if total == 0:
            return 0.0
        probs = hist / total
        probs = probs[probs > 0]
        entropy = -np.sum(probs * np.log2(probs))
        max_entropy = math.log2(16)
        return float(entropy / max_entropy)

    def _cohesion(self, balaur_interval: float) -> float:
        oracle_intervals = self._load_oracle_intervals()
        if not oracle_intervals:
            return 0.0
        diffs = [abs(balaur_interval - val) for val in oracle_intervals]
        mean_diff = float(np.mean(diffs))
        return float(1.0 / (1.0 + mean_diff))

    # ------------------------------------------------------------------
    # Data loading helpers
    # ------------------------------------------------------------------
    def _load_harmonic_seed(self) -> HarmonicSeed:
        if not self.orchestrion_spec.is_file():
            return HarmonicSeed(tempo=6.0, priority_band=None, raw={})
        try:
            text = self.orchestrion_spec.read_text(encoding="utf-8")
        except OSError:
            return HarmonicSeed(tempo=6.0, priority_band=None, raw={})
        tempo = self._match_float(text, r"Tempo\s*[:=]\s*(\d+(?:\.\d+)?)") or 6.0
        priority_match = self._match_str(text, r"Priority\s*(?:Band|Level)?\s*(\w+)")
        return HarmonicSeed(tempo=tempo, priority_band=priority_match, raw={"tempo_line": str(tempo)})

    def _load_rhythm_state(self) -> Dict[str, any]:
        if not self.rhythm_state_path.is_file():
            return {}
        try:
            return json.loads(self.rhythm_state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _load_oracle_intervals(self) -> List[float]:
        if not ORACLE_SYNC_DIR.exists():
            return []
        intervals: List[float] = []
        for path in ORACLE_SYNC_DIR.glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            interval = data.get("interval")
            if isinstance(interval, (int, float)):
                intervals.append(float(interval))
        return intervals

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_value(line: str, token: str) -> float:
        idx = line.find(token)
        if idx == -1:
            return float("nan")
        substr = line[idx + len(token):]
        end = substr.split()[0]
        end = end.rstrip("s,")
        try:
            return float(end)
        except ValueError:
            return float("nan")

    @staticmethod
    def _maybe_epoch(text_ts: str) -> Optional[float]:
        try:
            return datetime.fromisoformat(text_ts.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return None

    @staticmethod
    def _sample_interval(timestamps: np.ndarray) -> float:
        if timestamps.size < 2:
            return 1.0
        diffs = np.diff(timestamps)
        return float(np.mean(diffs)) or 1.0

    @staticmethod
    def _match_float(text: str, pattern: str) -> Optional[float]:
        import re

        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return None
        return float(match.group(1))

    @staticmethod
    def _match_str(text: str, pattern: str) -> Optional[str]:
        import re

        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return None
        return match.group(1)

    @staticmethod
    def _iso(epoch_seconds: float) -> str:
        return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _derive_annotations(metrics: Dict[str, any]) -> List[str]:
        annotations: List[str] = []
        if metrics["fourier"]["energy"] >= 0.4:
            annotations.append("Dominant harmonic spike detected")
        if metrics["wavelet"]["peak_energy"] >= 0.4:
            annotations.append("Transient resonance surge")
        if metrics["cohesion"] >= 0.8:
            annotations.append("Cross-oracle cadence lock")
        if metrics["entropy"] <= 0.3:
            annotations.append("Entropy drop (stabilizing cadence)")
        if not annotations:
            annotations.append("Nominal rhythmic landscape")
        return annotations


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pattern Engine Core v1.0")
    parser.add_argument(
        "--project-dir",
        default="/srv/janus/balaur/projects/05_software/pattern_engine",
        help="Base directory for Pattern Engine artifacts",
    )
    parser.add_argument(
        "--orchestrion-spec",
        default=str(DEFAULT_ORCHESTRION_SPEC),
        help="Path to orchestrion spec file",
    )
    parser.add_argument("--watch", action="store_true", help="Continuously sample and emit artifacts")
    parser.add_argument("--once", action="store_true", help="Run a single cycle (overrides --watch)")
    parser.add_argument("--emit-now", action="store_true", help="Force artifact emission even if below threshold")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, ...)")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))
    project_dir = Path(args.project_dir).expanduser()
    controller = PatternEngineCore(project_dir, Path(args.orchestrion_spec).expanduser())
    watch_mode = args.watch and not args.once
    controller.run(watch=watch_mode, force_emit=args.emit_now)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
