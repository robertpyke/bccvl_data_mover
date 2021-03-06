import datetime
import unittest

from data_mover.domain.dataset import *


class TestDataset(unittest.TestCase):

    def test_dataset_provenance_init(self):
        source = DatasetProvenance.SOURCE_ALA
        url = "http://some.url.org.au"
        source_date = datetime.datetime.now()

        to_test = DatasetProvenance(source, url, source_date)
        self.assertEqual(source, to_test.source)
        self.assertEqual(url, to_test.url)
        self.assertEqual(source_date, to_test.source_date)

    def test_dataset_provenance_eq_ne(self):
        source = DatasetProvenance.SOURCE_ALA
        url = "http://some.url.org.au"
        source_date = datetime.datetime.now()

        dp_1 = DatasetProvenance(source, url, source_date)
        dp_2 = DatasetProvenance(source, url, source_date)

        self.assertTrue(dp_1 == dp_1)
        self.assertFalse(dp_1 != dp_1)
        self.assertTrue(dp_1 == dp_2)
        self.assertFalse(dp_1 != dp_2)

        self.assertFalse(dp_1 == DatasetProvenance("Some other source", url, source_date))
        self.assertTrue(dp_1 != DatasetProvenance("Some other source", url, source_date))

        self.assertFalse(dp_1 == DatasetProvenance(source, "http://some.other.url.org.au", source_date))
        self.assertTrue(dp_1 != DatasetProvenance(source, "http://some.other.url.org.au", source_date))

        self.assertFalse(dp_1 == DatasetProvenance(source, url, source_date + datetime.timedelta(seconds=1000)))
        self.assertTrue(dp_1 != DatasetProvenance(source, url, source_date + datetime.timedelta(seconds=1000)))

        self.assertFalse(dp_1 == "dp_1")
        self.assertTrue(dp_1 != "dp_1")

        self.assertFalse(dp_1 == None)
        self.assertTrue(dp_1 != None)

    def test_dataset_file_init(self):
        url = "file://some/path/to/the/file"
        dataset_type = DatasetFile.TYPE_OCCURRENCES
        size = 1234

        to_test = DatasetFile(url, dataset_type, size)
        self.assertEqual(url, to_test.url)
        self.assertEqual(dataset_type, to_test.dataset_type)
        self.assertEqual(size, to_test.size)

    def test_dataset_file_eq_ne(self):
        url = "file://some/path/to/the/file"
        dataset_type = DatasetFile.TYPE_OCCURRENCES
        size = 1234

        df_1 = DatasetFile(url, dataset_type, size)
        df_2 = DatasetFile(url, dataset_type, size)

        self.assertTrue(df_1 == df_1)
        self.assertFalse(df_1 != df_1)
        self.assertTrue(df_1 == df_2)
        self.assertFalse(df_1 != df_2)

        self.assertFalse(df_1 == DatasetFile("file://some/other/path/to/dataset", dataset_type, size))
        self.assertTrue(df_1 != DatasetFile("file://some/other/path/to/dataset", dataset_type, size))

        self.assertFalse(df_1 == DatasetFile(url, DatasetFile.TYPE_ATTRIBUTION, size))
        self.assertTrue(df_1 != DatasetFile(url, DatasetFile.TYPE_ATTRIBUTION, size))

        self.assertFalse(df_1 == DatasetFile(url, dataset_type, 4562))
        self.assertTrue(df_1 != DatasetFile(url, dataset_type, 4562))

        self.assertFalse(df_1 == "df_1")
        self.assertTrue(df_1 != "df_1")

        self.assertFalse(df_1 == None)
        self.assertTrue(df_1 != None)

    def test_dataset_init(self):
        source = DatasetProvenance.SOURCE_ALA
        url = "http://some.url.org.au"
        source_date = datetime.datetime.now()

        url_1 = "some/path/to/the/file/1"
        dataset_type_1 = DatasetFile.TYPE_OCCURRENCES
        size_1 = 1234
        url_2 = "some/path/to/the/file/2"
        dataset_type_2 = DatasetFile.TYPE_ATTRIBUTION
        size_2 = 4567

        file_1 = DatasetFile(url_1, dataset_type_1, size_1)
        file_2 = DatasetFile(url_2, dataset_type_2, size_2)

        files = [file_1, file_2]
        provenance = DatasetProvenance(source, url, source_date)

        title = "the title of my dataset"
        description = "a dataset thats used in unit testing"
        num_occurrences = 14432

        to_test = Dataset(title, description, num_occurrences, files, provenance)

        self.assertEqual(title, to_test.title)
        self.assertEqual(description, to_test.description)
        self.assertEqual(files, to_test.files)
        self.assertEqual(provenance, to_test.provenance)

    def test_dataset_eq_ne(self):
        file_1 = DatasetFile("path_1", DatasetFile.TYPE_ATTRIBUTION, 1234)
        file_2 = DatasetFile("path_2", DatasetFile.TYPE_OCCURRENCES, 5678)
        files = [file_1, file_2]
        provenance = DatasetProvenance("some source", "http://intersect.org.au", datetime.datetime.now())
        title = "the title"
        description = "description"
        num_occurrences = 153
        ds_1 = Dataset(title, description, num_occurrences, files, provenance)
        ds_2 = Dataset(title, description, num_occurrences, files, provenance)

        self.assertTrue(ds_1 == ds_1)
        self.assertFalse(ds_1 != ds_1)
        self.assertTrue(ds_1 == ds_2)
        self.assertFalse(ds_1 != ds_2)

        self.assertTrue(ds_1 != Dataset("another title", description, num_occurrences, files, provenance))
        self.assertFalse(ds_1 == Dataset("another title", description, num_occurrences, files, provenance))

        self.assertTrue(ds_1 != Dataset(title, "another description", num_occurrences, files, provenance))
        self.assertFalse(ds_1 == Dataset(title, "another description", num_occurrences, files, provenance))

        self.assertTrue(ds_1 != Dataset(title, description, 111, files, provenance))
        self.assertFalse(ds_1 == Dataset(title, description, 111, files, provenance))

        self.assertTrue(ds_1 != Dataset(title, description, num_occurrences, [file_1], provenance))
        self.assertFalse(ds_1 == Dataset(title, description, num_occurrences, [file_1], provenance))

        self.assertTrue(ds_1 != Dataset(title, description, num_occurrences, files, DatasetProvenance("another source", "http://intersect.org.au", datetime.datetime.now())))
        self.assertFalse(ds_1 == Dataset(title, description, num_occurrences, files, DatasetProvenance("another source", "http://intersect.org.au", datetime.datetime.now())))

        self.assertFalse(ds_1 == "ds_1")
        self.assertTrue(ds_1 != "ds_1")

        self.assertFalse(ds_1 == None)
        self.assertTrue(ds_1 != None)
