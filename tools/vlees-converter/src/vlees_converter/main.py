"""Assortiment converter."""

import csv
import io
import os

import yaml
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

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


def to_templates(templates_path='content/products/',
                 sheet_path='assortiment/Vlees assortiment - assortiment.csv'):
    """Convert csv to product markdown files."""
    data = sheet(sheet_path)
    cols = next(data)
    print('cols:', cols)

    write = create_writer(templates_path)

    for row in data:

        # skip empty rows
        if not any(row):
            continue

        # convert to dict
        d = dict(zip(cols, row))

        # skip products that have no price
        if not d['price']:
            continue

        # convert to product
        p = Product(**d)
        write(**p.__dict__)

    print('Templates written to ', templates_path)


def to_sheet(templates_path='data/output/',
             sheet_path='data/input/test.csv'):
    """Convert product markdown files to csv."""
    data = templates(templates_path)

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

    with open(sheet_path, 'w') as f:
        w = csv.writer(f)
        for p in data:
            w.writerow([p[col] for col in column_order])
        print('Csv written to ', sheet_path)


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

        with open(f'{folder}{title}.md', 'w') as f:
            f.write(template.format(**kwargs))
    return _inner


def download_csv(file_id='1EDZQHGoad_XQabpskXeT7Q5A0n55L4Gisz1v8a5O1Vo'):

    # Find credentials
    scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    creds = Credentials.from_authorized_user_file('credentials.json', scopes)
    service = build('drive', 'v3', credentials=creds)

    # Download file
    request = (
        service
        .files()
        .export_media(fileId=file_id, mimeType='text/csv')
    )
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
