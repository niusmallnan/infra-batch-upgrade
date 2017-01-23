from __future__ import print_function

import click

from infra_upgrade import config
from infra_upgrade.cli import pass_context


def get_external_id(stack, external_id):
    if external_id.startswith('catalog'):
        return external_id
    return config.LIBRARY_CATALOG_INFRA+external_id


@click.command('upgrade', short_help='run upgrade task')
@click.argument('stack_name', default='')
@click.option('--external-id', '-eid', default="")
@click.option('--docker-compose', '-dp', type=click.File('r'))
@click.option('--rancher-compose', '-rp', type=click.File('r'))
@pass_context
def cli(ctx, stack_name, external_id, docker_compose, rancher_compose):
    if len(stack_name) == 0:
        print("Pls use a specfic stack name")
        return
    client = config.get_global_client()
    stacks = client.list_environment(name=stack_name,
                                     state=config.STATE_ACTIVE)
    docker_cp = docker_compose.read()
    rancher_cp = rancher_compose.read()
    for stack in stacks:
        external_id = get_external_id(stack, external_id)
        print("Upgrade stack: %s, externalId: %s" %  ("1st"+stack.id[2:],
                                                      external_id))
        stack.upgrade(dockerCompose=docker_cp,
                      rancherCompose=rancher_cp,
                      externalId=external_id)

