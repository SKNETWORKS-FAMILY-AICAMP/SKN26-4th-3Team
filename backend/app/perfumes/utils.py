import json
import os
from django.conf import settings

def load_master_map():
    path = os.path.join(settings.BASE_DIR, 'perfumes', 'data', 'mappings', 'master_fragrance_map.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_user_preference_map():
    path = os.path.join(settings.BASE_DIR, 'perfumes', 'data', 'mappings', 'user_preference_map.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_mood_descriptors():
    path = os.path.join(settings.BASE_DIR, 'perfumes', 'data', 'mappings', 'fragrance_mood_descriptors.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_preference_expansion():
    path = os.path.join(settings.BASE_DIR, 'perfumes', 'data', 'mappings', 'user_preference_map.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
