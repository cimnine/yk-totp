from typing import Optional

import keyring
from click import echo, prompt
from click.exceptions import Abort
from ykman.base import YkmanDevice
from ykman.device import list_all_devices
from yubikit.core.smartcard import SmartCardConnection
from yubikit.management import DeviceInfo
from yubikit.oath import OathSession

from .error import WrongPasswordError, UndefinedPasswordError, KeyNotFound, UndefinedDevice
from .tool import TOOL_NAME


def get_device(serial=None) -> Optional[tuple[YkmanDevice, DeviceInfo]]:
  devices = list_all_devices()

  if len(devices) == 0:
    return None

  if serial:
    found_device = [device_info for device_info in devices if device_info[1].serial == serial]
    if len(found_device) == 1:
      return found_device[0]
    raise KeyNotFound

  selected_device_index = 0
  if len(devices) > 1:
    for device_index in range(len(devices)):
      _, device_info = devices[device_index]
      echo(f"{device_index + 1}   {device_info.serial}")

    while True:
      try:
        selected_device_index = -1 + \
                                int(prompt("Select device: ", default=1, type=int))
        if 0 <= selected_device_index < len(devices):
          break
      except Abort:
        exit(1)
      except ValueError:
        continue

  return devices[selected_device_index]


def get_session(device_info: tuple[YkmanDevice, DeviceInfo] = None) -> OathSession:
  if device_info is None:
    device_info = get_device()

  device, _ = device_info
  connection = device.open_connection(SmartCardConnection)
  return OathSession(connection=connection)


def get_unlocked_session(device_info: Optional[tuple[YkmanDevice, DeviceInfo]] = None,
                         password: Optional[str] = None) -> OathSession:
  if device_info is None:
    device_info = get_device()
  if device_info is None:
    raise UndefinedDevice

  device, info = device_info
  connection = device.open_connection(SmartCardConnection)
  session = OathSession(connection=connection)
  if not session.locked:
    return session

  if not password:
    password = get_password(info)
  if not password:
    try:
      password = prompt(f"Password for YubiKey '{info.serial}'", hide_input=True, type=str, err=True)
    except Abort:
      raise UndefinedPasswordError

  try:
    key = session.derive_key(password=password)
    session.validate(key=key)
  except Exception:
    raise WrongPasswordError

  return session


def get_password(device: DeviceInfo) -> Optional[str]:
  return keyring.get_password(TOOL_NAME, str(device.serial))


def validate(password: str, session: OathSession = None,
             device_info: Optional[tuple[YkmanDevice, DeviceInfo]] = None) -> None:
  if session is None:
    session = get_session(device_info)

  key = session.derive_key(password)
  try:
    session.validate(key)
    return
  except Exception:
    raise WrongPasswordError
