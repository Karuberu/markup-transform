import lxml.etree as xml
import mwparserfromhell as mw
from pathlib import Path
import sys

def parse(sourceXml):
    if sourceXml.tag != 'mediawiki':
        raise ValueError('Root element must be mediawiki')

    return convertChildrenToMarkup(sourceXml)

def convertXmlToMarkup(element):
    tag = element.tag
    if tag == 'argument':
        return argumentToMarkup(element)
    if tag == 'heading':
        return headingToMarkup(element)
    if tag == 'link':
        return externalLinkToMarkup(element)
    if tag == 'parameter':
        return parameterToMarkup(element)
    if tag == 'section':
        return sectionToMarkup(element)
    if tag == 'template':
        return templateToMarkup(element)
    if tag == 'tag':
        return tagToMarkup(element)
    if tag == 'title':
        return convertChildrenToMarkup(element)
    if tag == 'text':
        return textToMarkup(element)
    if tag == 'url':
        return convertChildrenToMarkup(element)
    if tag == 'wikilink':
        return wikilinkToMarkup(element)

    raise ValueError('Unhandled element ' + element.tag)

def convertChildrenToNodes(element, search = None):
    node = mw.parse('').nodes

    children = list(element) if search == None else element.findall(search)
    for child in children:
        markup = convertXmlToMarkup(child)
        node.append(markup)

    return node

def convertChildrenToMarkup(element, search = None):
    return nodesToMarkup(convertChildrenToNodes(element, search))

def nodesToMarkup(nodes):
    wikitext = mw.parse('')
    wikitext.nodes = nodes
    return str(wikitext)

def argumentToMarkup(element):
    name = element.get('name')
    default = convertChildrenToMarkup(element)
    return mw.nodes.argument.Argument(name, default)

def commentToMarkup(element):
    contents = convertChildrenToMarkup(element)
    return mw.nodes.comment.Comment(contents)

def externalLinkToMarkup(element):
    url = convertChildrenToMarkup(element, 'title')
    title = convertChildrenToMarkup(element, 'url')
    return mw.nodes.external_link.ExternalLink(url, title)

def headingToMarkup(element):
    level = int(element.get('level'))
    title = convertChildrenToMarkup(element)
    return mw.nodes.heading.Heading(title, level)

def htmlEntityToMarkup(node):
    value = element.text
    return mw.nodes.html_entity.HTMLEntity(value)

def parameterToMarkup(element):
    name = element.get('name')
    value = convertChildrenToMarkup(element)
    showKey = str(element.get('showkey')).lower() in ['true', 'none', '']
    return mw.nodes.extras.Parameter(name, value, showKey)

def sectionToMarkup(element):
    return convertChildrenToMarkup(element)

def templateToMarkup(element):
    name = element.get('name')
    params = convertChildrenToNodes(element)
    return mw.nodes.template.Template(name, params)

def tagToMarkup(element):
    text = element.text if element.text != None else ''
    return mw.nodes.text.Text(text)

def textToMarkup(element):
    text = element.text if element.text != None else ''
    return mw.nodes.text.Text(text)

def wikilinkToMarkup(element):
    title = convertChildrenToMarkup(element, 'title')
    text = convertChildrenToMarkup(element, 'text')
    return mw.nodes.wikilink.Wikilink(title, text)
