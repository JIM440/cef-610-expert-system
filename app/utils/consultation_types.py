FARMER_SELF = "FARMER_SELF"
ADMIN_FOR_FARMER = "ADMIN_FOR_FARMER"
ADMIN_GENERAL = "ADMIN_GENERAL"

IMAGE_FARMER_SELF = "IMAGE_FARMER_SELF"
IMAGE_ADMIN_FOR_FARMER = "IMAGE_ADMIN_FOR_FARMER"
IMAGE_ADMIN_GENERAL = "IMAGE_ADMIN_GENERAL"

SYMPTOM_TYPES = frozenset({FARMER_SELF, ADMIN_FOR_FARMER, ADMIN_GENERAL})
IMAGE_TYPES = frozenset({IMAGE_FARMER_SELF, IMAGE_ADMIN_FOR_FARMER, IMAGE_ADMIN_GENERAL})

LABELS = {
    FARMER_SELF: "Farmer self-diagnosis",
    ADMIN_FOR_FARMER: "Admin diagnosis for farmer",
    ADMIN_GENERAL: "Admin general diagnosis",
    IMAGE_FARMER_SELF: "Farmer image diagnosis",
    IMAGE_ADMIN_FOR_FARMER: "Admin image diagnosis for farmer",
    IMAGE_ADMIN_GENERAL: "Admin general image diagnosis",
}


def is_image_consultation(consultation_type: str | None) -> bool:
    return consultation_type in IMAGE_TYPES


def is_symptom_consultation(consultation_type: str | None) -> bool:
    return consultation_type in SYMPTOM_TYPES
