from typing import Protocol


class ProjectInfo:
    name: str
    build_surface: float
    terrain_surface: float
    floors_total: int
    

class BudgetUsd:
    construction_gross: int
    construction_fine: int
    fees_professional: int
    fees_provider: int

    def total(self) -> int:
        return (
            self.construction_gross
            + self.construction_fine
            + self.fees_professional
            + self.fees_provider
        )


class EstimatedTimeMonths:
    project_design: int
    neighborhood_approval: int
    city_approval: int
    construction_gross: int
    construction_fine: int


class ProjectProviders:
    gas: str
    water: str
    electricity: str
    materials: str
    materials_storage: str
    personnel_management: str


class Material:
    name: str
    description: str | None
    unit: str
    quantity: float
    price_per_unit: float
    brand: str | None


class ConstructionTask(Protocol):
    floor_nr: int

    def total_price(self) -> float: ...


class ConstructionPreliminary(ConstructionTask):
    preliminary_tasks: list[Material]
    foundation: list[Material]


class ConstructionGross(ConstructionTask):
    floor_nr: int
    structure: list[Material]
    walls: list[Material]
    roof: list[Material]
    exterior: list[Material]
    # total_price(method)


class ConstructionFine(ConstructionTask):
    floor_nr: int
    bathroom_walls: list[Material]
    interior_openings: list[Material]
    exterior_openings: list[Material]
    interior_equipement: list[Material]
    installations: list[Material]
