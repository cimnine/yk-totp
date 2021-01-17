import click

from click import echo

from .yk import getDevice, getController, validate

@click.group(name="totp")
@click.pass_context
def totp_group(ctx):
  pass

@totp_group.command()
@click.pass_context
def codes(ctx):
  pass
