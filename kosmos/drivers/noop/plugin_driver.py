from kosmos.drivers.plugin_driver import GslbAbstractDriver

__author__ = 'kugandhi'

class NoOpPluginDriver(GslbAbstractDriver):

    """
        This is the no op plugin driver that only logs the invocation and update the database..
    """
    def delete_member(self, context, member):
        pass

    def create_loadbalancer(self, context, loadbalancer):
        pass

    def delete_healthmonitor(self, context, healthmonitor):
        pass

    def delete_pooL_healthmonitor(self, context, pool_id, healthmonitor):
        pass

    def create_healthmonitor(self, context, healthmonitor):
        pass

    def delete_entity_status(self, context, entity):
        pass

    def delete_pool(self, context, pool):
        pass

    def create_pool_healthmonitor(self, context, pool_id, healthmonitor):
        pass

    def delete_loadbalancer(self, context, loadbalancer):
        pass

    def create_pool(self, context, pool):
        pass

    def update_entity_status(self, context, entity_id, state):
        pass

    def create_member(self, context, member):
        pass