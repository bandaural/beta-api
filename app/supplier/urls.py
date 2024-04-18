"""
URL mapings for the supplier apps.
"""

from django.urls import (
    path
)

from supplier import views

app_name = 'supplier'

urlpatterns = [
    path('', views.supplier),
    path('<int:id>', views.supplier_detail)
]