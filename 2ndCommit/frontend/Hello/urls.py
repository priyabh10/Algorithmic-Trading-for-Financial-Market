

from django.contrib import admin
from django.urls import path, include

admin.site.site_header = ""
admin.site.site_title = ""
admin.site.index_title = ""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'))

]
