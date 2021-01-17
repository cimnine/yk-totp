# yk-totp

`yk-totp` is a little CLI util for YubiKeys,
that will generate TOTP codes upon request.

The added benefit compared to [the official `ykman`][ykman] is that it offers
to store the password for unlocking your YubiKey in your system's keyring,
whereas `ykman` stores your password in it's config file.
(While the password is stored as `PBKDF2HMAC`-hash and not in plain-text,
this hash is all that is required to get to your 2FA
but this hash is not protected in anyway.)

This allows `yk-totp` to be used in other tools (like in an [Alfred Worflow][alred-wf])
which don't offer facilities to store or enter a password,
or where it's inconvenient to repeatedly enter the password.

## Requirements

This tool requires [_Python 3_][python] and an operating system that is supported by [the `keyring` Python module][keyring].

## Installation

For now, the way to install `yk-totp` is via PIP:

```bash
pip install yk-totp
```

## Licensing and Copyright

This code is copyrighted.
But it can be used under the terms of the [MIT license](./License) for your own purposes.
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
