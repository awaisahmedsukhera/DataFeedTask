import argparse
import logging
from data_processor_factory import DataProcessorFactory

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
        # Using the factory to process data
        logger.info(f"Starting data processing: Source={args.source_type}, Destination={args.destination_type}")
        processor_factory = DataProcessorFactory()
        processor_factory.process_data(args.source_type, args.destination_type, args.source_file, args.destination_file)
        logger.info("Data processing completed successfully")
    except ValueError as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
