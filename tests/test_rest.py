
import pytest
from lxml import html


# @pytest.mark.parametrize('sphinx_param', ['proj_rest', 'proj_myst'])
@pytest.mark.sphinx('proj_rest')
class TestNormal:
    def test_link_to_top(self, sphinx_app):
        '''Test if hyperlink to document root is generated
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        href = '../index.html'
        text = 'To Document root'
        xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
        elements = tree.xpath(xpath)
        assert len(elements) == 1

    def test_link_relative(self, sphinx_app):
        '''Test if hyperlink to relative file is generated
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        href = 'link_target.html'
        text = 'To Relative file'
        xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
        elements = tree.xpath(xpath)
        assert len(elements) == 1

    def test_link_to_target(self, sphinx_app):
        '''Test if hyperlink to cross-reference target is generated
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        href = 'link_target.html#target-1'
        text = 'To XRef target'
        xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
        elements = tree.xpath(xpath)
        assert len(elements) == 1

    def test_link_to_google(self, sphinx_app):
        '''Test if hyperlink to absolute URL is generated
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        href = 'https://google.com'
        text = 'To Absolute URL'
        xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
        elements = tree.xpath(xpath)
        assert len(elements) == 1
