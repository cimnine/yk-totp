from click import echo, prompt
from click.exceptions import Abort
from ykman.descriptor import list_devices
from ykman.oath import OathController
from ykman.util import TRANSPORT

from .error import PasswordError, KeyNotFound

def getDevices():
  return list_devices(transports=TRANSPORT.CCID)


def getDevice(serial=None):
  devices = list(getDevices())

  if len(devices) == 0:
    return None

  if serial:
    foundDevice = [ device for device in devices if device.serial == serial ]
    if len(foundDevice) == 1:
      return foundDevice[0]
    raise KeyNotFound

  selectedDeviceIndex = 0
  if len(devices) > 1:
    for deviceIndex in range(len(devices)):
      echo("%d   %s" % (deviceIndex+1, devices[deviceIndex]))

    while True:
      try:
        selectedDeviceIndex = -1 + \
            int(prompt("Select device: ", default=1, type=int))
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
