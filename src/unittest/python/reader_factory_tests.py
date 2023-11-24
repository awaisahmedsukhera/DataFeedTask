from unittest import TestCase
from src.main.python.reader_factory import ReaderFactory


class TestReaderFactory(TestCase):
    def test_create_data_source_with_valid_type(self):
        factory = ReaderFactory()
        source_type = "xml"
        data_destination = factory.create_data_source(source_type)
        self.assertIsNotNone(data_destination)

    def test_create_data_destination_with_invalid_type(self):
        factory = ReaderFactory()
        source_type = "invalid_type"
        with self.assertRaises(ValueError):
            factory.create_data_source(source_type)
