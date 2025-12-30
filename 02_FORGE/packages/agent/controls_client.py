"""Victorian Control Mechanisms integration client.

This module provides integration with the Victorian-inspired control mechanisms:
- Governor: PID controller for dynamic concurrency adjustment
- Relief Valve: Resource-based system protection
- Escapement: Periodic tick mechanism for timing

These controls are already implemented in harness.py, this module provides
additional monitoring and coordination capabilities.
"""
from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from .logging_utils import AuditLogger, LogEvent


@dataclass(slots=True)
class SystemMetrics:
    """Current system resource metrics."""

    timestamp: str
    cpu_load_1min: float
    cpu_load_5min: float
    cpu_load_15min: float
    memory_total_mb: int
    memory_available_mb: int
    memory_used_mb: int
    memory_percent: float
    disk_used_percent: float
    active_processes: int
    network_connections: int


@dataclass(slots=True)
class GovernorState:
    """Current state of the Governor (PID controller)."""

    timestamp: str
    allowed_concurrency: int
    max_concurrency: int
    target_backlog: int
    current_backlog: int
    active_tasks: int
    proportional_error: float
    integral_error: float


@dataclass(slots=True)
class ReliefValveState:
    """Current state of the Relief Valve (system protection)."""

    timestamp: str
    is_degraded: bool
    cpu_threshold_percent: Optional[int]
    memory_threshold_mb: Optional[int]
    current_cpu_percent: float
    current_memory_mb: int
    network_blocked: bool


