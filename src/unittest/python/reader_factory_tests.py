from unittest import TestCase

from ...main.python.reader_factory import ReaderFactory


class TestReaderFactory(TestCase):

    def test_create_destination_with_invalid_type(self):
        reader_factory = ReaderFactory()
        source_type = "xmsl"
        with self.assertRaises(ValueError):
            reader_factory.create_data_source(source_type)

