from enum import StrEnum
from datetime import datetime
class ProjectInfo:
    project_id: int
    project_name: str
    build_surface_m2: float
    terrain_surface_m2: float
    floors_total: int


class ConstructionPhase(StrEnum):
    PRELIMINARY = "PRELIMINARY"
    GROSS = "GROSS"
    FINE = "FINE"


class Material:
    material_id: int
    material_name: str
    description: str | None
    unit: str
    quantity: float
    unit_price: float
    brand: str | None
    provider: str | None


class ConstructionTask:
    floor_nr: int
    date_bought: datetime
    date_use_intended: datetime
    date_use_real: datetime
    phase_type: ConstructionPhase

    # materials: list[Material]

    def total_price(self) -> float: ...


class ConstructionPreliminary(ConstructionTask):
    material_type = 'any of ["preliminary_tasks", "foundation"]'
    materials: list[Material]

class ConstructionGross(ConstructionTask):
    material_type = 'any of  ["structure", "walls", "roof", "exterior"]'
    materials: list[Material]


class ConstructionFine(ConstructionTask):
    material_type = 'any of ["bathroom_walls", "interior_openings", "exterior_openings", "interior_equipement", "installations"]'
    materials: list[Material]
    
# class BudgetUsd:
#     # this could be a property of ProjectInfo
#     construction_gross: int
#     construction_fine: int
#     fees_professional: int
#     fees_provider: int

#     def total(self) -> int:
#         return (
#             self.construction_gross
#             + self.construction_fine
#             + self.fees_professional
#             + self.fees_provider
#         )


# class EstimatedTimeMonths:
#     # this could be a property of ProjectInfo
#     project_design: int
#     neighborhood_approval: int
#     city_approval: int
#     construction_gross: int
#     construction_fine: int


# class ProjectProviders:
#     # this could be a property of ProjectInfo
#     gas: str
#     water: str
#     electricity: str
#     materials: str
#     materials_storage: str
#     personnel_management: str

