"""
@file __init__.py
@role
Marks the perfume service package.
"""

"""Perfume service package.

Import service classes from their concrete modules to avoid loading optional
runtime dependencies when a command only needs one small service.
"""

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-13: fix(django): guard migrate schema drift. (author: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: __init__.py
