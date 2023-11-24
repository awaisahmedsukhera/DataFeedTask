# from unittest import TestCase
# from src.main.python.writer_factory import WriterFactory
#
#
# class TestWriterFactory(TestCase):
#     def test_create_data_destination_with_valid_type(self):
#         factory = WriterFactory()
#         destination_type = "sqlite"
#         data_destination = factory.create_data_destination(destination_type)
#         self.assertIsNotNone(data_destination)
#
#     def test_create_data_destination_with_invalid_type(self):
#         factory = WriterFactory()
#         destination_type = "invalid_type"
#         with self.assertRaises(ValueError):
#             factory.create_data_destination(destination_type)
