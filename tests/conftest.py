import shutil
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# For the marker @pytest.mark.sphinx
pytest_plugins = ('sphinx.testing.fixtures',)


@pytest.fixture(scope='session', params=['proj_rest'])
def sphinx_app(request):
    '''Provide a Sphinx instance for testing as fixture

    scope='session' creates the instance once during a test run
    for each of 'proj_rest' and 'proj_myst'.
    @pytest.mark.sphinx() marker decides which instance to use.
    '''
    project_dir = Path(__file__).parent.resolve() / request.param

    # Get confoverrides from marker.
    marker = request.node.get_closest_marker('sphinx')
    confoverrides = marker.kwargs.get('confoverrides', {}) if marker else {}

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
