from pyramid_xmlrpc import XMLRPCView
from data_mover.models import *

class DataMoverServices(XMLRPCView):

    def move(self, destination_args, source_args):

        type = source_args['type']
        data_id = source_args['id']
        destination = destination_args['host']

        # TODO: Perform validation on the inputs and return early on error

        # TODO: Query the dataset manager to obtain the source details of the file requested - should probably be persisted along with the job
        # TODO: return early if the file can't be found.

        # create a new job
        job = Job(type, data_id, destination)

        DBSession.add(job)
        DBSession.flush()


        #put into job queue so it can be moved

        #create the response
        response = {'id': job.id, 'status': job.status}
        return response

    def check(self, id):
        job = DBSession.query(Job).get(id)
        response = {'id': job.id, 'status': job.status}
        return response