"""Data ingestion services for the Master Librarian."""

from .ubos_ingester import UbosIngester, UBOSKnowledgeIngester
from .yaml_parser import parse_concept_yaml

# Alias for backward compatibility or typo correction
UBOSKnowledgeIngester = UbosIngester

__all__ = ["UbosIngester", "UBOSKnowledgeIngester", "parse_concept_yaml"]