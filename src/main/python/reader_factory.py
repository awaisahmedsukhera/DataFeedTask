from src.main.python.reader import XMLDataSource
import logging
from typing import Type

# Creating a logger for this file
logger = logging.getLogger(__name__)


# Factory class to create object based on source type
class ReaderFactory:
    @staticmethod
    def create_data_source(source_type: str) -> Type[XMLDataSource]:
        if source_type == "xml":
            return XMLDataSource()
        else:
            error_message = f"Invalid source type: {source_type}"
            logger.error(error_message)
            raise ValueError(error_message)
