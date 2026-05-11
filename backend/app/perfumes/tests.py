import json
import base64
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

class AnalyzeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('analyze') 
        self.session_id = "test-session-uuid"

    @patch('scent_engine.VLEngine.analyze_image')
    def test_analyze_success(self, mock_analyze):
        # Mock VLM response
        mock_analyze.return_value = {
            "visual_summary": "검은색 슈트를 입은 세련된 남성",
            "colors": ["black"],
            "objects": ["suit"],
            "scene": ["indoor"],
            "mood": ["urban", "modern"],
            "season": ["autumn"],
            "time": ["night"],
            "raw_keywords": ["chic", "sharp"]
        }

        # Mock Image (1x1 white pixel)
        small_img = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xff\xff\xff\x3f\x00\x05\xfe\x02\xfe\x0dcD\x01\x00\x00\x00\x00IEND\xaeB`\x82').decode()
        
        data = {
            "image": small_img,
            "selectedNotes": ["베르가못", "샌달우드"]
        }
        
        headers = {'HTTP_X_SESSION_ID': self.session_id}
        response = self.client.post(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('recommendations', response.data)
        self.assertIn('radarScores', response.data['analysisMetadata'])
        print(f"Test Success: {response.data['fashionStyle']}")

    def test_analyze_missing_session_id(self):
        data = {"image": "dummy", "selectedNotes": []}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
