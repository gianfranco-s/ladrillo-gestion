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
    name: str
    purchase_date: date
    intended_use_date: Optional[date] = None
    real_use_date: Optional[date]     = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    """
    Use `metadata` for any extra fields during the PoC,
    e.g. {"supplier": "...", "notes": "..."} 
    """

@dataclass
class ProjectInfo:
    project_id: str                   # PK
    name: str                         # was project_name
    build_surface_m2: float
    terrain_surface_m2: float
    floors_total: int
    materials: List[BuildingMaterial] = field(default_factory=list)
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    """
    Once you stabilize your schema you can
    set created_at/updated_at automatically
    (e.g. in a DB trigger or in your service layer).
    """
