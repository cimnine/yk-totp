# Development

## Dev Env

```bash
# Load venv
source .venv/bin/active

# Install locally so that you can edit the code
pip install --editable .

# Test it
.venv/bin/yk-totp version
```

## Release

```bash
# Check that there are no git changes pending
git status

# Check Version
cat yktotp/tool.py | grep VERSION

# Build egg locally
python3 setup.py sdist bdist_wheel

# Upload
python3 -m twine upload --repository pypi dist/*

# Git Tag
git tag x.y.z
git push --tags

# Update to next version
vim yktotp/tool.py
git commit -m "Prepare for next version" yktotp/tool.py
git push

# Clean Up
rm -rf dist build yk_totp.egg-info
```
