import logging

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from zope.sqlalchemy import ZopeTransactionExtension
from redis import Redis
from rq import Queue

from data_mover.models import Base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

from data_mover.services.job_service import JobService
from data_mover.services.file_manager import FileManager

JOB_SERVICE = JobService()
BACKGROUND_QUEUE = Queue(connection=Redis())
FILE_MANAGER = FileManager()

from data_mover.services.data_mover_services import DataMoverServices


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    logger = logging.getLogger(__name__)
    logger.info('******************************')
    logger.info('Starting DataMover Pyramid App')
    logger.info('******************************')

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    FILE_MANAGER.configure(settings, 'file_manager.')

    config = Configurator(settings=settings)
    config.add_view(DataMoverServices, name='data_mover')
    config.scan()
    return config.make_wsgi_app()
