"""
@file apps.py
@role
Defines the perfumes Django app configuration.
"""

from django.apps import AppConfig


class PerfumesConfig(AppConfig):
    """Django perfumes 앱의 기본 설정을 정의한다."""

    name = 'perfumes'

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: apps.py
