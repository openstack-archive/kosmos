import base

__author__ = 'kugandhi'

class GslbManager(base.GslbBackendPlugin):

    """
        The Gslb Manager is the entry point to the service layer that orchestrates the following:
         * Loads the appropriate Gslb driver as per the configuration.
         * Manages the database entries for all API calls.
         * Invokes the appropriate driver method for the operation.
    """

    def __init__(self):
        pass

    def delete_member(self, context, member_id):
        pass

    def create_loadbalancer(self, context, loadbalancer):
        pass

    def delete_pooL_healthmonitor(self, context, pool_id, healthmonitor):
        pass

    def delete_healthmonitor(self, context, healthmonitor_id):
        pass

    def create_healthmonitor(self, context, healthmonitor):
        pass

    def get_healthmonitor(self, context, healthmonitor_id):
        pass

    def delete_pool(self, context, pool_id):
        pass

    def create_pool_healthmonitor(self, context, pool_id, healthmonitor):
        pass

    def delete_loadbalancer(self, context, loadbalancer):
        pass

    def create_pool(self, context, pool):
        pass

    def create_member(self, context, member):
        pass

    def get_loadbalancer(self, context, loadbalancer_id):
        pass

