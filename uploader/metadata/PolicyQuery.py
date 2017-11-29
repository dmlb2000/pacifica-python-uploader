#!/usr/bin/python
"""This is the module for quering the Policy service."""
from __future__ import absolute_import
import json
import logging
from collections import namedtuple
from .Json import generate_namedtuple_encoder, generate_namedtuple_decoder
from .MetaData import metadata_encode
from ..common import CommonBase

LOGGER = logging.getLogger(__name__)
QUERY_KEYS = [
    'user',
    'columns',
    'from_table',
    'where'
]
PolicyQueryData = namedtuple('PolicyQueryData', QUERY_KEYS)
# Set the defaults to None for these attributes
PolicyQueryData.__new__.__defaults__ = (None,) * len(PolicyQueryData._fields)


class PolicyQuery(CommonBase):
    """
    Handle quering the policy server.

    This class handles quering the policy server and parsing the
    results.
    """

    pq_data = None
    user_id = None
    _proto = None
    _addr = None
    _port = None
    _uploader_path = None
    _ingest_path = None
    _uploader_url = None
    _ingest_url = None
    _auth = None

    def set_user(self, user):
        """Set the user for the current PolicyQuery."""
        try:
            self.user_id = int(user)
        except ValueError:
            id_check = PolicyQuery(
                user=-1,
                columns=['_id'],
                from_table='users',
                where={'network_id': user},
                auth=self._auth
            )
            self.user_id = id_check.get_results()[0]['_id']

    def get_user(self):
        """Get the user id."""
        return self.user_id

    def _set_url_from_parts(self):
        """Set the url from the parts in self."""
        for url_part in ['uploader', 'ingest']:
            if not getattr(self, '_{}_url'.format(url_part)):
                url_str = '{}://{}:{}{}'.format(
                    self._proto,
                    self._addr,
                    self._port,
                    getattr(self, '_{}_path'.format(url_part))
                )
                setattr(self, '_{}_url'.format(url_part), url_str)

    def __init__(self, user, *args, **kwargs):
        """Set the policy server url and define any data for the query."""
        self._server_url(
            [
                ('proto', 'http'),
                ('port', 8181),
                ('addr', '127.0.0.1'),
                ('uploader_path', '/uploader'),
                ('ingest_path', '/ingest'),
                ('uploader_url', None),
                ('ingest_url', None)
            ],
            'POLICY',
            kwargs
        )
        self._set_url_from_parts()
        self._setup_requests_session()
        self._auth = kwargs.pop('auth', {})
        LOGGER.debug('Policy URL %s auth %s', self._uploader_url, self._auth)
        # global sential value for userid
        if user != -1:
            self.set_user(user)
            self.pq_data = PolicyQueryData(user=self.get_user(), *args, **kwargs)
        else:
            self.pq_data = PolicyQueryData(user=-1, **kwargs)

    def tojson(self):
        """Export self to json."""
        return json.dumps(self.pq_data, cls=PolicyQueryDataEncoder)

    @staticmethod
    def fromjson(json_str):
        """Import json string to self."""
        pq_data = json.loads(json_str, cls=PolicyQueryDataDecoder)
        pq_dict = pq_data._asdict()
        user = pq_dict.pop('user', -1)
        return PolicyQuery(user, **pq_dict)

    def get_results(self):
        """Get results from the Policy server for the query."""
        headers = {'content-type': 'application/json'}
        LOGGER.debug('Policy Query Uploader %s', self.tojson())
        reply = self.session.post(self._uploader_url, headers=headers, data=self.tojson(), **self._auth)
        LOGGER.debug('Policy Result Uploader %s', reply.content)
        return reply.json()

    def valid_metadata(self, md_obj):
        """Check the metadata object against the ingest API."""
        headers = {'content-type': 'application/json'}
        LOGGER.debug('Policy Query Ingest %s', metadata_encode(md_obj))
        reply = self.session.post(self._ingest_url, headers=headers, data=metadata_encode(md_obj), **self._auth)
        LOGGER.debug('Policy Result Ingest %s', reply.content)
        return reply.json()


#####################################################################
# The from key in the json data is for the policy server.
# It's also a keyword in python so it needs to be handled correctly
#####################################################################
def _mangle_encode(obj):
    """Move the from_table to just from."""
    obj['from'] = obj.pop('from_table')


def _mangle_decode(**json_data):
    """Mangle the decode of the policy query object."""
    json_data['from_table'] = json_data.pop('from')
    return PolicyQueryData(**json_data)


PolicyQueryDataEncoder = generate_namedtuple_encoder(PolicyQueryData, _mangle_encode)
PolicyQueryDataDecoder = generate_namedtuple_decoder(_mangle_decode)
