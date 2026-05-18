"""
@file wsgi.py
@role
Exposes the WSGI callable for synchronous Django deployments.
"""

"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: wsgi.py
