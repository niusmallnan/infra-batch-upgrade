from __future__ import print_function

import click

from infra_upgrade import config
from infra_upgrade.cli import pass_context


@click.command('check', short_help='check stack state')
@click.argument('stack_name', default='')
@pass_context
def cli(ctx, stack_name):
    if len(stack_name) == 0:
        print("Pls use a specfic stack name")
        return
    client = config.get_global_client()
    for stack in client.list_environment(name=stack_name):
        print("Project: %s, state: %s" % (stack.accountId, stack.state))

