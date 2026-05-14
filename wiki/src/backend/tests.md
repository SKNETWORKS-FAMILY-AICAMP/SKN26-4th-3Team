# Backend Tests

## Status

Last verified: 2026-05-14

```bash
docker compose exec -T -w /backend/app backend python manage.py test perfumes --keepdb
```

Result:

```text
Ran 14 tests in 0.259s
OK
```

## Scope

Backend tests live in `backend/app/perfumes/tests.py`. The current suite covers:

- `/api/analyze/` request handling and missing session rejection
- preservation of recommendation image payload fields in the analyze response
- perfume raw data ingestion into normalized `PerfumeDetail` and `PerfumeRawData`
- perfume image extraction, skip behavior, failure recording, and DB sync
- Fragrantica image URL backfill parsing
- recommendation response payload shape, including detail data, note pyramid fallback, image URL, and base64 image fields

## Image Payload Contract Test

`AnalyzeViewTest.test_analyze_response_preserves_recommendation_image_payload` locks the API boundary between backend and frontend. The test mocks the VLM, aura scoring, and recommendation service so it verifies only the analyze endpoint response mapping.

The response must preserve these recommendation fields:

```json
{
  "image": "/static/perfumes/images/bvlgari/black.jpg",
  "imageUrl": "http://localhost:8000/static/perfumes/images/bvlgari/black.jpg",
  "imageBase64": "base64-image",
  "imageDetail": {
    "url": "/static/perfumes/images/bvlgari/black.jpg",
    "originalUrl": "https://img.example.com/black.jpg",
    "backendPath": "/backend/app/static/perfumes/images/bvlgari/black.jpg",
    "base64": "base64-image"
  }
}
```

This protects the frontend image rendering path:

1. `imageBase64` for immediate inline rendering
2. `imageUrl` for browser-accessible backend static files
3. legacy `image` and `imageDetail` fields for compatibility

## Focused Commands

Run only the analyze image payload test:

```bash
docker compose exec -T -w /backend/app backend python manage.py test perfumes.tests.AnalyzeViewTest.test_analyze_response_preserves_recommendation_image_payload --keepdb
```

Run only recommendation service contract tests:

```bash
docker compose exec -T -w /backend/app backend python manage.py test perfumes.tests.RecommendationServiceTest --keepdb
```

## Notes

Use Docker for backend tests. The local Windows Python environment may miss container dependencies or fail on console encoding, while the Docker backend matches the running service environment.
