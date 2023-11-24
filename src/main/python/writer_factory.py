from writer import SQLiteDestination, Writer
import logging
from typing import Type

logger = logging.getLogger(__name__)


# Factory class to create object based on destination type
class WriterFactory:
    @staticmethod
    def create_data_destination(destination_type: str) -> Type[Writer]:
        if destination_type == "sqlite":
            return SQLiteDestination()
        else:
            error_message = f"Invalid destination type: {destination_type}"
            logger.error(error_message)
            raise ValueError(error_message)
