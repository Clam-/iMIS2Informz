from __future__ import print_function
from string import Template
from base64 import b64encode, b64decode
from pysimplesoap.client import SoapClient # https://web.archive.org/web/20151122142348/http://code.google.com/p/pysimplesoap/wiki/SoapClient
from gzip import compress, decompress
from defusedxml import cElementTree

from sys import stderr
import re, requests, json
from collections import OrderedDict
from datetime import datetime
from time import sleep
from os.path import expanduser, join
home = expanduser("~")

from InformzBodies import INTERESTS


SETTINGS = json.load(open(join(home, ".informz.json"), "rb"))
API_URL = SETTINGS["API_URL"]
USERNAME = SETTINGS["username"]
PASSWORD = SETTINGS["password"]
BRAND_NAME = SETTINGS["BRAND_NAME"]
BRAND_ID = SETTINGS["BRAND_ID"]

CLIENT = SoapClient(wsdl="https://partner.informz.net/AAPI/InformzService.svc?singleWsdl")





# Subscriber, Subscriber Interests
SAMPLE = Template("""<GridRequest xmlns="http://partner.informz.net/aapi/2009/08/">
<Password>$password</Password>
<Brand id="$BRAND_ID">$BRAND_NAME</Brand>
<User>$username</User>
<Grids>$data</Grids>
</GridRequest>""").safe_substitute(**SETTINGS).replace("\n", "")

def makeRequest(body):
    ebody = body.encode("utf-8")
    encbody = b64encode(len(ebody).to_bytes(4, 'little')+compress(ebody)).decode("utf-8")
    payload = Template(SAMPLE).safe_substitute(data=encbody)
    response = CLIENT.PostInformzMessage(payload)
    responsetree = cElementTree.fromstring(response['PostInformzMessageResult'])
    grids = responsetree.find("{http://partner.informz.net/aapi/2009/08/}Grids")
    return cElementTree.fromstring(decompress(b64decode(grids.text)[4:]))

respunzip = makeRequest(INTERESTS)
