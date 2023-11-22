import argparse
import logging
import sqlite3
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import json

# Logging configuration
logging.basicConfig(filename='error.log', level=logging.ERROR)


class DataSource(ABC):
    @abstractmethod
    def read_data(self, file_path):
        pass


class XMLDataSource(DataSource):
    def read_data(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            logging.error(f"Error parsing XML: {e}")
            return None


class DataDestination(ABC):
    @abstractmethod
    def write_data(self, data, db_file):
        pass


class SQLiteDestination(DataDestination):
    def write_data(self, data, db_file):
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()

            for table_name, entries in data.items():
                # Creating a table (if not exists) for the data
                c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                            id INTEGER PRIMARY KEY,
                                            {', '.join(self.get_column_names(entries[0]))}
                                         )''')

                # Inserting data into the table
                for entry in entries:
                    values = [entry.find(column).text for column in self.get_column_names(entry)]
                    c.execute(f'''INSERT INTO {table_name} ({', '.join(self.get_column_names(entry))}) VALUES 
                    ({', '.join(['?'] * len(values))})''', values)

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e}")

    def get_column_names(self, element):
        return [child.tag for child in element]


class DataProcessor:
    def __init__(self, data_source: DataSource, data_destination: DataDestination):
        self.data_source = data_source
        self.data_destination = data_destination

    def process_data(self, source_file, destination_file):
        data = self.data_source.read_data(source_file)
        if data:
            self.data_destination.write_data(data, destination_file)


class DataProcessorFactory:
    @staticmethod
    def create_data_processor(source_type, destination_type):
        try:
            data_source = source_type()
            data_destination = destination_type()
            return DataProcessor(data_source, data_destination)
        except Exception as e:
            raise ValueError(f"Error creating DataProcessor: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process XML data and push it to a database')
    parser.add_argument('xml_file', type=str, help='Path to the XML file')
    parser.add_argument('db_file', type=str, help='Path to the SQLite database file')

    args = parser.parse_args()

    try:
        processor_factory = DataProcessorFactory()
        processor = processor_factory.create_data_processor(XMLDataSource, SQLiteDestination)

        processor.process_data(args.xml_file, args.db_file)
    except ValueError as e:
        print(f"Error: {e}")
