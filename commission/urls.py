from django.urls import path
from .views import CommissionsView, CommissionsSummedView

urlpatterns = [
    path('transactions/', CommissionsView.as_view(), name="transactions"),
    path('commission/', CommissionsSummedView.as_view(), name="commission")
]