import abc

__author__ = 'kugandhi'

class GslbBackendPlugin(object):

    """
        An abstract backend class that defines a list of the methods to be implemented by the service layer.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_loadbalancer(self, context, loadbalancer):
        pass

    @abc.abstractmethod
    def delete_loadbalancer(self, context, loadbalancer):
        pass

    @abc.abstractmethod
    def get_loadbalancer(self, context, loadbalancer_id):
        pass

    @abc.abstractmethod
    def create_pool(self, context, pool):
        pass

    @abc.abstractmethod
    def delete_pool(self, context, pool_id):
        pass

    @abc.abstractmethod
    def create_healthmonitor(self, context, healthmonitor):
        pass

    @abc.abstractmethod
    def delete_healthmonitor(self, context, healthmonitor_id):
        pass

    @abc.abstractmethod
    def get_healthmonitor(self, context, healthmonitor_id):
        pass

    @abc.abstractmethod
    def create_member(self, context, member):
        pass

    @abc.abstractmethod
    def delete_member(self, context, member_id):
        pass

    def create_pool_healthmonitor(self,context, pool_id, healthmonitor):
        pass

    def delete_pooL_healthmonitor(self, context, pool_id, healthmonitor):
        pass


