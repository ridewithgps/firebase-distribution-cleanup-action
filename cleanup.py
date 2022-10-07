#!/usr/bin/env python3

import os.path
import sys

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

APP_ID = sys.argv[1]

DISCOVERY_URI = 'https://firebaseappdistribution.googleapis.com/$discovery/rest?version=v1'

def main():
    try:
        service = build('appdistribution', 'v1', discoveryServiceUrl=DISCOVERY_URI)
    except HttpError as err:
        print(err)

    releases = service.projects().apps().releases()

    items = []
    go = True
    nextPageToken = ''

    if len(sys.argv) > 1:
        while go:
            try:
                res = releases.list(parent = APP_ID, pageToken = nextPageToken).execute()
                nextPageToken = res.get('nextPageToken')
                items.extend(res['releases'])
                go = nextPageToken
            except HttpError as err:
                print(err)
        print("Found %s artifacts" % len(items))


    if len(sys.argv) > 2 and len(sys.argv[2]) > 0:
        pr = sys.argv[2]
        print("Matching builds against: %s" % pr)
        toRemove = list(filter(lambda x: pr in x['displayVersion'], items))

        names = [ x['name'] for x in toRemove ]

        if len(names) > 0:
            dell = releases.batchDelete(parent = APP_ID, body = {'names': names})
            dell.execute()

        print("Removed %s artifacts:" % len(names))
        print("\n".join(["  %s" % x['displayVersion'] for x in toRemove]))

if __name__ == '__main__':
    main()