class ControlsClient:
    """Client for monitoring and coordinating Victorian control mechanisms."""

    def __init__(
        self,
        audit_logger: AuditLogger,
        vessel_id: str = "janus-in-balaur",
        metrics_interval: timedelta = timedelta(seconds=30),
    ) -> None:
        self.audit_logger = audit_logger
        self.vessel_id = vessel_id
        self.metrics_interval = metrics_interval
        self._monitor_task: Optional[asyncio.Task[None]] = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        """Start controls monitoring."""
        if self._monitor_task and not self._monitor_task.done():
            return
        self._stop_event.clear()
        self._monitor_task = asyncio.create_task(
            self._monitor_loop(),
            name="janus-controls-monitor",
        )
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="controls_client.started",
                data={},
            )
        )

    async def stop(self) -> None:
        """Stop controls monitoring."""
        if not self._monitor_task or self._monitor_task.done():
            return
        self._stop_event.set()
        if self._monitor_task:
            await self._monitor_task

    async def _monitor_loop(self) -> None:
        """Periodic monitoring loop for system metrics."""
        while not self._stop_event.is_set():
            try:
                metrics = self.collect_system_metrics()
                self._emit_metrics(metrics)

                # Check for anomalies or concerning patterns
                await self._check_anomalies(metrics)

            except Exception as exc:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="error",
                        vessel=self.vessel_id,
                        event="controls_client.monitor_error",
                        data={"error": str(exc)},
                    )
                )

            await asyncio.sleep(self.metrics_interval.total_seconds())

    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system resource metrics."""
        timestamp = datetime.now(timezone.utc).isoformat()

        # CPU load averages
        try:
            load1, load5, load15 = os.getloadavg()
        except OSError:
            load1 = load5 = load15 = 0.0

        # Memory metrics
        mem_total = 0
        mem_available = 0
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        mem_total = int(line.split()[1])  # kB
                    elif line.startswith("MemAvailable:"):
                        mem_available = int(line.split()[1])  # kB
        except (FileNotFoundError, IOError, ValueError):
            pass

        mem_total_mb = mem_total // 1024
        mem_available_mb = mem_available // 1024
        mem_used_mb = mem_total_mb - mem_available_mb
        mem_percent = (mem_used_mb / mem_total_mb * 100) if mem_total_mb > 0 else 0

        # Disk usage (for /srv/janus)
        disk_used_percent = 0.0
        try:
            stat = os.statvfs("/srv/janus")
            disk_total = stat.f_blocks * stat.f_frsize
            disk_free = stat.f_bfree * stat.f_frsize
            disk_used = disk_total - disk_free
            disk_used_percent = (disk_used / disk_total * 100) if disk_total > 0 else 0
        except (FileNotFoundError, OSError):
            pass

        # Process count (rough estimate)
        active_processes = 0
        try:
            active_processes = len([p for p in Path("/proc").iterdir() if p.name.isdigit()])
        except (FileNotFoundError, OSError):
            pass

        # Network connections (rough estimate)
        network_connections = 0
        try:
            with open("/proc/net/tcp", "r", encoding="utf-8") as f:
                network_connections = len(f.readlines()) - 1  # Exclude header
        except (FileNotFoundError, IOError):
            pass

        return SystemMetrics(
            timestamp=timestamp,
            cpu_load_1min=load1,
            cpu_load_5min=load5,
            cpu_load_15min=load15,
            memory_total_mb=mem_total_mb,
            memory_available_mb=mem_available_mb,
            memory_used_mb=mem_used_mb,
            memory_percent=mem_percent,
            disk_used_percent=disk_used_percent,
            active_processes=active_processes,
            network_connections=network_connections,
        )

    def _emit_metrics(self, metrics: SystemMetrics) -> None:
        """Emit metrics to audit log."""
        self.audit_logger.emit(
            LogEvent.create(
                level="debug",
                vessel=self.vessel_id,
                event="controls.metrics",
                data={
                    "cpu_load_1min": round(metrics.cpu_load_1min, 2),
                    "memory_used_mb": metrics.memory_used_mb,
                    "memory_percent": round(metrics.memory_percent, 1),
                    "disk_used_percent": round(metrics.disk_used_percent, 1),
                    "active_processes": metrics.active_processes,
                },
            )
        )

    async def _check_anomalies(self, metrics: SystemMetrics) -> None:
        """Check for anomalous system conditions."""
        # High memory usage warning
        if metrics.memory_percent > 90:
            self.audit_logger.emit(
                LogEvent.create(
                    level="warn",
                    vessel=self.vessel_id,
                    event="controls.anomaly.high_memory",
                    data={
                        "memory_percent": round(metrics.memory_percent, 1),
                        "memory_used_mb": metrics.memory_used_mb,
                    },
                )
            )

        # High CPU load warning
        cpu_cores = os.cpu_count() or 1
        cpu_load_percent = (metrics.cpu_load_1min / cpu_cores) * 100
        if cpu_load_percent > 90:
            self.audit_logger.emit(
                LogEvent.create(
                    level="warn",
                    vessel=self.vessel_id,
                    event="controls.anomaly.high_cpu",
                    data={
                        "cpu_load_1min": round(metrics.cpu_load_1min, 2),
                        "cpu_load_percent": round(cpu_load_percent, 1),
                    },
                )
            )

        # High disk usage warning
        if metrics.disk_used_percent > 85:
            self.audit_logger.emit(
                LogEvent.create(
                    level="warn",
                    vessel=self.vessel_id,
                    event="controls.anomaly.high_disk",
                    data={"disk_used_percent": round(metrics.disk_used_percent, 1)},
                )
            )

    def create_governor_state(
        self,
        allowed_concurrency: int,
        max_concurrency: int,
        target_backlog: int,
        current_backlog: int,
        active_tasks: int,
        proportional_error: float,
        integral_error: float,
    ) -> GovernorState:
        """Create governor state snapshot."""
        return GovernorState(
            timestamp=datetime.now(timezone.utc).isoformat(),
            allowed_concurrency=allowed_concurrency,
            max_concurrency=max_concurrency,
            target_backlog=target_backlog,
            current_backlog=current_backlog,
            active_tasks=active_tasks,
            proportional_error=proportional_error,
            integral_error=integral_error,
        )

    def create_relief_valve_state(
        self,
        is_degraded: bool,
        cpu_threshold_percent: Optional[int],
        memory_threshold_mb: Optional[int],
        current_cpu_percent: float,
        current_memory_mb: int,
        network_blocked: bool,
    ) -> ReliefValveState:
        """Create relief valve state snapshot."""
        return ReliefValveState(
            timestamp=datetime.now(timezone.utc).isoformat(),
            is_degraded=is_degraded,
            cpu_threshold_percent=cpu_threshold_percent,
            memory_threshold_mb=memory_threshold_mb,
            current_cpu_percent=current_cpu_percent,
            current_memory_mb=current_memory_mb,
            network_blocked=network_blocked,
        )

    def emit_governor_state(self, state: GovernorState) -> None:
        """Log governor state for monitoring."""
        self.audit_logger.emit(
            LogEvent.create(
                level="debug",
                vessel=self.vessel_id,
                event="controls.governor",
                data={
                    "allowed": state.allowed_concurrency,
                    "max": state.max_concurrency,
                    "backlog": state.current_backlog,
                    "active": state.active_tasks,
                    "error": round(state.proportional_error, 2),
                },
            )
        )

    def emit_relief_valve_state(self, state: ReliefValveState) -> None:
        """Log relief valve state for monitoring."""
        self.audit_logger.emit(
            LogEvent.create(
                level="info" if not state.is_degraded else "warn",
                vessel=self.vessel_id,
                event="controls.relief_valve",
                data={
                    "degraded": state.is_degraded,
                    "cpu_percent": round(state.current_cpu_percent, 1),
                    "memory_mb": state.current_memory_mb,
                    "network_blocked": state.network_blocked,
                },
            )
        )

    def query_rate_limit(self, action_type: str) -> tuple[bool, str]:
        """Query Governor for rate limit approval.

        Returns (is_allowed, reason) tuple.
        """
        # In production, this would integrate with the Governor's rate limiting logic
        # For now, implement basic checks

        metrics = self.collect_system_metrics()

        # Check CPU load
        cpu_cores = os.cpu_count() or 1
        cpu_load_percent = (metrics.cpu_load_1min / cpu_cores) * 100
        if cpu_load_percent > 95:
            return False, f"CPU load too high: {cpu_load_percent:.1f}%"

        # Check memory
        if metrics.memory_percent > 95:
            return False, f"Memory usage too high: {metrics.memory_percent:.1f}%"

        # Check disk space
        if metrics.disk_used_percent > 95:
            return False, f"Disk usage too high: {metrics.disk_used_percent:.1f}%"

        return True, "Rate limit checks passed"

    def request_escapement_tick(self) -> bool:
        """Request permission to execute on next Escapement tick.

        The Escapement ensures actions are synchronized and paced appropriately.
        """
        # The Escapement is implemented in harness.py's _tick_loop
        # This method is a placeholder for future coordination features
        return True

    def check_relief_valve_status(self) -> tuple[bool, str]:
        """Check if Relief Valve has activated system protection.

        Returns (is_operational, status_message) tuple.
        """
        metrics = self.collect_system_metrics()

        cpu_cores = os.cpu_count() or 1
        cpu_load_percent = (metrics.cpu_load_1min / cpu_cores) * 100

        # Check if we're in degraded mode
        if cpu_load_percent > 90 or metrics.memory_percent > 90:
            return False, "System in degraded mode - Relief Valve activated"

        return True, "System operational"
