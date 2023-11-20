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
