from flask.ext import restful
from . import database
from flask import abort, request
from datetime import datetime
import pytz

class PeerInstance (restful.Resource):

    def get(self, id):
        peers = db.meta.load_pickle('peers')
        if id in peers.keys():
            peer = peers[id]
            peer = {
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            }
            return peer
        else:
            abort(404)

    def delete(self, id):
        peers = db.meta.load_pickle('peers')
        if id in peers.keys():
            db.remove_peer(id)
        else:
            abort(404)


class PeerResource(restful.Resource):

    def get(self):
        peers = [
            {
                'id': peer['id'],
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            } for peer in database.get_peers()
        ]

        return {'peers': peers}

    def post(self):

        address = request.form.get('address')
        port = request.form.get('port')
        hostname = request.form.get('hostname')
        last_seen = request.form.get('last_seen')

        if not address or not port or not hostname or not last_seen:

            abort(400)

        last_seen = datetime.strptime(last_seen, '%Y-%m-%d %H:%M:%S')
        last_seen = pytz.utc.localize(last_seen)

        peer = {
            'address': address,
            'port': port,
            'hostname': hostname,
            'last_seen': last_seen
        }

        database.add_peer(peer)

        peers = [
            {
                'id': peer['id'],
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            } for peer in database.get_peers()
        ]

        return {'peers': peers}
