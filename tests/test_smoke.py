try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

import sphinx_inline_svg


def read_pyproject_toml():
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)


def test_version():
    '''Test if extension version equals to project version
    '''
    proj_data = read_pyproject_toml()
    proj_ver = proj_data["project"]["version"]
    assert sphinx_inline_svg.__version__ == proj_ver
