#!/usr/bin/python

import glob
from os.path import expanduser
import re
from xml.etree import ElementTree as ET

BASEDIR = expanduser(r"~/Library/Application Support/Viscosity/OpenVPN")
CONNECTION_NAME_RE = re.compile("#viscosity\\s+name\\s+(.*)$")
REMOTE_NAME_RE = re.compile("\\s*remote\\s+([^\\s]+)")

def addConnection(xmlTree, name, remotes):
  elem = ET.SubElement(xmlTree, 'item')

  # Add the title
  titleElem = ET.SubElement(elem, 'title')
  titleElem.text = name

  # Add the subtitle
  subTitleElem = ET.SubElement(elem, 'subtitle')
  subTitleElem.text = ' / '.join(remotes)

  # Add an icon
  iconElement = ET.SubElement(elem, 'icon')
  iconElement.text = 'icon.png'

  # Add the arg attribute
  elem.set("arg", name)
  elem.set("uid", name)

def getConnections(query):
  if query == None:
    query = ""
  else:
    query = query.lower()

  xmlTree = ET.Element("items")

  for configFile in glob.glob("%s/*/config.conf" % BASEDIR):
    name = None
    remotes = set()


    for line in open(configFile, "r"):
      match = CONNECTION_NAME_RE.search(line)
      if match and query in line.lower():
        name = match.group(1)
        continue

      match = REMOTE_NAME_RE.match(line)
      if match:
        remotes.add(match.group(1))

    if name != None:
      addConnection(xmlTree, name, remotes)

  return ET.tostring(xmlTree, encoding="UTF-8")
