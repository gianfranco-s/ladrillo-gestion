from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from typing import List, Optional, Any, Dict


class ConstructionPhase(StrEnum):
    PRELIMINAR = "preliminar"
    GROSS = "gross"
    FINE = "fine"


@dataclass
class BuildingMaterial:
    material_id: str # PK
    project_id: str # FK → ProjectInfo.project_id
    total_price: float
    phase: ConstructionPhase
    floor_nr: int
    date_bought: date
    date_use_intended: Optional[date] = None
    date_use_real: Optional[date]     = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    """
    Use `metadata` for any extra fields during the PoC,
    e.g. {"supplier": "...", "notes": "..."} 
    """

# Unused for now
# @dataclass
# class ProjectInfo:
#     project_id: str                   # PK
#     name: str                         # was project_name
#     build_surface_m2: float
#     terrain_surface_m2: float
#     floors_total: int
#     materials: List[BuildingMaterial] = field(default_factory=list)
#     created_at: Optional[date] = None
#     updated_at: Optional[date] = None
