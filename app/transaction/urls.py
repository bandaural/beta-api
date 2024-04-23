"""
URL mapings for the recipe apps.
"""

from django.urls import (
    path,
    include,
)

from transaction import views

app_name = 'transaction'

urlpatterns = [
    path('', views.transaction),
    path('<int:id>', views.transaction_detail),
    path('body', views.body)
]