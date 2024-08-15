"""
Utility functions for reading and writing toml files.

Handles module imports for all supported versions (in a build root or on a host).
"""
try:
    import tomllib as toml  # stdlib since 3.11 (read-only)
    tomlw = None
except ModuleNotFoundError:
    import tomli as toml  # EL9+
    tomlw = None
except ModuleNotFoundError:
    import toml  # older unmaintained lib, needed for backwards compatibility with existing EL9 and Fedora manifests
    tomlw = toml
except ModuleNotFoundError:
    import pytoml as toml  # EL8
    tomlw = toml

# import writer if we don't have one already
if tomlw is None:
    try:
        import tomli_w as tomlw  # EL9+
    except ModuleNotFoundError:
        # no write module available
        tomlw = None


def load(*args, **kwargs):
    return toml.load(*args, **kwargs)


def dump(*args, **kwargs):
    if tomlw is None:
        raise RuntimeError("no toml module available with write support")

    tomlw.dump(*args, **kwargs)
