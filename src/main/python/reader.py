from abc import ABC, abstractmethod
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class Reader(ABC):
    @abstractmethod
    def read_data(self, file_path):
        pass


class XMLDataSource(Reader):
    def read_data(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            error_message = f"Error parsing XML in file '{file_path}': {e}"
            logger.error(error_message, exc_info=True)
            return None
