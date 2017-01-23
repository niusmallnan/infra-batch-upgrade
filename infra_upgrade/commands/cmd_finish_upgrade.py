from __future__ import print_function

import click

from infra_upgrade import config
from infra_upgrade.cli import pass_context


@click.command('finish-upgrade', short_help='finish upgrade task')
@click.argument('stack_name', default='')
@pass_context
def cli(ctx, stack_name):
    if len(stack_name) == 0:
        print("Pls use a specfic stack name")
        return
    client = config.get_global_client()
    stacks = client.list_environment(name=stack_name,
                                     state=config.STATE_UPGRADED)
    for stack in stacks:
        print("Finish upgrade stack: %s ......" % "1st"+stack.id[2:])
        stack.finishupgrade()


__command_name__ = 'finish-upgrade'
