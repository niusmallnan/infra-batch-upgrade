from __future__ import print_function

import os
import sys
import click
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client


class Context(object):

    def __init__(self):
        self.verbose = False
        self.host = os.getcwd()

    def log(self, msg, *args):
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'commands'))


class InfraUpgradeCLI(click.MultiCommand):

    def _import_mod(self, module):
        return __import__(module, None, None, ['cli'])

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                temp = filename[4:-3]
                mod = self._import_mod('infra_upgrade.commands.cmd_'+temp)
                try:
                    command_name = mod.__command_name__
                except AttributeError:
                    command_name = temp
                rv.append(command_name)
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            name = name.replace('-', '_')
            mod = self._import_mod('infra_upgrade.commands.cmd_' + name)

        except ImportError:
            return
        return mod.cli


@click.command(cls=InfraUpgradeCLI)
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    """A tool for upgrade infrastructure services on Rancher"""
    if verbose:
        http_client.HTTPConnection.debuglevel = 1
    ctx.verbose = verbose
