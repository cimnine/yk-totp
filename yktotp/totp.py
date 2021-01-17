import click

from click import echo

from .lib import getDevice

@click.group(name="totp")
@click.option('-d', '--device', required=False, help="Ony get TOTP from this device.")
@click.pass_context
def totp_group(ctx):
  ctx.ensure_object(dict)
  ctx.obj['device'] = getDevice()
  pass

@totp_group.command()
@click.pass_context
def codes(ctx):
  pass
