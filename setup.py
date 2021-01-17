from yktotp.tool import TOOL_VERSION
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
  long_description = fh.read()

setup(
  version=TOOL_VERSION,
  long_description=long_description,
)
