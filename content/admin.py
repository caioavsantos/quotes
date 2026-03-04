from django.contrib import admin

from .models import Thinker, Quote, Work, Picture, DailyQuote

admin.site.register(Thinker)
admin.site.register(Quote)
admin.site.register(Work)
admin.site.register(Picture)
admin.site.register(DailyQuote)