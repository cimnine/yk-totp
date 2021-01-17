# yk-totp

![PyPI Version](https://img.shields.io/pypi/v/yk-totp?style=flat-square)
![PyPI License](https://img.shields.io/pypi/l/yk-totp?style=flat-square)
![PyPI Status](https://img.shields.io/pypi/status/yk-totp?style=flat-square)

`yk-totp` is a little CLI util for YubiKeys,
that will generate TOTP codes upon request.

The added benefit compared to [the official `ykman`][ykman] is that it offers
to store the password for unlocking your YubiKey in your system's keyring,
whereas `ykman` stores your password in it's config file.
(While the password is stored as `PBKDF2HMAC`-hash and not in plain-text,
this hash is all that is required to get to your 2FA,
yet this hash is not protected in anyway.)

This allows `yk-totp` to be used in other tools (like in an [Alfred Worflow][alred-wf])
which don't offer facilities to store or enter a password,
or where it's inconvenient to repeatedly enter the password.

## Requirements

This tool requires [Python 3][python] and an operating system that is supported by both,
[the `keyring` Python module][keyring] and by [the `ykman` tool from YubiCo][ykman].

## Installation

For now, the way to install `yk-totp` is via PIP:

```bash
pip3 install -U yk-totp
```

Use the same command to update to a new version.

### Error while installation

If you get errors while installing `yk-totp`, try this:

```bash
# Update the Python modules responsible for installing other modules
pip3 install -U pip wheel setuptools
```

Check [if you have `swig` installed][swig-installation],
which is apparently required to install `pyscard`,
which is a dependency of `ykman`:

```bash
# macOS with Homebrew
brew install swig

# Linux (apt)
sudo apt update && sudo apt install swig

# Linux (yum)
sudo yum install swig

# Windows with Chocolately
choco install swig
```

## Licensing and Copyright

This code is copyrighted.
But it can be used under the terms of the [MIT license](./LICENSE) for your own purposes.
It builds upon the following third party modules:

- [keyring][keyring] for the interaction with the operating system's keyring, which is MIT licensed.
- [yubikey-manager][ykman] for communicating with the YubiKey, which is licensed under a BSD-2-Clause License.
- [click][click] for the CLI interface, which is licensed under a BSD-3-Clause License.

Open source software rocks 🎸!

[ykman]: https://github.com/Yubico/yubikey-manager#readme
[alfred-wf]: https://www.alfredapp.com/help/workflows/
[python]: https://www.python.org
[keyring]: https://github.com/jaraco/keyring#readme
[click]: https://github.com/pallets/click#readme
[swig-installation]: http://www.swig.org/Doc4.0/Preface.html#Preface_installation
