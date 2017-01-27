# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db.models.signals import post_save, pre_save

from pdump.utils import Pdump, purple, blue, green, yellow, c


def dump_model_pre_save_signal(sender, instance=None, created=False, **kwargs):
    title = '%s %s' % (c(yellow, 'PRE SAVE'), c(purple, str(kwargs)))
    print(c(blue, ">>> %s" % title))
    Pdump({'object': instance})


def dump_model_post_save_signal(sender, instance=None, created=False, **kwargs):
    title = '%s %s' % (c(yellow, 'POST SAVE'), c(purple, str(kwargs)))
    print(c(green, ">>> %s" % title))
    Pdump({'object': instance})


if getattr(settings, 'PDUMP_SIGNALS', False) == True:

    post_save.connect(dump_model_post_save_signal)
    pre_save.connect(dump_model_pre_save_signal)
