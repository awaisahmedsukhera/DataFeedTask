from abc import ABC, abstractmethod
import logging
import sqlite3

logger = logging.getLogger(__name__)


class Writer(ABC):
    @abstractmethod
    def write_data(self, data, db_file):
        pass


class SQLiteDestination(Writer):
    def write_data(self, data, db_file):

        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()

            table_name = data.tag

            for item in data.findall("item"):
                column_names = [child.tag for child in item]

                # Creating a table (if not exists) for the data
                c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                                    id INTEGER PRIMARY KEY,
                                                    {', '.join(column_names)}
                                                 )''')

                # Inserting data into the table
                values = [child.text for child in item]
                placeholders = ', '.join(['?'] * len(values))

                c.execute(f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})", values)

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            error_message = f"SQLite error while writing data to {db_file}: {e}"
            logger.error(error_message, exc_info=True)
