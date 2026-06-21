import streamlit as st


def render_symptom_selector(symptoms: list[dict]) -> list[int]:
    st.subheader("Observed symptoms")
    names = [s["name"] for s in symptoms]
    selected = st.multiselect("Select all that apply", names)
    name_to_id = {s["name"]: s["id"] for s in symptoms}
    return [name_to_id[n] for n in selected]


def render_environment_selector(env_rows: list[dict]) -> list[int]:
    st.subheader("Environmental conditions")
    conditions: dict[str, list[dict]] = {}
    for row in env_rows:
        conditions.setdefault(row["condition_name"], []).append(row)

    selected_ids: list[int] = []
    for condition_name, values in conditions.items():
        options = {v["value_name"]: v["value_id"] for v in values}
        choice = st.selectbox(condition_name, ["—"] + list(options.keys()))
        if choice != "—":
            selected_ids.append(options[choice])
    return selected_ids
