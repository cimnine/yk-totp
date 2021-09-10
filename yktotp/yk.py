import click
from click import echo
from keyring import get_password

from .lib import list_all_devices, get_session
from .tool import TOOL_NAME


@click.group(name="yubikey")
def yubikey_group() -> None:
  """
  Information about connected YubiKeys.

  This module contains commands to show information about all YubiKeys
  discovered on this computer.
  """
  pass


@yubikey_group.command(name="list")
@click.option('-v', '--version', is_flag=True,
              help='Show the version of each YubiKey')
@click.option('-f', '--form-factor', is_flag=True,
              help='Show the form factor of each YubiKey')
@click.option('-p', '--password', is_flag=True,
              help='Show if a password is required or not for each YubiKey')
@click.option('-r', '--remembered-password', is_flag=True,
              help='Show if a password is remembered for each YubiKey')
@click.option('+P', '--require-password', is_flag=True,
              help='Show devices that require a password (and it is not known).')
@click.option('-P', '--require-no-password', is_flag=True,
              help="Show devices that don't require a password (or it is remembered).")
def list_devices(version, form_factor, password, remembered_password, require_password, require_no_password) -> None:
  devices = list_all_devices()
  for device_info in devices:
    device, info = device_info
    suffix = ""

    if version:
      suffix += ", Version "
      v = info.version
      if v:
        suffix += f" {v[0]}.{v[1]}.{v[2]}"
      else:
        suffix += " unknow"

    if form_factor:
      suffix += f", {info.form_factor}"

    serial = str(info.serial)

    password_remembered = get_password(TOOL_NAME, serial) is not None
    if remembered_password:
      suffix += ", Password Remembered: "
      suffix += "yes" if password_remembered else "no"

    device_requires_password = None
    if password or require_password:
      session = get_session(device_info)
      device_requires_password = session.locked

    if password:
      suffix += ", Password Required: "
      suffix += "yes" if device_requires_password else "no"

    if require_password != require_no_password:
      if require_password and device_requires_password and password_remembered:
        continue
      if require_no_password and device_requires_password and not password_remembered:
        continue

    echo(serial + suffix)
