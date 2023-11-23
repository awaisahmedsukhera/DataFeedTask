from data_source.source import XMLDataSource
from data_destination.destination import SQLiteDestination
import logging

# Creating a logger for this file
logger = logging.getLogger(__name__)


# Factory class to create objects based on source and destination type
class DataProcessorFactory:
    @staticmethod
    def process_data(source_type, destination_type, source_file, destination_file):

        if source_type == "xml":
            data_source = XMLDataSource()
        else:
            error_message = f"Invalid source type: {source_type}"
            logger.error(error_message)
            raise ValueError(error_message)

        if destination_type == "sqlite":
            data_destination = SQLiteDestination()
        else:
            error_message = f"Invalid destination type: {destination_type}"
            logger.error(error_message)
            raise ValueError(error_message)

        if data_source and data_destination:
            data = data_source.read_data(source_file)
            if data:
                data_destination.write_data(data, destination_file)
                logger.info(f"Data processed successfully from {source_type} to {destination_type}")
            else:
                logger.warning("No data to process.")
        else:
            logger.error("Invalid source or destination type.")
