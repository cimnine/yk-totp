class PasswordError(Exception):
  pass


class WrongPasswordError(PasswordError):
  pass


class UndefinedPasswordError(PasswordError):
  pass


class UndefinedDevice(Exception):
  pass


class KeyNotFound(Exception):
  pass
