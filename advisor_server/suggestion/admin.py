# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.models import TrialMetric

admin.site.register(Study)
admin.site.register(Trial)
admin.site.register(TrialMetric)
