"""Assortiment converter."""

import argparse
import csv
import os

import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TEMPLATE = """---
title: "{title}"
price: "{price}"
image: "{image}"
subtitle: "{subtitle}"
category: "{type}"
weight: "{weight}"
truncated: {truncated}
ordinal: {ordinal}
date: {date}
draft: {draft}
action: {action}
items: {items}
---
"""


class Product():
    """A generic product class."""

    def __init__(self, title, price, type, weight, image, action,
                 subtitle, date, live, ordinal, truncated, items=None):
        """Init."""
        self.title = title.title()
        self.price = price.replace("€", "")
        self.type = type.lower()
        self.weight = weight
        self.image = image
        self.action = action == 'TRUE'
        self.subtitle = subtitle
        self.date = date
        self.draft = live == 'FALSE'
        self.ordinal = int(ordinal) if ordinal else 0
        self.truncated = truncated == 'TRUE'
        self.items = items


def to_templates():
    """Convert csv to product markdown files."""
    parser = argparse.ArgumentParser('downloader')
    parser.add_argument('sheet_path', type=str)
    parser.add_argument('templates_path', type=str)
    args = parser.parse_args()

    data = sheet(args.sheet_path)
    cols = next(data)
    print('cols:', cols)

    write = create_writer(args.templates_path)

    for row in data:

        # skip empty rows
        if not any(row):
            continue

        # convert to dict
        d = dict(zip(cols, row))

        # skip products that have no price
        # if not d['price']:
            # continue

        # convert to product
        p = Product(**d)
        write(**p.__dict__)

    print('Templates written to ', args.templates_path)


def to_sheet():
    """Convert product markdown files to csv."""
    parser = argparse.ArgumentParser('downloader')
    parser.add_argument('templates_path', type=str)
    parser.add_argument('sheet_path', type=str)
    args = parser.parse_args()

    data = templates(args.templates_path)

    column_order = ('title',
                    'price',
                    'category',
                    'weight',
                    'image',
                    'subtitle',
                    'date',
                    'draft',
                    'ordinal',
                    'truncated',
                    'action',
                    'items')

    with open(args.sheet_path, 'w') as f:
        w = csv.writer(f)
        for p in data:
            w.writerow([p[col] for col in column_order])
        print('Csv written to ', args.sheet_path)


def templates(path: str):
    """Read product templates."""
    for entry in os.scandir(path):
        if entry.path.endswith('.md') and entry.is_file():
            with open(entry.path, 'r') as f:
                yield yaml.safe_load(f.read().replace('---\n', ''))


def sheet(path: str):
    """Read product csv."""
    with open(path) as c:
        for line in csv.reader(c):
            yield line


def mkdir(path: str):
    """Create folder if not exists."""
    if not os.path.exists(path):
        os.makedirs(path)


def create_writer(folder: str, template=TEMPLATE):
    """Create writer function."""
    mkdir(folder)

    def _inner(*args, **kwargs):
        title = (
            kwargs['title']
            .lower()
            .replace(' ', '-')
            .replace('/', '-')
        )

        fullpath = os.path.join(folder, title)

        with open(f'{fullpath}.md', 'w') as f:
            f.write(template.format(**kwargs))
    return _inner


def download_csv():
    """Download csv file with products."""
    parser = argparse.ArgumentParser('downloader')
    parser.add_argument('file_id', type=str)
    parser.add_argument('outpath', type=str)
    args = parser.parse_args()

    # Find credentials
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create service
    service = build('drive', 'v3', credentials=creds)

    # Download file
    data = (
        service
        .files()
        .export(fileId=args.file_id, mimeType='text/csv')
        .execute()
    )

    # if non-empty file
    if data:
        with open(args.outpath, 'wb') as f:
            f.write(data)
        print('DONE')
