import lxml.etree as xml
import mw2xml
from pathlib import Path
import sys
import xml2mw

numArgs = len(sys.argv)
sourceFilename = Path(sys.argv[1] if numArgs > 1 else 'source.txt')
xsltFilename = Path(sys.argv[2] if numArgs > 2 else 'transformation.xslt')
destinationFilename = Path(sys.argv[2] if numArgs > 2 else 'transformed.txt')

sourceFile = open(str(sourceFilename), 'r');
sourceText = sourceFile.read()
sourceFile.close()

sourceXml = mw2xml.parse(sourceText)

sourceXmlFile = open(str(sourceFilename.with_suffix('.xml')), 'w')
sourceXmlFile.write(xml.tostring(sourceXml, pretty_print = True))
sourceXmlFile.close()

xslt = xml.parse(str(xsltFilename))
transform = xml.XSLT(xslt)
transformed = transform(sourceXml)

transformedFile = open(str(destinationFilename.with_suffix('.xml')), 'w')
transformedFile.write(xml.tostring(transformed, pretty_print = True))
transformedFile.close()

destinationFile = open(str(destinationFilename), 'w')
destinationFile.write(xml2mw.parse(transformed.getroot()))
destinationFile.close()
