from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.homepage,name='invoice-homepage'),
    path('add_items/<str:id>/', views.add_items, name='add-items'),
    path('update_items/<str:id>/<int:pk>', views.item_update, name='update-items'),
    path('delete_items/<str:id>/<int:pk>', views.item_delete, name='delete-items'),
    path('history/<str:id>/', views.history, name='history'),
    path('generate-pdf/<str:id>/<str:type>', views.generate_pdf, name='generate-pdf'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)