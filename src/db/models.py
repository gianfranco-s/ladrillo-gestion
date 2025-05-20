from dataclasses import dataclass, asdict
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
    date_bought: date | None = None
    date_use_intended:date | None = None
    date_use_real: date | None = None
    # metadata: Dict[str, Any] = field(default_factory=dict)  # for extra fields like supplier, notes, etc

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

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
