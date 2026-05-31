# Django → FastAPI Migration Guide

## Setup

```bash
cd backend-fastapi
pip install -r requirements.txt

# Copy your .env (update SECRET_KEY)
cp .env.example .env

# Run the server (replaces: python manage.py runserver)
uvicorn main:app --reload
```

Interactive API docs available at: http://localhost:8000/docs

---

## Django → FastAPI Mapping

| Django / DRF                        | FastAPI equivalent                        |
|-------------------------------------|-------------------------------------------|
| `settings.py`                       | `core/config.py` (pydantic-settings)      |
| `models.py` + Django ORM            | `auth/models.py` + SQLAlchemy             |
| `python manage.py migrate`          | Tables created automatically on startup   |
| `serializers.py`                    | Pydantic schemas in `*/schemas.py`        |
| `views.py` (APIView / CreateAPIView)| Router functions in `*/router.py`         |
| `urls.py`                           | `app.include_router(...)` in `main.py`    |
| `simplejwt TokenObtainPairView`     | `POST /api/v1/token/`                     |
| `simplejwt TokenRefreshView`        | `POST /api/v1/token/refresh/`             |
| `IsAuthenticated` permission        | `Depends(get_current_user)` in router     |
| `MEDIA_URL / MEDIA_ROOT`            | `app.mount("/media", StaticFiles(...))`   |
| Django Admin                        | Use FastAPI `/docs` or add SQLAdmin       |
| `python manage.py createsuperuser`  | `POST /api/v1/register/`                  |

---

## Endpoints (unchanged URLs)

```
POST /api/v1/register/          Register new user
POST /api/v1/token/             Login → access + refresh tokens
POST /api/v1/token/refresh/     Refresh access token
GET  /api/v1/protected-view/    JWT-protected test endpoint
POST /api/v1/predict/           Stock prediction (ticker in body)
GET  /media/{filename}          Serve generated chart images
```

---

## Protecting the predict endpoint

The `/predict/` endpoint is currently public. To require authentication, open
`prediction/router.py` and uncomment these two lines:

```python
# dependencies=[Depends(get_current_user)],   ← in @router.post(...)
# current_user: User = Depends(get_current_user),  ← in function signature
```

---

## Project structure

```
backend-fastapi/
├── main.py                  # App entry point, CORS, mounts
├── requirements.txt
├── .env
├── core/
│   ├── config.py            # Settings (replaces settings.py)
│   └── database.py          # SQLAlchemy engine + session
├── auth/
│   ├── models.py            # User model
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── security.py          # JWT + password helpers
│   └── router.py            # Auth endpoints
└── prediction/
    ├── schemas.py           # Pydantic request/response schemas
    ├── utils.py             # save_plot() helper
    └── router.py            # /predict/ endpoint
```
