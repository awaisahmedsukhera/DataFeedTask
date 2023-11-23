from abc import ABC, abstractmethod
import logging
import sqlite3

# Creating a logger for this module
logger = logging.getLogger(__name__)


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
            error_message = f"SQLite error while writing data to {db_file}: {e}"
            logger.error(error_message, exc_info=True)

    def get_column_names(self, element):
        return [child.tag for child in element]
