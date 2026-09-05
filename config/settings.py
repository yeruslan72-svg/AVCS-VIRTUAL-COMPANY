"""
AVCS VIRTUAL COMPANY
Configuration Settings

FUNCTION:
- Centralized configuration for all components
- Environment variables
- Default settings
"""

import os
from typing import Dict, Any
from datetime import datetime


class Settings:
    """Centralized configuration for AVCS Virtual Company."""

    # Application
    APP_NAME = "AVCS VIRTUAL COMPANY"
    APP_VERSION = "0.1.0"
    APP_ENV = os.getenv("APP_ENV", "development")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Departments
    DEPARTMENT_CONFIG: Dict[str, Any] = {
        "LOOKOUT Dpt.": {
            "confidence_threshold": 0.7,
            "max_observations": 100
        },
        "CHARTS Dpt.": {
            "confidence_threshold": 0.7,
            "max_contexts": 50
        },
        "GYRO Dpt.": {
            "confidence_threshold": 0.7,
            "tracking_window": 60
        },
        "NAVIGATOR Dpt.": {
            "confidence_threshold": 0.7,
            "threat_timeout": 120
        },
        "COMPASS Dpt.": {
            "confidence_threshold": 0.7,
            "max_alternatives": 5
        },
        "HELM Dpt.": {
            "authority": "EXECUTION_ONLY",
            "execution_timeout": 30
        },
        "CAPTAIN Dpt.": {
            "authority": "HUMAN_AUTHORITY_INTERFACE",
            "decision_timeout": 300
        }
    }

    # Dispatcher
    DISPATCHER_CONFIG = {
        "routing_mode": "dynamic",
        "parallel_processing": True,
        "timeout": 30
    }

    # Aggregator
    AGGREGATOR_CONFIG = {
        "preserve_conflicts": True,
        "confidence_weighted": True,
        "min_departments": 3
    }

    # Authority Gate
    AUTHORITY_GATE_CONFIG = {
        "require_human_approval": True,
        "allow_delegation": False,
        "timeout": 300
    }

    # Records
    RECORDS_CONFIG = {
        "store_path": "data/records/",
        "format": "json",
        "immutable": True
    }

    @classmethod
    def get_department_config(cls, department_name: str) -> Dict[str, Any]:
        """Get configuration for a specific department."""
        return cls.DEPARTMENT_CONFIG.get(department_name, {})

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "app_env": cls.APP_ENV,
            "log_level": cls.LOG_LEVEL,
            "departments": cls.DEPARTMENT_CONFIG,
            "dispatcher": cls.DISPATCHER_CONFIG,
            "aggregator": cls.AGGREGATOR_CONFIG,
            "authority_gate": cls.AUTHORITY_GATE_CONFIG,
            "records": cls.RECORDS_CONFIG
        }


# Default settings instance
settings = Settings()
