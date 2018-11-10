from django.conf.urls import url
from .import views


urlpatterns = [
    url(r'^signup/$',views.SignupAPIView.as_view()),
    url(r'^signup/security-code/(?P<pk>\d+)/$',views.VerifyAPIView.as_view()),
    url(r'^complete-profile/$',views.CompleteProfile.as_view()),
]
