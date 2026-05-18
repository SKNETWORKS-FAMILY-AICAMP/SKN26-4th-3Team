"""
@file urls.py
@role
Maps perfume app API routes to view handlers.
"""

from django.urls import path
from .views import AnalyzeView

urlpatterns = [
    path('analyze/', AnalyzeView.as_view(), name='analyze'),
]

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: urls.py
