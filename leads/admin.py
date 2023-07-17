from django.contrib import admin

from .models import Agent, Category, Lead, User, UserPortfolio

admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(UserPortfolio)
admin.site.register(Category)
