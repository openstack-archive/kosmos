import abc
from kosmos.backend import base as backend_base
__author__ = 'kugandhi'

class Storage(backend_base.GslbBackendPlugin):

    """
        This abstract class is for the storage engine to manage the entities in the local db.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def find_pool(self, context, criterion=None):
        pass


