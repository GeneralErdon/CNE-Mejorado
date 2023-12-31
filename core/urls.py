
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from apps.elecciones.views import HomePage, NotFoundView, TotalizarVotosView, VotarView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', HomePage.as_view(), name='home'),
    path('votar/', csrf_exempt(VotarView.as_view()), name="votar"),
    path('totalizar/<uuid:pk>/', TotalizarVotosView.as_view(), name="totalizar"),
    
    re_path(r"^.*/$", NotFoundView.as_view(), name="404")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
