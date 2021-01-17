import click

from click import echo, prompt
from click.exceptions import Abort
from keyring import get_password

from .tool import TOOL_NAME
from .lib import getDevices, getController

@click.group(name="yubikey")
def yubikey_group():
  """
  Information about connected YubiKeys.

  This module contains commands to show information about all YubiKeys
  discovered on this computer.
  """
  pass


@yubikey_group.command()
@click.option('-v', '--version', is_flag=True, help='Show the version of each YubiKey')
@click.option('-f', '--form-factor', is_flag=True, help='Show the form factor of each YubiKey')
@click.option('-p', '--password', is_flag=True, help='Show if a password is required or not for each YubiKey')
@click.option('-r', '--remembered-password', is_flag=True, help='Show if a password is remembered for each YubiKey')
@click.option('+P', '--require-password', is_flag=True, help='Show devices that require a password (and it is not known).')
@click.option('-P', '--require-no-password', is_flag=True, help="Show devices that don't require a password (or it is remembered).")
def list(version, form_factor, password, remembered_password, require_password, require_no_password):
  devices = getDevices()
  for device in devices:
    suffix = ""

    if version:
      v = device.version
      suffix += ", Version %d.%d.%d" % (v[0], v[1], v[2])

    if form_factor:
      suffix += ", %s" % device.form_factor

    serial = str(device.serial)

    password_remembered = get_password(TOOL_NAME, serial) != None
    if remembered_password:
      suffix += ", Password Remembered: %s" % (
          "yes" if password_remembered else "no")

    device_requires_password = None
    if password or require_password:
      controller = getController(device)
      device_requires_password = controller.locked

    if password:
      suffix += ", Password Required: %s" % (
        "yes" if device_requires_password else "no")

    if require_password != require_no_password:
      if require_password and device_requires_password and password_remembered:
        continue;
      if require_no_password and device_requires_password and not password_remembered:
        continue;

    echo(serial + suffix)
