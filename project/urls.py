from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('app.urls', namespace='app')),
    # path('', include('app.student_urls',
    # 	 namespace='student')),

    path('', include('app2.urls_teacher', namespace='teacher_app')),
    path('', include('app2.urls_student', namespace='student_app')),

    path('', include('app2.urls_admin', namespace='app2')),
    path('api/', include('app2.urls_api')),

    # path('__debug_/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

