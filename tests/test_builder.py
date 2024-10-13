import shutil
from pathlib import Path

from sphinx.testing.util import SphinxTestApp


def test_builder(mocker):
    '''Test if inline_svg is not called when builder is not html
    '''
    mock_inline_svg = mocker.patch('sphinx_inline_svg.inline_svg.inline_svg')
    project_dir = Path(__file__).parent.resolve() / 'proj_rest'
    app = SphinxTestApp(
        buildername='text',
        srcdir=project_dir / 'source',
        builddir=project_dir / 'build')
    shutil.rmtree(project_dir / 'build', ignore_errors=True)

    app.build()
    app.cleanup()

    assert not mock_inline_svg.called
