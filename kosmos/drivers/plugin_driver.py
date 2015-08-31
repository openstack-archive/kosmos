import abc

__author__ = 'kugandhi'

class GslbAbstractDriver(object):

    """ This is an abstract driver that various gslb plugin drivers will have to extend and implement the methods.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_loadbalancer(self, context, loadbalancer):
        pass

    @abc.abstractmethod
    def delete_loadbalancer(self, context, loadbalancer):
        pass

    @abc.abstractmethod
    def create_pool(self, context, pool):
        pass

    @abc.abstractmethod
    def delete_pool(self, context, pool):
        pass

    @abc.abstractmethod
    def create_healthmonitor(self, context, healthmonitor):
        pass


    @abc.abstractmethod
    def delete_healthmonitor(self, context, healthmonitor):
        pass

    @abc.abstractmethod
    def create_member(self, context, member):
        pass

    @abc.abstractmethod
    def delete_member(self, context, member):
        pass

    @abc.abstractmethod
    def create_pool_healthmonitor(self,context, pool_id, healthmonitor):
        pass

    @abc.abstractmethod
    def delete_pooL_healthmonitor(self, context, pool_id, healthmonitor):
        pass

    @abc.abstractmethod
    def update_entity_status(self, context, entity_id, state):
        pass

    @abc.abstractmethod
    def delete_entity_status(self, context, entity):
        pass



