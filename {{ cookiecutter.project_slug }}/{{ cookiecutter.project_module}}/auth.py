from core_api.auth import build_current_user
from {{cookiecutter.project_module}}.config import settings

current_user = build_current_user(settings.JWT_SECERT_KEY_FILE, settings.JWT_ALGORITHM)
