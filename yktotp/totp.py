import click

from click import echo

from .lib import getDevice
from .error import KeyNotFound

@click.group(name="totp")
@click.option('-d', '--device-serial', type=int, required=False, help="Ony get TOTP from this device.")
@click.pass_context
def totp_group(ctx, device_serial):
  ctx.ensure_object(dict)

  try:
    device = getDevice(device_serial)

    if not device:
      echo("No YubiKey discovered.")
      exit(1)

    ctx.obj['device'] = device
  except KeyNotFound:
    echo("Could not find YubiKey '%d'." % device_serial)

@totp_group.command()
@click.pass_context
def codes(ctx):
  pass
