from enum import StrEnum
from datetime import datetime


class BuildingMaterialDetails:
    material_id: int  # FK
    material_name: str
    description: str | None
    unit: str
    quantity: float
    unit_price: float
    brand: str | None
    provider: str | None


class BudgetUsd:
    # this could be a property of ProjectInfo
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
    # this could be a property of ProjectInfo
    project_design: int
    neighborhood_approval: int
    city_approval: int
    construction_gross: int
    construction_fine: int


class ProjectProviders:
    # this could be a property of ProjectInfo
    gas: str
    water: str
    electricity: str
    materials: str
    materials_storage: str
    personnel_management: str

