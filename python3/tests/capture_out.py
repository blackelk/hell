from io import StringIO

from hell import Config

Config.OUT = StringIO()

def capture_out(fn):
    def wrapped(*args, **kwargs):
        pos = Config.OUT.tell()

        fn(*args, **kwargs)

        Config.OUT.seek(pos)

        return Config.OUT.read()

    return wrapped
