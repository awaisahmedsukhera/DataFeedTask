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
    def write_data(self, data, file_path):
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
                                            data TEXT
                                         )''')

                # Inserting data into the table
                for entry in entries:
                    data_json = json.dumps(self.xml_to_dict(entry))
                    c.execute(f'''INSERT INTO {table_name} (data) VALUES (?)''', (data_json,))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e}")

    def xml_to_dict(self, element):
        data = {}
        for child in element:
            if child:
                data[child.tag] = self.xml_to_dict(child)
            else:
                data[child.tag] = child.text
        return data


class DataProcessor:
    def __init__(self, data_source: DataSource, data_destination: DataDestination):
        self.data_source = data_source
        self.data_destination = data_destination

    def process_data(self, source_file, destination_file):
        data = self.data_source.read_data(source_file)
        if data:
            tables_data = {}
            for entry in data.findall('entry'):
                table_name = entry.tag
                if table_name not in tables_data:
                    tables_data[table_name] = []
                tables_data[table_name].append(entry)

            self.data_destination.write_data(tables_data, destination_file)


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
