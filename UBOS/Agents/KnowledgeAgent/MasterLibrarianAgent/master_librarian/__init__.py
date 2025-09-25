"""Master Librarian Agent - UBOS Knowledge Core."""

__version__ = "1.0.0"

from .api import create_app
from .cli import main
from .graph import UBOSKnowledgeGraph
from .ingestion import UbosIngester
from .services import ConsultationService