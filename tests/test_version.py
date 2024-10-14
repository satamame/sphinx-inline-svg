try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

import sphinx_inline_svg


def test_version():
    '''Test if extension version equals to project version
    '''
    with open("pyproject.toml", "rb") as f:
        proj_data = tomllib.load(f)
    proj_ver = proj_data["project"]["version"]
    assert sphinx_inline_svg.__version__ == proj_ver
