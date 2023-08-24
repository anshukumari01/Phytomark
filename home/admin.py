from django.contrib import admin
from .models import  Banner
from .models import Placeholder
from .models import About
from .models import Fproduct
from .models import Info
from .models import Contact
from .models import Service
from .models import OrganicFarming


# Register your models here.
admin.site.register(Banner)
admin.site.register(Placeholder)
admin.site.register(About)
admin.site.register(Fproduct)
admin.site.register(Info)
admin.site.register(Contact)
admin.site.register(Service)
admin.site.register(OrganicFarming)