"""
Módulo de servicios de autenticación y registro.

Este módulo contiene todos los servicios e interfaces relacionados con
la autenticación y registro de usuarios, siguiendo los principios SOLID.
"""

from .interfaces import AuthServiceInterface, RegistrationServiceInterface
from .http_client_interface import HttpClientInterface
from .urllib_http_client import UrllibHttpClient
from .api_auth_service import ApiAuthService
from .api_registration_service import ApiRegistrationService
from .dashboard_logger import DashboardLogger

__all__ = [
    'AuthServiceInterface',
    'RegistrationServiceInterface', 
    'HttpClientInterface',
    'UrllibHttpClient',
    'ApiAuthService',
    'ApiRegistrationService',
    'DashboardLogger'
]
