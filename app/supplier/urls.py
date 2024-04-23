"""
URL mapings for the recipe apps.
"""

from django.urls import (
    path,
    include,
)

from supplier import views

app_name = 'supplier'

urlpatterns = [
    path('', views.supplier),
    path('<int:id>', views.supplier_detail)
]