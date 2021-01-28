import click

from click import echo

from .lib import getUnlockedController, getDevice
from .error import KeyNotFound, UndefinedDevice, WrongPasswordError, UndefinedPasswordError

@click.group(name="totp")
@click.option('-d', '--device-serial', type=int, required=False, help="Ony get TOTP from this device.")
@click.option('-p', '--password', required=False, help="Provide the password for the device.")
@click.pass_context
def totp_group(ctx, device_serial, password):
  """
  Commands to generate TOTP codes.

  This module is used to actually generate and display TOTP codes.
  """
  ctx.ensure_object(dict)

  try:
    device = getDevice(device_serial)
    device_serial = device.serial

    ctx.obj['controller'] = getUnlockedController(device=device, password=password)
  except KeyNotFound:
    echo(f"Could not find YubiKey '{device_serial}'.")
    exit(1)
  except UndefinedPasswordError:
    echo(f"The YubiKey '{device_serial}' requires a password, but none was given.")
    exit(1)
  except WrongPasswordError:
    echo(f"The given or remembered password could not be validated for YubiKey '{device_serial}', please check the password.")
    exit(1)
  except UndefinedDevice:
    if device_serial:
      echo(f"No YubiKey discovered that matches '{device_serial}'.")
    else:
      echo("No YubiKey discovered.")
    exit(1)

@totp_group.command()
@click.option('-e', '--exact', flag_value=True, help="Only return values that match exactly.")
@click.option('+i/-i', '--ignore-case/--no-ignore-case', help="Wether to ignore casing when filtering.")
@click.argument('query', required=False, type=str)
@click.pass_obj
def codes(obj, exact, ignore_case, query):
  """
  Generates TOTP codes.

  This command generates all TOTP codes and lists them in alphabetical
  order.
  Optionally the list can be filtered by providing the QUERY argument.
  """
  controller = obj['controller']

  codes = controller.calculate_all()

  if query:
    if not exact and ignore_case:
      codes = [ (cred, code)
                for (cred, code)
                in codes
                if query.lower() in cred.printable_key.lower() ]
    if not exact and not ignore_case:
      codes = [ (cred, code)
                for (cred, code)
                in codes
                if query in cred.printable_key ]
    if exact and ignore_case:
      codes = [(cred, code)
              for (cred, code)
              in codes
              if query.lower() == cred.printable_key.lower()]
    if exact and not ignore_case:
      codes = [(cred, code)
              for (cred, code)
              in codes
              if query == cred.printable_key]

  codes.sort(key=lambda x: x[0].printable_key)
  for (cred, code) in codes:
    echo(f"{cred.printable_key}: {code.value}")

@totp_group.command()
@click.pass_obj
def list(obj):
  """
  Lists all available credentials.

  This command returns all credentials that are stored in the chosen YubiKey
  in alphabetical order.
  """
  controller = obj['controller']

  credentials = [ cred.printable_key for cred in controller.list() ]
  credentials.sort()
  for cred in credentials:
    echo(str(cred))
