"""The Oracle Bridge package.

This package provides the central, asynchronous interface for connecting the
Pattern Engine to internal and external computational and data oracles.
"""

from .bridge import OracleBridge, OracleJob, JobStatus

__all__ = ["OracleBridge", "OracleJob", "JobStatus"]
