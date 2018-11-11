import lxml.etree as xml
import mwparserfromhell as mw
from pathlib import Path
import sys

def parse(sourceText):
    sourceXml = xml.Element('mediawiki')
    mwText = mw.parse(sourceText)
    for section in mwText.get_sections():
        sectionElement = sectionToXml(section)
        sourceXml.append(sectionElement)
    return sourceXml

def convertNodesToXml(baseNode, baseElement):
    for node in baseNode.nodes:
        nodeXml = convertNodeToXml(node)
        baseElement.append(nodeXml)
    return baseElement

def convertNodeToXml(node):
    if (isinstance(node, mw.nodes.argument.Argument)):
        return argumentToXml(node)

    if (isinstance(node, mw.nodes.comment.Comment)):
        return commentToXml(node)

    if (isinstance(node, mw.nodes.external_link.ExternalLink)):
        return externalLinkToXml(node)

    if (isinstance(node, mw.nodes.heading.Heading)):
        return headingToXml(node)

    if (isinstance(node, mw.nodes.html_entity.HTMLEntity)):
        return htmlEntityToXml(node)

    if (isinstance(node, mw.nodes.tag.Tag)):
        return tagToXml(node)

    if (isinstance(node, mw.nodes.template.Template)):
        return templateToXml(node)

    if (isinstance(node, mw.nodes.text.Text)):
        return textToXml(node)

    if (isinstance(node, mw.nodes.wikilink.Wikilink)):
        return wikilinkToXml(node)

    raise ValueError('Unhandled type ' + str(type(node)))

def argumentToXml(node):
    argumentNode = xml.Element('argument')
    argumentNode.set('name', str(node.name).strip())
    if (node.default != None):
        argumentNode = convertNodesToXml(node.default, argumentNode)
    return argumentNode

def commentToXml(node):
    commentNode = xml.Element('comment')
    commentNode = convertNodesToXml(node.contents, commentNode)
    return commentNode

def externalLinkToXml(node):
    linkNode = xml.Element('link')
    titleNode = convertNodesToXml(node.title, xml.Element('title'))
    urlNode = convertNodesToXml(node.url, xml.Element('url'))
    linkNode.append(titleNode)
    linkNode.append(urlNode)
    return linkNode

def headingToXml(node):
    headingNode = xml.Element('heading')
    headingNode.set('level', str(node.level))
    headingNode = convertNodesToXml(node.title, headingNode)
    return headingNode

def htmlEntityToXml(node):
    htmlNode = xml.Element('char')
    htmlNode.text = xml.CDATA(node.value)
    return htmlNode

def parameterToMarkup(node):
    paramNode = xml.Element('parameter')
    paramNode.set('name', str(node.name).strip())
    paramNode.set('showkey', str(node.showkey))
    paramNode = convertNodesToXml(node.value, paramNode);
    return paramNode

def sectionToXml(node):
    sectionElement = xml.Element('section')
    return convertNodesToXml(node, sectionElement)

def templateToXml(node):
    templateNode = xml.Element('template')
    templateNode.set('name', str(node.name).strip())
    for param in node.params:
        paramNode = parameterToMarkup(param)
        templateNode.append(paramNode)
    return templateNode

def tagToXml(node):
    tagNode = xml.Element('tag')
    tagNode.text = xml.CDATA(str(node))
    return tagNode

def textToXml(node):
    textNode = xml.Element('text')
    textNode.text = xml.CDATA(node.value)
    return textNode

def wikilinkToXml(node):
    wikilinkNode = xml.Element('wikilink')
    titleNode = convertNodesToXml(node.title, xml.Element('title'))
    textNode = xml.Element('text')
    if (node.text != None):
        textNode.text = xml.CDATA(node.text)
    wikilinkNode.append(titleNode)
    wikilinkNode.append(textNode)
    return wikilinkNode
