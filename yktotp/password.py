import click
import keyring

from click import echo
from click.exceptions import Abort

from .error import WrongPasswordError, KeyNotFound
from .tool import TOOL_NAME
from .lib import getDevice, getController, validate

@click.group(name="password")
@click.option('-d', '--device-serial', type=int, required=False, help="Set the password for this device.")
@click.pass_context
def password_group(ctx, device_serial):
  """
  Provides commands for storing your password.

  This can be useful if you would like to not enter your
  password repeatedly.
  """
  ctx.ensure_object(dict)
  try:
    ctx.obj['device'] = getDevice(device_serial)
  except KeyNotFound:
    echo(f"The YubiKey '{device_serial}' is not connected right now.")
    exit(1)


@password_group.command()
@click.pass_context
def remember(ctx):
  """
  Asks for a password and remembers it.

  If multiple YubiKeys are connected, then it will ask to select
  a YubiKey first.
  Then you will need to enter the corresponding password.
  If the password is correct, it is stored to the system's keyring.
  """
  device = ctx.obj['device']
  controller = getController(device)

  yk_serial = device.serial

  if not controller.locked:
    echo(f"The YubiKey '{yk_serial}' is not password protected.")
    exit(1)

  while True:
    try:
      password = click.prompt(f"Password for YubiKey '{yk_serial}'", hide_input=True, err=True)
      validate(password, controller)
      break
    except Abort:
      exit(1)
    except WrongPasswordError:
      echo("Could not validate password, possibly wrong password. Try again.")
      continue

  keyring.set_password(TOOL_NAME, str(yk_serial), password)
  keyring_name = keyring.get_keyring().name
  echo(f"The password was stored in {keyring_name}.")


@password_group.command()
@click.pass_context
def forget(ctx):
  """
  Forgets the stored password.

  If there is one YubiKey connected, it will forget the password,
  that is stored for this YubiKey.
  If multiple YubiKeys are connected, then it will ask to select
  a YubiKey first.
  """

  yk_serial = ctx.obj['device'].serial
  try:
    keyring.delete_password(TOOL_NAME, str(yk_serial))
  except keyring.errors.PasswordDeleteError:
    pass
