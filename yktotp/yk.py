import click

from click import echo, prompt
from click.exceptions import Abort

from ykman.descriptor import list_devices
from ykman.util import TRANSPORT
from ykman.oath import OathController

from .error import PasswordError

@click.group(name="yubikey")
def yubikey_group():
  pass

@yubikey_group.command()
@click.option('-v', '--version', is_flag=True, help='Show the version of each YubiKey')
@click.option('-f', '--form-factor', is_flag=True, help='Show the form factor of each YubiKey')
def list(version, form_factor):
  devices = list_devices(transports=TRANSPORT.CCID)
  for device in devices:
    suffix = ""

    if version:
      suffix += ", Version %d.%d.%d" % (device.version[0], device.version[1], device.version[2])

    if form_factor:
      suffix += ", %s" % device.form_factor

    echo(str(device.serial) + suffix)

def getDevice():
  devices = list(list_devices(transports=TRANSPORT.CCID))

  if len(devices) == 0:
    echo("No YubiKey discovered.")
    exit(1)

  selectedDeviceIndex = 0
  if len(devices) > 1:
    for deviceIndex in range(len(devices)):
      echo("%d   %s" % (deviceIndex+1, devices[deviceIndex]))

    while True:
      try:
        selectedDeviceIndex = -1 + int(prompt("Select device: ", default=1, type=int))
        if selectedDeviceIndex >= 0 and selectedDeviceIndex < len(devices):
          break
      except Abort:
        exit(1)
      except ValueError:
        continue

  return devices[selectedDeviceIndex]

def getController(device=None):
  if device is None:
    device = getDevice()

  return OathController(device.driver)

def validate(password, controller=None, device=None):
  if controller is None:
    controller = getController(device)

  key = controller.derive_key(password)
  try:
    controller.validate(key)
    return
  except Exception:
    raise PasswordError
