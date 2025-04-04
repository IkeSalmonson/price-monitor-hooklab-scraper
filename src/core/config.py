#src/core/config.py
"""
Modulo de seleção das configurações de ambiente da aplicação
"""
import os
import pathlib
from functools import lru_cache


class BaseConfig:
    """
    Informações base para funcionamento de acordo com as configurações do container.
    """
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")            # NEW
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")    # NEW


class DevelopmentConfig(BaseConfig):
    """
    Informações especificas para ambiente de desenvolvimento com as configurações do container.
    """
    pass


class ProductionConfig(BaseConfig):
    """
    Informações especificas para ambiente de produção com as configurações do container.
    """
    pass


class TestingConfig(BaseConfig):
    """
    Informações especificas para ambiente de testes com as configurações do container.
    """
    pass


@lru_cache()
def get_settings():
    """
    Determina a configuração a ser usada e guarda com LRU cache
    """
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()

settings = get_settings()
