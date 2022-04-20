from django.urls import path
from .views import ThirdPartyView, LicensingView, CombinedView, ComprehensiveView, PolicyReversalView

urlpatterns = [
    path('thirdparty/', ThirdPartyView.as_view(), name="thirdparty"),
    path('licensing/', LicensingView.as_view(), name="licensing"),
    path('combined/', CombinedView.as_view(), name="combined"),
    path('comprehensive/', ComprehensiveView.as_view(), name="comprehensive"),
    path('reversal_policy/', PolicyReversalView.as_view(), name="reversal_policy"),
]