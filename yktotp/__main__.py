import click
from click import Command
from ykman import __version__ as YKMAN_VERSION

from .password import password_group
from .tool import TOOL_PREFIX
from .totp import totp_group
from .yk import yubikey_group

SUBGROUPS: list[Command] = [password_group, totp_group, yubikey_group]


@click.group()
@click.version_option(
  message="%(prog)s Version %(version)s\n" + f"YubiKey Manager Version: {YKMAN_VERSION}",
  package_name="yk-totp"
)
def cli() -> None:
  pass


for SUBGROUP in SUBGROUPS:
  cli.add_command(SUBGROUP)

if __name__ == '__main__':
  cli(auto_envvar_prefix=TOOL_PREFIX)
