#iMIS Util Functions
from __future__ import print_function
from sys import stderr
import re, requests, json
from collections import OrderedDict
from datetime import datetime
from time import sleep
from os.path import expanduser, join
home = expanduser("~")

SETTINGS = json.load(open(join(home, ".iMIS.json"), "rb"))
SITE_NAME = SETTINGS["SITE_NAME"]
API_URL = SETTINGS["API_URL"]
h = {'content-type': "application/x-www-form-urlencoded"}
formdata = {"Username" : SETTINGS["username"], "Password": SETTINGS["password"], "Grant_type":"password"}
r = requests.post("%s/token" % API_URL, headers=h, data=formdata)
TOKEN = "Bearer %s" % r.json()[u'access_token']
HEADERS = {
    'content-type': "application/json",
    "Authorization" : TOKEN
}

def getUserIDByEmail(email):
    r = requests.get("%s/api/CsContactBasic" % API_URL, headers=HEADERS, params={'email': 'eq:%s' % email, "limit":2})
    if r.json()["Count"] < 1:
        return 0
    if r.json()["Count"] > 1:
        return None
    return r.json()["Items"]["$values"][0]["Identity"]["IdentityElements"]["$values"][0]

def getCommunicationPreferences():
    r = requests.get("%s/api/CommunicationType" % API_URL, headers=HEADERS)
    if r.status_code != 200:
        print("Error")
        print(r.text)
        return False
    else:
        return map(lambda x: x["ReasonCode"], r.json()["Items"]["$values"])

def getCommPrefIDs(commpref):
    r = requests.get("%s/api/CommunicationType" % (API_URL), headers=HEADERS, params={'ReasonCode': commpref})
    if r.status_code != 200:
        print("Error getting comm pref (%s)" % commpref)
        print(r.text)
        return False
    else:
        if r.json()["Count"] != 1:
            print("Not enough/Too many results for (%s) %s" % (commpref, r.json()["Count"]))
        typeid = r.json()["Items"]["$values"][0]["CommunicationTypeId"]
        print("Fetching all (%s) - %s" % (commpref, typeid))
        IDs = []
        r = requests.get("%s/api/iqa" % (API_URL), headers=HEADERS,
            params=(('limit', 500),
                ('QueryName', "$/%s/Contact Queries/CommunicationPrefs" % SITE_NAME),
                ('parameter',"eq:"+typeid)))
        if r.status_code != 200:
            print("ERROR: "+ r.text)
            return
        i = 0
        while r.json()["Count"] > 0:
            i += 500
            for x in r.json()["Items"]["$values"]:
                IDs.append(filter(lambda z: z["Name"] == "ID", x["Properties"]["$values"])[0]["Value"])
            r = requests.get("%s/api/iqa" % (API_URL), headers=HEADERS,
                params=(('limit', 500), ('offset', i),
                    ('QueryName', "$/%s/Contact Queries/CommunicationPrefs" % SITE_NAME),
                    ('parameter',"eq:"+typeid)))
            if r.status_code != 200:
                print("ERROR: "+ r.text)
                return
        return IDs

def apiIterator(url, p):
    p = list(p)
    p.append(("limit","100"))
    r = requests.get("%s%s" % (API_URL, url), headers=HEADERS, params=p)
    if r.status_code != 200:
        print("ERROR: "+ r.text)
        return
    print("Total: %s" % r.json()["TotalCount"], file=stderr)
    while r.json()["Count"] > 0:
        nextoffset = r.json()["NextOffset"]
        for x in r.json(object_pairs_hook=OrderedDict)["Items"]["$values"]:
            yield x
        if nextoffset == 0: return
        print(nextoffset)
        r = requests.get("%s%s" % (API_URL, url), headers=HEADERS,
            params=p+[('offset', nextoffset)])
        if r.status_code != 200:
            print("ERROR: "+ r.text)
            return

def accessProperty(item, pname, pval=None):
    for prop in item["Properties"]["$values"]:
        if prop["Name"] == pname:
            if isinstance(prop["Value"], dict):
                if (pval is not None): prop["Value"]["$value"] = pval
                return prop["Value"]["$value"]
            else:
                if (pval is not None): prop["Value"] = pval
                return prop["Value"]

def updateProperty(item, url):
    iid = item["Identity"]["IdentityElements"]["$values"][0]
    r = requests.put("%s/api/%s/%s" % (API_URL, url, iid), headers=HEADERS, data=json.dumps(item))
    if r.status_code != 200 and r.status_code != 201:
        print(r.status_code, " - ", r.text)
        return False
    return True
