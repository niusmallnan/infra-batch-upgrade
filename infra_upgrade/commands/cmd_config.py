from __future__ import print_function

import click
import json

from infra_upgrade import config
from infra_upgrade.cli import pass_context


@click.command('config', short_help='rancher auth config')
@pass_context
def cli(ctx):
    cattle_url = click.prompt('Cattle URL',
                              default='http://192.168.99.100:8080')
    access_key = click.prompt('Access Key',
                              default='xxxxxxxxxxxxx')
    secret_key = click.prompt('Secret Key',
                              default='xxxxxxxxxxxxxxxxxx')
    conf = {'url':cattle_url, 'access_key':access_key, 'secret_key':secret_key}
    with open(config.CONF_FILE_PATH, 'w') as conf_file:
        conf_file.writelines(json.dumps(conf))
    print('Rancher auth config......')
