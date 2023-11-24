import logging
from reader import Reader
from writer import Writer

# Creating a logger for this file
logger = logging.getLogger(__name__)


class DataProcessor:
    @staticmethod
    def process_data(data_source: Reader, data_destination: Writer, source_file: str, destination_file: str):

        if data_source and data_destination:
            data = data_source.read_data(source_file)
            if data:
                data_destination.write_data(data, destination_file)
                logger.info(f"Data processed successfully from {data_source} to {data_destination}")
            else:
                logger.warning("No data to process.")
        else:
            logger.error("Invalid source or destination type.")
