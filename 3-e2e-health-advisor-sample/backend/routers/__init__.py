from fastapi import APIRouter

from .molecular_design import router as molecular_router
from .clinical_trials import router as trials_router
from .automated_testing import router as testing_router
from .supply_chain import router as supply_router

__all__ = [
    'molecular_router',
    'trials_router',
    'testing_router',
    'supply_router'
]
