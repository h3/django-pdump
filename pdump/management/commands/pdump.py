# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError  # noqa

from pdump.utils import Pdump, purple, blue, green, yellow, c


class Command(BaseCommand):
    """
    python manage.py pdump --object users.user --filter={"pk": 1} --watch=1 --diff --diff-colors=red,green,blue --fields=email,first_name
    python manage.py pdump --object users.user --filter={"pk__in": [1,2,3,4]}

    python manage.py pdump --list users.user:{"username__istartwith": "anon"}
    python manage.py pdump --list users.user:[1,2,3,4]

    python manage.py pdump --signals
    python manage.py pdump --signals users
    python manage.py pdump --signals users.user

    """
    help = 'Pretty print and shit'

    def add_arguments(self, parser):
        parser.add_argument('--watch',
            dest='watch',
            action='store_true',
            default=False,
            help='Watch mode')

        parser.add_argument('--related',
            dest='related',
            action='store_true',
            default=False,
            help='Watch mode')

        parser.add_argument('--max-width',
            dest='max_width',
            type=int,
            default=400,
            help='Watch interval')

        parser.add_argument('--watch-interval',
            dest='watch_interval',
            type=int,
            default=5,
            help='Watch interval')

        parser.add_argument('--diff',
            dest='diff',
            default=True,
            action='store_true',
            help='Diff (only with watch)')

        parser.add_argument('--diff-colors',
            dest='diff_colors',
            type=str,
            default='white,green',
            help='Diff (only with watch)')

        parser.add_argument('--list',
            dest='list',
            type=str,
            help='Dump list')

        parser.add_argument('--fields',  # TODO: --exclude
            dest='fields',
            type=str,
            help='Only given fields (coma separeted)')

        parser.add_argument('--pks',
            dest='pks',
            type=str,
            help='Coma separeted list of ids')

        parser.add_argument('--filter',
            dest='filter',
            help='Use "filter" method on queryset')

    def handle(self, *args, **options):
        Pdump(options)
        sys.exit(0)
