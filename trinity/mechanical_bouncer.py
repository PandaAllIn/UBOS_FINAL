#!/usr/bin/env python3
"""
Mechanical Bouncer - Rate Limiter & Load Balancer
Protects API residents from quota exhaustion.
"""

import time
import logging
from enum import Enum
from collections import deque
from dataclasses import dataclass

class Resident(Enum):
    JANUS_LOCAL = "janus"
    CLAUDE = "claude"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"

@dataclass
class RateLimit:
    rpm: int
    tpd: int = -1 # -1 means unlimited

class RateLimitedQueue:
    def __init__(self, limits: RateLimit):
        self.limits = limits
        self.request_timestamps = deque()
        self.daily_tokens = 0
        self.last_day_reset = time.time()

    def can_submit(self) -> bool:
        now = time.time()
        
        # Check RPM
        while self.request_timestamps and now - self.request_timestamps[0] > 60:
            self.request_timestamps.popleft()
        
        if len(self.request_timestamps) >= self.limits.rpm:
            return False
            
        # Check Daily Limit (simplified)
        if now - self.last_day_reset > 86400:
            self.daily_tokens = 0
            self.last_day_reset = now
            
        # We don't strictly track tokens here yet, just request count for now
        # as a proxy if needed, but TPD is hard without response headers
        
        return True

    def submit(self):
        self.request_timestamps.append(time.time())

class MechanicalBouncer:
    def __init__(self):
        self.logger = logging.getLogger("mechanical_bouncer")
        self.queues = {
            Resident.GROQ: RateLimitedQueue(RateLimit(rpm=30, tpd=14400)),
            Resident.GEMINI: RateLimitedQueue(RateLimit(rpm=15)),
            Resident.CLAUDE: RateLimitedQueue(RateLimit(rpm=50)),
            Resident.OPENAI: RateLimitedQueue(RateLimit(rpm=500)),
            Resident.JANUS_LOCAL: RateLimitedQueue(RateLimit(rpm=1000)) # Effectively unlimited
        }
        
        # Map string names to enums for easier lookup
        self.resident_map = {r.value: r for r in Resident}

    def check_admission(self, resident_name: str) -> bool:
        """
        Check if a request can be admitted for the given resident.
        Returns True if allowed, False if rate limited.
        """
        resident = self.resident_map.get(resident_name)
        if not resident:
            # Unknown resident, fail open or closed? Let's fail open for now but log
            self.logger.warning(f"Unknown resident: {resident_name}")
            return True
            
        queue = self.queues.get(resident)
        if not queue:
            return True # No limits defined
            
        if queue.can_submit():
            queue.submit()
            return True
        else:
            self.logger.warning(f"Rate limit hit for {resident_name}")
            return False

    def get_backup(self, resident_name: str) -> str:
        """Return the failover resident for a given resident"""
        resident = self.resident_map.get(resident_name)
        
        failovers = {
            Resident.GROQ: Resident.GEMINI,
            Resident.GEMINI: Resident.CLAUDE,
            Resident.CLAUDE: Resident.OPENAI,
            Resident.OPENAI: Resident.CLAUDE
        }
        
        backup = failovers.get(resident, Resident.JANUS_LOCAL)
        return backup.value
