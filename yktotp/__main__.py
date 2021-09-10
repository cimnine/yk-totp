import click

from click import echo, Command
from ykman import __version__ as YKMAN_VERSION

from .password import password_group
from .tool import TOOL_NAME, TOOL_VERSION, TOOL_PREFIX
from .totp import totp_group
from .yk import yubikey_group

SUBGROUPS: list[Command] = [password_group, totp_group, yubikey_group]


@click.group()
def cli() -> None:
  pass


@cli.command()
def version() -> None:
  """
  Shows version information.
  """
  echo(f"{TOOL_NAME} Version: {TOOL_VERSION}")
  echo(f"YubiKey Manager Version: {YKMAN_VERSION}")


for SUBGROUP in SUBGROUPS:
  cli.add_command(SUBGROUP)

if __name__ == '__main__':
  cli(auto_envvar_prefix=TOOL_PREFIX)
