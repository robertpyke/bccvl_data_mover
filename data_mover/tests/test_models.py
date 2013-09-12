import unittest
from data_mover.models.job import Job
from data_mover.models.ala_job import ALAJob


class TestModels(unittest.TestCase):

    def testJobModel(self):
        theType = 'someType'
        data_id = 7
        destination = 'someDestination'
        job = Job(theType, data_id, destination)
        self.assertEqual(theType, job.type)
        self.assertEqual(data_id, job.data_id)
        self.assertEquals(destination, job.destination)
        self.assertEquals(Job.STATUS_PENDING, job.status)
        self.assertIsNone(job.start_timestamp)
        self.assertIsNone(job.end_timestamp)
        self.assertEqual('sample/sample_source', job.source)

    def testALAJobModel(self):
        lsid = 'urn:lsid:biodiversity.org.au:afd.taxon:31a9b8b8-4e8f-4343-a15f-2ed24e0bf1ae'
        dataset_id = 1337
        ala_job = ALAJob(lsid, dataset_id)
        self.assertEqual(lsid, ala_job.lsid)
        self.assertEqual(dataset_id, ala_job.dataset_id)
        self.assertIsNotNone(ala_job.submitted_time)
        self.assertIsNone(ala_job.start_time)
        self.assertIsNone(ala_job.end_time)
        self.assertEqual(Job.STATUS_PENDING, ala_job.status)