import shutil
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


def pytest_configure(config):
    '''Special function (hook) called by pytest
    '''
    # Define `sphinx_config` marker to overwrite config values.
    config.addinivalue_line(
        "markers",
        "sphinx_config(**kwargs): mark test to set specific config in conf.py"
    )


@pytest.fixture(params=['proj_rest', 'proj_myst'])
def sphinx_app(request):
    '''Provide a Sphinx instance for testing as fixture
    '''
    project_dir = Path(__file__).parent.resolve() / request.param

    # Get confoverrides from markers.
    confoverrides = {}
    for marker in request.node.iter_markers(name="sphinx_config"):
        confoverrides.update(marker.kwargs)

    app = SphinxTestApp(
        buildername='html',
        srcdir=project_dir / 'source',
        builddir=project_dir / 'build',  # See below.
        confoverrides=confoverrides)

    # Actual destination (build/html) is `sphinx_app.outdir` in test codes.

    # Clear build directory in advance.
    shutil.rmtree(project_dir / 'build', ignore_errors=True)

    app.build()
    yield app
    app.cleanup()
