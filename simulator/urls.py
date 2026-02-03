from django.urls import path

from transactions import views

urlpatterns = [
    path("api/transactions/", views.create_transaction, name="create-transaction"),
    path("api/transactions/<uuid:transaction_id>/", views.transaction_detail, name="transaction-detail"),
]
