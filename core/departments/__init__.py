"""
AVCS VIRTUAL COMPANY
Departments Package

Contains all seven INS Departments:
- LOOKOUT Dpt.
- CHARTS Dpt.
- GYRO Dpt.
- NAVIGATOR Dpt.
- COMPASS Dpt.
- HELM Dpt.
- CAPTAIN Dpt.
"""

from core.departments.base import BaseDepartment
from core.departments.lookout import LookoutDepartment
from core.departments.charts import ChartsDepartment
from core.departments.gyro import GyroDepartment
from core.departments.navigator import NavigatorDepartment
from core.departments.compass import CompassDepartment
from core.departments.helm import HelmDepartment
from core.departments.captain import CaptainDepartment

__all__ = [
    "BaseDepartment",
    "LookoutDepartment",
    "ChartsDepartment",
    "GyroDepartment",
    "NavigatorDepartment",
    "CompassDepartment",
    "HelmDepartment",
    "CaptainDepartment",
]
