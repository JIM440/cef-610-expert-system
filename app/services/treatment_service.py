from app.repositories import disease_repository as repo


class TreatmentService:
    def get_for_disease(self, disease_id: int) -> list[dict]:
        return repo.get_treatments_for_disease(disease_id)
