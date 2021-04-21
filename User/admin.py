from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Hospital)
admin.site.register(NGO)
admin.site.register(Bill)
admin.site.register(Admission)
admin.site.register(HelpRequest)