from enum import Enum

class ConstructionPhase(str, Enum):
    PRELIMINAR = "preliminar"
    GROSS = "gross"
    FINE = "fine"

print([ConstructionPhase[mn].value for mn in ConstructionPhase._member_names_])