__author__ = 'kugandhi'

import flask
import kosmos.schema as schema

blueprint = flask.Blueprint('loadbalancers', __name__)
domain_schema = schema.Schema('v1', 'loadbalancers')


@blueprint.route('/loadbalancers', methods=['POST'])
def create_loadbalancers():
    pass

@blueprint.route('/loadbalancers/<loadbalancer_id>', methods=['GET'])
def get_loadbalancers(loadbalancer_id):
    pass

@blueprint.route('/loadbalancers/<loadbalancer_id>', methods=['DELETE'])
def delete_loadbalancer(loadbalancer_id):
    pass




