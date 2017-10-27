from django.contrib import admin
from api.models import Group, Node, AlarmLog

admin.site.register([Group, Node, AlarmLog])
