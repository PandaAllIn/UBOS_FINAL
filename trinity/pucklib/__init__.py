"""
Constitutional puck library utilities.

This package will gradually house the full builder, validation, and transport
stack described in `SPEC_puck_library_architecture.md`. For Phase 1 we expose
the Talking Drum transport primitives so agents can exchange pucks over the
filesystem Mailroom (COMMS_HUB) with rhythmic signalling.
"""

from .comms.talking_drum import TalkingDrumTransmitter, RhythmDefinition, RHYTHMS, RhythmDetection  # noqa: F401

__all__ = [
    "TalkingDrumTransmitter",
    "RhythmDefinition",
    "RHYTHMS",
    "RhythmDetection",
]
