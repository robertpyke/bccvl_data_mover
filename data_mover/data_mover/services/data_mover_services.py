from pyramid_xmlrpc import XMLRPCView
from data_mover.models.error_messages import *
import threading

from data_mover import ALA_SERVICE, ALA_JOB_DAO


class DataMoverServices(XMLRPCView):
    """
    Contains methods that are callable from the XML RPC Interface
    See https://wiki.intersect.org.au/display/BCCVL/Data+Mover+and+Data+Movement+API
    """

    def __init__(self, context, request):
        XMLRPCView.__init__(self, context, request)
        self._ala_service = ALA_SERVICE
        self._ala_job_dao = ALA_JOB_DAO

    def pullOccurrenceFromALA(self, lsid=None):
        """
         XML RPC endpoint for pulling occurrence data from ALA for a given LSID of a species.
        """
        if lsid is None:
            return REJECTED(MISSING_PARAMS)
        else:
            job = self._ala_job_dao.create_new(lsid)

            thread_name = 'ala-get-' + lsid
            thread = threading.Thread(target=self._ala_service.worker, args=(job,), name=thread_name)
            thread.start()
            return {'id': job.id, 'status': job.status}

    def checkALAJobStatus(self, id=None):
        if id is None:
            return REJECTED(MISSING_PARAMS)

        if not isinstance(id, int):
            return REJECTED(INVALID_PARAMS)

        job = self._ala_job_dao.findById(id)

        if job is not None:
            response = {'id': id, 'status': job.status}
            return response
        else:
            return REJECTED(JOB_DOES_NOT_EXIST)