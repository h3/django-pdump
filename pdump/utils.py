# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import json

from texttable import Texttable, bcolors, get_color_string as c

GLOBAL_CACHE = {}

purple,  blue, green, yellow, red, endc, white = (
    bcolors.PURPLE,
    bcolors.BLUE,
    bcolors.GREEN,
    bcolors.YELLOW,
    bcolors.RED,
    bcolors.ENDC,
    bcolors.WHITE)


class Fields(object):
    obj = None

    def __init__(self, obj, diff=True):
        self.diff = diff
        self.obj = obj
        if obj.pk:
            self.ns = '%s.%s-%s' % (obj._meta.model_name, obj._meta.app_label, obj.pk)
        else:
            self.ns = '%s.%s' % (obj._meta.model_name, obj._meta.app_label)

    def render(self, fieldname):
        ns = '%s.%s' % (self.ns, fieldname)
        val = getattr(self.obj, fieldname)
        if self.diff and not GLOBAL_CACHE.get(ns):
            GLOBAL_CACHE[ns] = val
        if not self.diff or GLOBAL_CACHE[ns] == val:
            return c(green, val)
        else:
            GLOBAL_CACHE[ns] = val
            return c(red, val)


class Pdump(object):
    options = {}
    action = None
    model = None
    app_model = None

    def __init__(self, options):
        self.options = options
        self.action = self._get_action()
        if self.options.get('watch'):
            self.watch()
        else:
            self.run()

    def _ids(self):
        return [int(i) for i in self.options.get('pks').split(',')]

    def _get_model(self):
        if type(self.options.get('object')) is str:
            app, model = self.options.get('object').split('.')
        elif type(self.options.get('object')) is object:
            obj = self.options.get('object')
            app, model = (obj._meta.model_name, obj._meta.app_label, obj.pk)
        else:
            app, model = self.options.get('list').split('.')
        return apps.get_model(app_label=app, model_name=model)

    def _get_action(self):
        if self.options.get('object'):
            return self.dump_object
        elif self.options.get('list'):
            return self.dump_list
        else:
            raise CommandError('This command requires a --object or a --list option')  # noqa

    def run(self):
        if self.options.get('object'):
            for obj in self.query():
                self.action(obj)
        elif self.options.get('list'):
            self.action(self.query())

    def watch(self):
        try:
            while True:
                os.system('clear')
                print('\n')
                self.run()
                print("Watching, press Ctrl+Q to pause, Ctrl+S to resume and Ctrl+C to exit.")  # noqa
                time.sleep(int(self.options.get('watch_interval')))
        except KeyboardInterrupt:
            sys.exit(0)

    def query(self):
        if type(self.options.get('object')) is str:
            self.model = self._get_model()
            if self.options.get('filter'):
                return self.model.objects.filter(**json.loads(self.options.get('filter')))
            elif self.options.get('pks'):
                return self.model.objects.filter(pk__in=self._ids())
            else:
                return self.model.objects.all()
        else:
            return [self.options.get('object')]

    def output(self, rows):
        table = Texttable(max_width=self.options.get('max_width'))
        table.add_rows(rows)
        print(table.draw())
        print('\n')

    def title(self, s):
        print('%s\n%s' % (s, len(s) * '='))

    def dump_related(self, obj):
        for ro in obj._meta.related_objects:
            if ro.one_to_one:
                try:
                    self.dump_object(getattr(obj, ro.related_name), related=False)
                except:
                    pass
            elif ro.one_to_many:
                try:
                    qs = getattr(obj, '%s_set' % ro.name).all()
                    if qs.count():
                        self.dump_list(qs)
                except:
                    pass

    def dump_object(self, obj, related=True):
        _rows =[]
       #import IPython
       #IPython.embed()
        f = Fields(obj, diff=self.options.get('diff')).render
        self.title('%s.%s' % (obj._meta.app_label, obj._meta.model_name))
        _rows.append([c(blue, 'Field'), c(blue, 'Value')])
        for field in obj._meta.fields:
            _rows.append([c(blue, field.verbose_name), f(field.name)])
        self.output(_rows)
        if related and self.options.get('related'):
            self.dump_related(obj)

    def dump_list(self, qs):
        if not qs.count():
            sys.exit(0)
        _rows = []
        _cols = []
        for field in qs[0]._meta.fields:
            _cols.append(c(blue, field.verbose_name))
        _rows.append(_cols)
        for obj in qs:
            f = Fields(obj, diff=self.options.get('diff')).render
            _cols = []
            for field in obj._meta.fields:
                if len(_cols) == 0:
                    _cols.append(c(blue, f(field.name)))
                else:
                    _cols.append(f(field.name))
            _rows.append(_cols)
        self.title('%s.%s' % (qs[0]._meta.app_label, qs[0]._meta.model_name))
        self.output(_rows)
