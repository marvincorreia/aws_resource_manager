from django.contrib import admin
from django.forms.widgets import Textarea
from django.db.models import TextField
from . import models


class CronJobLogInline(admin.TabularInline):
    model = models.CronJobLog
    extra = 0
    max_num = 2
    # formfield_overrides = {
    #     TextField: {'widget': Textarea(attrs={'rows': 5,  'cols': 50})},
    # }
