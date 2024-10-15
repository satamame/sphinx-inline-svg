import shutil
from pathlib import Path

import pytest
from lxml import etree
from pytest_mock.plugin import MockerFixture
from sphinx.testing.util import SphinxTestApp


def test_no_svg_element(mocker: MockerFixture):
    '''Test warning log for no svg element in SVG file
    '''
    # Mock `html.parse` function to return a single empty root element.
    mock_html_parse = mocker.patch('sphinx_inline_svg.inline_svg.html.parse')
    mock_html_parse.return_value = etree.fromstring('<root></root>')

    project_dir = Path(__file__).parent.resolve() / 'proj_rest'
    app = SphinxTestApp(
        buildername='html',
        srcdir=project_dir / 'source',
        builddir=project_dir / 'build')
    shutil.rmtree(project_dir / 'build', ignore_errors=True)
    app.build()
    warnings = app._warning.getvalue()
    app.cleanup()

    assert 'No svg element.' in warnings


@pytest.mark.sphinx_config(inline_svg_classes=['undefined-target-svg'])
def test_link_to_undefined_target(sphinx_app):
    '''Test warning log for hyperlink to undefined target
    '''
    warnings = sphinx_app._warning.getvalue()
    assert 'Target not found: undefined-target' in warnings


@pytest.mark.sphinx_config(inline_svg_classes=['no-file-to-link-svg'])
def test_link_to_unexisting_file(sphinx_app):
    '''Test warning log for hyperlink to unexisting file
    '''
    warnings = sphinx_app._warning.getvalue()
    assert 'Document not found: unexisting.txt' in warnings
