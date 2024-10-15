import pytest
from lxml import html


def test_link_to_top(sphinx_app):
    '''Test if hyperlink to document root is generated
    '''
    tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
    href = '../index.html'
    text = 'To Document root'
    xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
    elements = tree.xpath(xpath)
    assert len(elements) == 1


def test_link_relative(sphinx_app):
    '''Test if hyperlink to relative file is generated
    '''
    tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
    href = 'link_target.html'
    text = 'To Relative file'
    xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
    elements = tree.xpath(xpath)
    assert len(elements) == 1


def test_link_to_target(sphinx_app):
    '''Test if hyperlink to cross-reference target is generated
    '''
    tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
    href = 'link_target.html#target-1'
    text = 'To XRef target'
    xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
    elements = tree.xpath(xpath)
    assert len(elements) == 1


def test_link_to_google(sphinx_app):
    '''Test if hyperlink to absolute URL is generated
    '''
    tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
    href = 'https://google.com'
    text = 'To Absolute URL'
    xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
    elements = tree.xpath(xpath)
    assert len(elements) == 1


@pytest.mark.sphinx_config(inline_svg_classes=['custom-svg'])
def test_link_to_infile_target(sphinx_app):
    '''Test if hyperlink to in-file target is generated
    '''
    tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
    href = '#target-2'
    text = 'To in-file target'
    xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
    elements = tree.xpath(xpath)
    assert len(elements) == 1
