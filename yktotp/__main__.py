import click

from click import echo
from ykman import __version__ as YKMAN_VERSION

from .tool import TOOL_NAME, TOOL_VERSION
from .password import password_group


@click.group()
def cli():
  pass

SUBGROUPS=[password_group]

for SUBGROUP in SUBGROUPS:
  cli.add_command(SUBGROUP)

@cli.command()
def version():
  """
  Shows version information.
  """
  echo("%s Version: %s" % (TOOL_NAME, TOOL_VERSION))
  echo("YubiKey Manager Version: %s" % YKMAN_VERSION)

if __name__ == '__main__':
  cli()
