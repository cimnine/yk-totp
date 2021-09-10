from typing import Optional, Union, Tuple

import click
from click import echo, Context
from ykman import YkmanDevice
from yubikit.core.smartcard import ApduError
from yubikit.management import DeviceInfo
from yubikit.oath import OathSession, Credential, Code

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

    ctx.obj['device_info'] = device_info
    device, info = device_info
    device_serial = info.serial

    session = get_unlocked_session(device_info=device_info, password=password)
    ctx.obj['session'] = session
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
def codes(obj: dict[str, Union[OathSession, tuple[YkmanDevice, DeviceInfo]]], exact: Optional[bool], ignore_case: Optional[bool], query: Optional[str]):
  """
  Generates TOTP codes.

  This command generates all TOTP codes and lists them in alphabetical
  order.
  Optionally the list can be filtered by providing the QUERY argument.
  """
  session: OathSession = obj['session']
  device_info: tuple[YkmanDevice, DeviceInfo] = obj['device_info']
  _, info = device_info

  if session.has_key and session.locked:
    echo(f"The YubiKey {info.serial} is locked.")
    exit(1)

  try:
    totp_codes = session.calculate_all()
  except ApduError as err:
    echo(f"Unable to generate codes with YubiKey {info.serial}: {err}")
    exit(1)

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

  totp_codes_list: list[Tuple[Credential, Optional[Code]]] = list(totp_codes.items())
  totp_codes_list.sort(key=lambda t: t[0].issuer+t[0].name)
  for cc in totp_codes_list:
    cred, code = cc
    echo(f"{cred.issuer} ({cred.name}): {code.value}")


@totp_group.command(name='list')
@click.pass_obj
def list_credentials(obj: dict[str, OathSession]) -> None:
  """
  Lists all available credentials.

  This command returns all credentials that are stored in the chosen YubiKey
  in alphabetical order.
  """
  session = obj['session']

  credentials = session.list_credentials()
  credentials.sort()
  for cred in credentials:
    echo(f"{cred.issuer} ({cred.name})")
