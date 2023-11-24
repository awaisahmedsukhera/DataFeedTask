from abc import ABC, abstractmethod
import logging
import xml.etree.ElementTree as ET

# Creating a logger for this module
logger = logging.getLogger(__name__)


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
            error_message = f"Error parsing XML in file '{file_path}': {e}"
            logger.error(error_message, exc_info=True)
            return None
