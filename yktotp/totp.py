from typing import Optional

import click
from click import echo, Context
from yubikit.oath import OathSession

from .error import KeyNotFound, UndefinedDevice, WrongPasswordError, UndefinedPasswordError
from .lib import get_unlocked_session, get_device


@click.group(name="totp")
@click.option('-d', '--device-serial', type=int, required=False, help="Ony get TOTP from this device.")
@click.option('-p', '--password', required=False, help="Provide the password for the device.")
@click.pass_context
def totp_group(ctx: Context, device_serial: Optional[str], password: Optional[str]) -> None:
  """
  Commands to generate TOTP codes.

  This module is used to actually generate and display TOTP codes.
  """
  ctx.ensure_object(dict)

  try:
    device_info = get_device(device_serial)
    if not device_info:
      echo(f"No YubiKeys detected.")
      exit(0)

    device, info = device_info
    device_serial = info.serial

    ctx.obj['session'] = get_unlocked_session(device_info=device_info, password=password)
  except KeyNotFound:
    echo(f"Could not find YubiKey '{device_serial}'.")
    exit(1)
  except UndefinedPasswordError:
    echo(f"The YubiKey '{device_serial}' requires a password, but none was given.")
    exit(1)
  except WrongPasswordError:
    echo(f"The given or remembered password could not be validated for YubiKey '{device_serial}', " +
         "please check the password.")
    exit(1)
  except UndefinedDevice:
    if device_serial:
      echo(f"No YubiKey discovered that matches '{device_serial}'.")
    else:
      echo("No YubiKey discovered.")
    exit(1)


@totp_group.command()
@click.option('-e', '--exact', flag_value=True, help="Only return values that match exactly.")
@click.option('+i/-i', '--ignore-case/--no-ignore-case', help="Whether to ignore casing when filtering.")
@click.argument('query', required=False, type=str)
@click.pass_obj
def codes(obj: dict[str, OathSession], exact: Optional[bool], ignore_case: Optional[bool], query: Optional[str]):
  """
  Generates TOTP codes.

  This command generates all TOTP codes and lists them in alphabetical
  order.
  Optionally the list can be filtered by providing the QUERY argument.
  """
  session = obj['session']

  totp_codes = session.calculate_all()

  if query:
    if not exact and ignore_case:
      totp_codes = [(cred, totp_code)
                    for (cred, totp_code)
                    in totp_codes
                    if query.lower() in cred.printable_key.lower()]
    if not exact and not ignore_case:
      totp_codes = [(cred, totp_code)
                    for (cred, totp_code)
                    in totp_codes
                    if query in cred.printable_key]
    if exact and ignore_case:
      totp_codes = [(cred, totp_code)
                    for (cred, totp_code)
                    in totp_codes
                    if query.lower() == cred.printable_key.lower()]
    if exact and not ignore_case:
      totp_codes = [(cred, totp_code)
                    for (cred, totp_code)
                    in totp_codes
                    if query == cred.printable_key]

  totp_codes_list = list(totp_codes.items())
  totp_codes_list.sort(key=lambda t: t[0].name)
  for (cred, code) in totp_codes_list:
    echo(f"{cred.name}: {code.value}")


@totp_group.command(name='list')
@click.pass_obj
def list_credentials(obj: dict[str, OathSession]) -> None:
  """
  Lists all available credentials.

  This command returns all credentials that are stored in the chosen YubiKey
  in alphabetical order.
  """
  session = obj['session']

  credentials = [cred.name for cred in session.list_credentials()]
  credentials.sort()
  for cred in credentials:
    echo(str(cred))
