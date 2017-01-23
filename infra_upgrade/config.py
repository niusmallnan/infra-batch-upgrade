from __future__ import print_function

import os
import gdapi
import json


STATE_ACTIVE = 'active'
STATE_UPGRADED = 'upgraded'

LIBRARY_CATALOG_INFRA = 'catalog://library:infra*'

CONF_FILE_PATH = os.environ['HOME']+'/.infra_upgrade.conf'


class CattleClient(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(CattleClient, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            return cls._instance

    def __init__(self):
        with open(CONF_FILE_PATH, 'r') as conf_file:
            conf = json.loads(conf_file.read())
            self.url = conf['url']
            self.access_key = conf['access_key']
            self.secret_key = conf['secret_key']


    def global_client(self):
        return gdapi.Client(url=self.url,
                            access_key=self.access_key,
                            secret_key=self.secret_key)


def get_global_client():
    return CattleClient().global_client()
