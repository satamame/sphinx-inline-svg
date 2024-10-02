import os
import re

from docutils import nodes
from lxml import html
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.nodes import make_refnode
from sphinx.writers.html import HTMLTranslator

__version__ = '0.1.1'

logger = logging.getLogger(__name__)

protocol_ptn = re.compile(r'[a-zA-Z]+://')


class svg(nodes.General, nodes.Element):
    '''Special svg node to replace .svg image node
    '''
    pass


def visit_svg_html(self: HTMLTranslator, node: nodes.Element):
    self.body.append(node['content'])


def depart_svg_html(self: HTMLTranslator, node: nodes.Element):
    # Closing tag already added to 'content' in visit_svg_html().
    pass


def setup(app: Sphinx):
    '''Set up extension
    '''
    # Add config parameters.
    app.add_config_value(
        'inline_svg_classes', ['inline-svg'], 'html', list[str])
    app.add_config_value(
        'inline_svg_del_attrs', ['content'], 'html', list[str])
    app.add_config_value(
        'inline_svg_resolve_xref', True, 'html', bool)

    # Add special 'svg' node definition.
    app.add_node(svg, html=(visit_svg_html, depart_svg_html))

    # Add process after doctree resolved.
    app.connect('doctree-resolved', process_svg_nodes)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


def process_svg_nodes(app: Sphinx, doctree: nodes.document, docname: str):
    '''Process after doctree resolved
    '''
    # This process is done only when target is html.
    if app.builder.name != 'html':
        return

    for node in doctree.traverse(nodes.image):
        if node['uri'].endswith('.svg'):
            svg_path = app.srcdir / node['uri']
            try:
                inline_svg(app, node, svg_path, docname)
            except Exception as e:
                # Just warn, continue building the document.
                logger.warning(f"Error inlining SVG {svg_path}: {e}")


def inline_svg(app, node, svg_path, docname):
    '''Replace img tag with inline svg read from svg_path
    '''
    # Check if node has any of 'inline_svg_classes'.
    # Inlining only nodes with any of the classes (extension's rule).
    for klass in node.attributes['classes']:
        if klass in app.config.inline_svg_classes:
            break
    else:
        # Skip if none of 'inline_svg_classes' found.
        return

    # Parse SVG file to get svg element.
    tree = html.parse(svg_path)
    svgs = tree.xpath('//svg')
    if not svgs:
        raise ValueError('No svg element.')
    root = svgs[0]

    # Remove namespaces in svg element.
    remove_namespaces(root)

    # Delete attributes from svg element.
    # Attributes are set as extension config param 'inline_svg_del_attrs'.
    for attr in app.config.inline_svg_del_attrs:
        if attr in root.attrib:
            del root.attrib[attr]

    # Add attributes from original node to svg element.
    for key, value in node.non_default_attributes().items():
        attr_key = 'class' if key == 'classes' else 'key'
        if isinstance(value, list):
            root.set(attr_key, ' '.join(value))
        elif isinstance(value, str):
            root.set(attr_key, value)

    # Resolve cross references in svg element.
    if app.config.inline_svg_resolve_xref:
        resolve_xref_thru_element(app, root, docname)

    # Create svg node, and replace image node with it.
    svg_content = html.tostring(root, encoding='unicode')
    svg_node = svg(content=svg_content)
    node.replace_self(svg_node)


def remove_namespaces(element):
    '''Remove namespaces from element and descendants
    '''
    # Remove relevant attrs from element.
    for attr in ['xmlns', 'xmlns:xlink']:
        if attr in element.attrib:
            del element.attrib[attr]

    # Change 'xlink:href' into 'href'.
    if 'xlink:href' in element.attrib:
        href = element.attrib['xlink:href']
        del element.attrib['xlink:href']
        element.set('href', href)

    # Apply it recursively.
    for child in element:
        remove_namespaces(child)


def resolve_xref_thru_element(app, element, docname):
    '''Resolve cross references in element and descendants
    '''
    env = app.builder.env

    # For all <a> tags with 'href' attribute
    for a_el in element.xpath('.//a[@href]'):
        resolved = resolve_uri(app, env, a_el, docname)
        if resolved:
            a_el.attrib['href'] = resolved


def resolve_uri(app, env, a_element, docname):
    '''Resolve href value of a_element if needed, otherwise return None
    '''
    href = a_element.get('href')
    text_node = nodes.Text(a_element.text)

    # Link to absolute URI - No need to resolve.
    if protocol_ptn.match(href):
        return None

    if href.startswith('#'):
        # Link to defined target.
        refnode = refnode_to_target(app, env, href[1:], text_node, docname)
    else:
        # Link to file path.
        refnode = refnode_to_file(app, env, href, text_node, docname)

    return refnode.attributes['refuri'] if refnode else None


def refnode_to_target(app, env, target, text_node, docname):
    '''Create refnode to defined target if needed, otherwise return None
    '''
    # target_defs is dict {target_name: (docname, target_id), ...}
    target_defs = env.get_domain('std').anonlabels

    for target_name, target_def in target_defs.items():
        if target == target_name:
            # Target is in the same page - No need to resolve.
            if docname == target_def[0]:
                return None

            ref_node = make_refnode(
                app.builder, docname, target_def[0], target_def[1], text_node)
            return ref_node

    # If no target to link.
    raise ValueError(f'Target not found: {target}')


def refnode_to_file(app, env, href, text_node, docname):
    '''Create refnode to file path if needed, otherwise return None
    '''
    if href.startswith('/'):
        # If starts with '/', treat as relative from doc root (working dir).
        target_path = href.lstrip('/')
    else:
        # Treat as relative from current file (referred via docname).
        current_dir = os.path.dirname(docname)
        target_path = os.path.normpath(os.path.join(current_dir, href))

    base, ext = os.path.splitext(target_path)
    suffix = env.config.source_suffix
    # suffix can be either str or list.
    suffix = [suffix] if isinstance(suffix, str) else suffix
    if ext in suffix:
        target_path = base + '.html'

    target_docname = target_path.replace(os.path.sep, '/')
    if target_docname.endswith('.html'):
        target_docname = target_docname[:-5]

    if target_docname in env.found_docs:
        ref_node = make_refnode(
            app.builder, docname, target_docname, '', text_node)
        return ref_node

    # If no file to link.
    raise ValueError(f'Document not found: {target_docname}')
