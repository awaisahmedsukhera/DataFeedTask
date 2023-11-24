import os
import tempfile
import sqlite3
import unittest
from src.main.python.data_processor import DataProcessor
from src.main.python.reader_factory import XMLDataSource
from src.main.python.writer_factory import SQLiteDestination
import xml.etree.ElementTree as ET


class TestDataProcessorIntegration(unittest.TestCase):
    def setUp(self):
        # Creating a temporary XML file for testing
        self.xml_file_fd, self.xml_file_path = tempfile.mkstemp(suffix=".xml")

        # Creating a temporary SQLite database file for testing
        self.sqlite_file_fd, self.sqlite_file_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        # Closing and removing the temporary files after testing
        os.close(self.xml_file_fd)
        os.remove(self.xml_file_path)

        os.close(self.sqlite_file_fd)
        os.remove(self.sqlite_file_path)

    def _write_test_xml_data(self, root_element):
        # Helper method to write XML content to the temporary XML file
        tree = ET.ElementTree(root_element)
        tree.write(self.xml_file_path)

    def test_process_data_integration(self):
        # Creating an XML structure with sample data
        root = ET.Element("catalog")

        # Sample item
        item = ET.SubElement(root, "item")
        entity_id = ET.SubElement(item, "entity_id")
        entity_id.text = "123"
        category_name = ET.SubElement(item, "CategoryName")
        category_name.text = "Test\\ Product"
        sku = ET.SubElement(item, "sku")
        sku.text = "456"
        name = ET.SubElement(item, "name")
        name.text = "Test Product"
        description = ET.SubElement(item, "description")
        description.text = "This is a sample product description."
        shortdesc = ET.SubElement(item, "shortdesc")
        shortdesc.text = "Short description for the product."
        price = ET.SubElement(item, "price")
        price.text = "19.99"
        link = ET.SubElement(item, "link")
        link.text = "http://example.com/product"
        image = ET.SubElement(item, "image")
        image.text = "http://example.com/product_image.jpg"
        brand = ET.SubElement(item, "Brand")
        brand.text = "Test Brand"
        rating = ET.SubElement(item, "Rating")
        rating.text = "4.5"
        caffeinetype = ET.SubElement(item, "CaffeineType")
        caffeinetype.text = "Caffeinated"
        count = ET.SubElement(item, "Count")
        count.text = "24"
        flavored = ET.SubElement(item, "Flavored")
        flavored.text = "Yes"
        seasonal = ET.SubElement(item, "Seasonal")
        seasonal.text = "No"
        instock = ET.SubElement(item, "Instock")
        instock.text = "Yes"
        facebook = ET.SubElement(item, "Facebook")
        facebook.text = "1"
        iskcup = ET.SubElement(item, "IsKCup")
        iskcup.text = "1"

        # Writing the XML data to the temporary file
        self._write_test_xml_data(root)

        mock_source = XMLDataSource()
        mock_destination = SQLiteDestination()

        # Calling the process_data method
        DataProcessor.process_data(mock_source, mock_destination, self.xml_file_path, self.sqlite_file_path)

        # Assertions
        self.assertTrue(os.path.exists(self.sqlite_file_path))  # Checking if SQLite file was created

        # Verifying the data in the SQLite database
        connection = sqlite3.connect(self.sqlite_file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM catalog")
        rows = cursor.fetchall()

        expected_row = (
            1, "123", "Test\\ Product", "456", "Test Product", "This is a sample product description.",
            "Short description for the product.", "19.99", "http://example.com/product",
            "http://example.com/product_image.jpg", "Test Brand", "4.5", "Caffeinated", "24", "Yes", "No", "Yes", "1",
            "1")

        self.assertEqual(rows[0], expected_row)

        connection.close()
