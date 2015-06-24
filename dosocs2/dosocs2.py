#!/usr/bin/env python2

# <SPDX-License-Identifier: Apache-2.0>
# Copyright (c) 2014-2015 University of Nebraska at Omaha (UNO) and other
# contributors.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Usage:
{0} generate (PACKAGE-ID)
{0} init [--no-confirm]
{0} print (DOC-ID)
{0} scan [-n] (PATH)
{0} (--help | --version)

Commands:
  generate      Generate SPDX document data in the database for a
                  particular package
  init          Drop and create all tables, then initialize with static
                  data (destructive, will prompt first)
  print         Render and print a document to standard output
  scan          Scan an archive file or directory

Options for 'scan':
  -n, --no-license-scan       Do not scan for license information

Options for 'init':
      --no-confirm            Don't prompt first

Report bugs to <tgurney@unomaha.edu>.
'''

from __future__ import print_function

import os
import pkg_resources
import sys

import docopt
import sqlsoup

from .spdxdb import Transaction
from .settings import settings, VERSION
from . import dbinit
from . import render
from . import scanners  # for the dummy scanner

format_map = {
    'tag': pkg_resources.resource_filename('dosocs2', 'templates/2.0.tag'),
#    'rdf': 'templates/2.0.rdf',
}


def msg(text, **kwargs):
    print('dosocs2' + ': ' + text, **kwargs)
    sys.stdout.flush()


def errmsg(text, **kwargs):
    print('dosocs2' + ': ' + text, file=sys.stderr, **kwargs)
    sys.stdout.flush()


def initialize(db):
    url = 'http://spdx.org/licenses/'
    msg('dropping all views...', end='')
    result = dbinit.drop_all_views(db)
    print('ok.')
    msg('dropping all tables...', end='')
    result = dbinit.drop_all_tables(db)
    print('ok.')
    msg('creating all tables...', end='')
    result = dbinit.create_all_tables(db)
    print('ok.')
    msg('committing changes...', end='')
    db.commit()
    print('ok.')
    msg('creating all views...', end='')
    result = dbinit.create_all_views(db)
    print('ok.')
    msg('loading licenses...', end='')
    result = dbinit.load_licenses(db, url)
    if not result:
        errmsg('error!')
        errmsg('failed to download and load the license list')
        errmsg('check your connection to ' + url + ' and make sure it is the correct page')
        return False
    else:
        print('ok.')
    msg('loading creator types...', end='')
    dbinit.load_creator_types(db)
    print('ok.')
    msg('loading default creator...', end='')
    dbinit.load_default_creator(db, 'dosocs2-' + VERSION)
    print('ok.')
    msg('loading annotation types...', end='')
    dbinit.load_annotation_types(db)
    print('ok.')
    msg('loading file types...', end='')
    dbinit.load_file_types(db)
    print('ok.')
    msg('loading relationship types...', end='')
    dbinit.load_relationship_types(db)
    print('ok.')
    msg('committing changes...', end='')
    db.commit()
    print('ok.')
    return True


def main():
    argv = docopt.docopt(doc=__doc__.format(os.path.basename(sys.argv[0])), version=VERSION)

    doc_id = argv['DOC-ID']
    document = None
    db = sqlsoup.SQLSoup(settings['connection-uri'])
    license_scan = not argv['--no-license-scan']
    package_id = argv['PACKAGE-ID']
    package_path = argv['PATH']
    output_format = 'tag'

    if argv['init']:
        if not argv['--no-confirm']:
            errmsg('preparing to initialize the database')
            errmsg('all existing data will be deleted!')
            errmsg('make sure you are connected to the internet before continuing.')
            errmsg('type the word "YES" (all uppercase) to commit.')
            answer = raw_input()
            if answer != 'YES':
                errmsg('canceling operation.')
                sys.exit(1)
        if initialize(db):
            sys.exit(0)
        else:
            sys.exit(1)
    elif argv['print']:
        with Transaction(db) as t:
            document = t.fetch('documents', doc_id)
        if document is None:
            errmsg('document id {} not found in the database.'.format(doc_id))
            sys.exit(1)
        print(render.render_document(db, doc_id, format_map[output_format]))
    elif argv['generate']:
        with Transaction(db) as t:
            package = t.fetch('packages', package_id)
            if package is None:
                errmsg('package id {} not found in the database.'.format(package_id))
                sys.exit(1)
            document = t.create_document(package_id)
            print('(package_id {}): document_id: {}'.format(package_id, document.document_id))
    elif argv['scan']:
        with Transaction(db) as t:
            if license_scan:
                package = t.scan_package(package_path)
            else:
                package = t.scan_package(package_path, scanner=scanners.dummy)
        print('{}: package_id: {}'.format(package_path, package.package_id))


if __name__ == "__main__":
    main()
