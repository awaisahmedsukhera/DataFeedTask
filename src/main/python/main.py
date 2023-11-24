import argparse
import logging
from reader_factory import ReaderFactory
from writer_factory import WriterFactory
from data_processor import DataProcessor

# Setting up a logger for the main script
logger = logging.getLogger(__name__)

# Creating a FileHandler to log errors to a file
error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

# Adding the FileHandler to the logger
logger.addHandler(error_handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process data and push it to a destination')
    parser.add_argument('--source-type', type=str, help='Type of the data source')
    parser.add_argument('--destination-type', type=str, help='Type of the data destination')
    parser.add_argument('source_file', type=str, help='Path to the source file')
    parser.add_argument('destination_file', type=str, help='Path to the destination file')

    args = parser.parse_args()

    try:
        logger.info(f"Starting data processing: Source={args.source_type}, Destination={args.destination_type}")
        # Using the factories to get source and destination type
        reader_factory = ReaderFactory()
        source_type = reader_factory.create_data_source(args.source_type)
        writer_factory = WriterFactory()
        destination_type = writer_factory.create_data_destination(args.destination_type)
        # Processing data based on the source and destination types
        data_processor = DataProcessor()
        data_processor.process_data(source_type, destination_type, args.source_file, args.destination_file)
        logger.info("Data processing completed successfully")
    except ValueError as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
