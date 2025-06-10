from django.contrib import admin

# Importa as models
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(ExtratoMovimentacao)