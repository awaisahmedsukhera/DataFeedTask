import argparse
import logging
import sqlite3
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

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

            # Creating a table (if not exists) for the data
            c.execute('''CREATE TABLE IF NOT EXISTS xml_data (
                            id INTEGER PRIMARY KEY,
                            field1 TEXT,
                            field2 TEXT,
                            field3 TEXT
                         )''')

            # Inserting data into the table
            for entry in data:
                c.execute('''INSERT INTO xml_data (field1, field2, field3)
                             VALUES (?, ?, ?)''', (entry['field1'], entry['field2'], entry['field3']))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e}")


class DataProcessor:
    def __init__(self, data_source: DataSource, data_destination: DataDestination):
        self.data_source = data_source
        self.data_destination = data_destination

    def process_data(self, source_file, destination_file):
        data = self.data_source.read_data(source_file)
        if data:
            data_to_push = []
            for entry in data.findall('entry'):
                field1 = entry.find('field1').text
                field2 = entry.find('field2').text
                field3 = entry.find('field3').text

                data_to_push.append({'field1': field1, 'field2': field2, 'field3': field3})

            self.data_destination.write_data(data_to_push, destination_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process XML data and push it to a database')
    parser.add_argument('xml_file', type=str, help='Path to the XML file')
    parser.add_argument('db_file', type=str, help='Path to the SQLite database file')

    args = parser.parse_args()

    # Instantiating data source and destination
    xml_data_source = XMLDataSource()
    sqlite_data_destination = SQLiteDestination()

    processor = DataProcessor(xml_data_source, sqlite_data_destination)
    processor.process_data(args.xml_file, args.db_file)
