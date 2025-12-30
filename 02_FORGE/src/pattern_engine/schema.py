"""Core data schemas for the Pattern Engine.

This file defines the foundational data structures for the metrics that will be
derived from the analysis of cross-domain harmonics.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PatternMetrics:
    """A snapshot of the planetary feedback compass metrics."""

    entropy_index: float
    """A measure of systemic turbulence and linguistic volatility."""

    resonance_density: float
    """Correlation bandwidth of identical patterns across unrelated domains."""

    cohesion_flux: float
    """Rate at which cooperative motifs arise in the data stream."""

    signal_integrity: float
    """The noise-to-insight ratio of the overall signal."""

    timestamp: int
    """The UTC timestamp when these metrics were calculated."""
