#!/usr/bin/env python3

from __future__ import print_function

import os.path

from sys import argv

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

    while go:
        try:
            res = releases.list(parent = APP_ID, pageToken = nextPageToken).execute()
            nextPageToken = res.get('nextPageToken')
            items.extend(res['releases'])
            go = nextPageToken
        except HttpError as err:
            print(err)


    if len(argv) > 2:
        pr = argv[2]
        print("Scanning: ", pr)
        toRemove = filter(lambda x: pr in x['displayVersion'], items)

        names = [ x['name'] for x in toRemove ]
        print(names)

        if len(names) > 0:
            dell = releases.batchDelete(parent = APP_ID, body = {'names': names})
            dell.execute()

if __name__ == '__main__':
    main()
