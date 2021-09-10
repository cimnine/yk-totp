# Development

## Dev Env

```bash
# Create venv
python3 -m venv .venv

# Load venv
source .venv/bin/activate
python3 -m pip install -U pip
pip3 install -Ur requirements.txt

# Install locally so that you can edit the code
pip3 install --editable .

# Test it
.venv/bin/yk-totp version
```

## Release

```bash
# Check that there are no git changes pending
git status

# Check Version
cat yktotp/tool.py | grep VERSION
cat setup.cfg | grep version

# Build egg locally
python3 setup.py sdist bdist_wheel

# Upload
python3 -m twine upload --repository pypi dist/*

# Git Tag
git tag x.y.z
git push --tags

# Update to next version
vim yktotp/tool.py setup.cfg
git commit -m "Prepare for next version" yktotp/tool.py setup.cfg
git push

# Clean Up
rm -rf dist build yk_totp.egg-info
```
