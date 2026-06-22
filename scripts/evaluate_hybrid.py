import app.path_setup  # noqa: F401

from app.services.evaluation_service import get_hybrid_evaluation


def main() -> None:
    result = get_hybrid_evaluation()
    print("Hybrid Expert System Evaluation")
    print(f"Eligible consultations: {result['eligible_consultations']}")
    print(f"Agreements: {result['agreements']}")
    print(f"Disagreements: {result['disagreements']}")
    rate = result["agreement_rate"]
    print(f"Agreement rate: {rate}%" if rate is not None else "Agreement rate: unavailable")
    print(f"Basis: {result['evaluation_basis']}")
    print(f"Held-out dataset used: {result['held_out_dataset']}")
    print(f"Limitation: {result['limitation']}")


if __name__ == "__main__":
    main()
