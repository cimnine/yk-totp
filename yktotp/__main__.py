import click

from click import echo
from ykman import __version__ as YKMAN_VERSION

from .password import password_group
from .tool import TOOL_NAME, TOOL_VERSION, TOOL_PREFIX
from .totp import totp_group
from .yk import yubikey_group

SUBGROUPS = [password_group, totp_group, yubikey_group]

@click.group()
def cli():
  pass

@cli.command()
def version():
  """
  Shows version information.
  """
  echo("%s Version: %s" % (TOOL_NAME, TOOL_VERSION))
  echo("YubiKey Manager Version: %s" % YKMAN_VERSION)


for SUBGROUP in SUBGROUPS:
  cli.add_command(SUBGROUP)

if __name__ == '__main__':
  cli(auto_envvar_prefix=TOOL_PREFIX)
