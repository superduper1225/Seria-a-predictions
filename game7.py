import streamlit as st
import pandas as pd

# -------------------- TEAM SETUP -------------------- #

tracked_teams = {
    "Inter Milan": 64,
    "Napoli": 61,
    "Atalanta": 58,
    "Bologna": 53,
    "Juventus": 52,
    "Lazio": 51,
}

# -------------------- FIXTURES -------------------- #

fixtures = [
    ("Inter Milan", "Udinese"),
    ("Inter Milan", "Parma"),
    ("Inter Milan", "Cagliari"),
    ("Inter Milan", "Bologna"),
    ("Inter Milan", "Roma"),
    ("Inter Milan", "Verona"),
    ("Inter Milan", "Torino"),
    ("Inter Milan", "Lazio"),
    ("Inter Milan", "Como"),

    ("Napoli", "Milan"),
    ("Napoli", "Bologna"),
    ("Napoli", "Empoli"),
    ("Napoli", "Monza"),
    ("Napoli", "Torino"),
    ("Napoli", "Lecce"),
    ("Napoli", "Genoa"),
    ("Napoli", "Parma"),
    ("Napoli", "Cagliari"),

    ("Atalanta", "Fiorentina"),
    ("Atalanta", "Lazio"),
    ("Atalanta", "Bologna"),
    ("Atalanta", "Milan"),
    ("Atalanta", "Lecce"),
    ("Atalanta", "Monza"),
    ("Atalanta", "Roma"),
    ("Atalanta", "Genoa"),
    ("Atalanta", "Parma"),

    ("Bologna", "Venezia"),
    ("Bologna", "Napoli"),
    ("Bologna", "Atalanta"),
    ("Bologna", "Inter Milan"),
    ("Bologna", "Udinese"),
    ("Bologna", "Juventus"),
    ("Bologna", "Milan"),
    ("Bologna", "Fiorentina"),
    ("Bologna", "Genoa"),

    ("Juventus", "Genoa"),
    ("Juventus", "Roma"),
    ("Juventus", "Lecce"),
    ("Juventus", "Parma"),
    ("Juventus", "Monza"),
    ("Juventus", "Bologna"),
    ("Juventus", "Lazio"),
    ("Juventus", "Udinese"),
    ("Juventus", "Venezia"),

    ("Lazio", "Torino"),
    ("Lazio", "Atalanta"),
    ("Lazio", "Roma"),
    ("Lazio", "Genoa"),
    ("Lazio", "Parma"),
    ("Lazio", "Empoli"),
    ("Lazio", "Juventus"),
    ("Lazio", "Inter Milan"),
    ("Lazio", "Lecce"),
]

result_mapping = {
    "Win": "Loss",
    "Loss": "Win",
    "Draw": "Draw",
}

# -------------------- SESSION INIT -------------------- #

if "match_results" not in st.session_state:
    st.session_state.match_results = {}

match_results = st.session_state.match_results

# -------------------- HEADER -------------------- #

st.title("⚽ Serie A Match-by-Match Standings Simulator")
st.markdown("Simulate all fixtures. Only the top 6 teams are shown in the table.")

if st.button("🔄 Reset All Results"):
    st.session_state.match_results = {}
    st.rerun()

# -------------------- TEAM TABS -------------------- #

tabs = st.tabs(list(tracked_teams.keys()))

for i, team in enumerate(tracked_teams.keys()):
    with tabs[i]:
        st.subheader(f"{team}'s Remaining Fixtures")

        for fixture_index, match in enumerate(fixtures):
            if team not in match:
                continue

            opponent = match[1] if match[0] == team else match[0]
            match_key = f"{match[0]} vs {match[1]}"
            reverse_key = f"{match[1]} vs {match[0]}"
            widget_key = f"match::{fixture_index}"  # unique key per fixture

            # Only render input if team owns the match (first in tuple)
            if team == match[0]:
                if widget_key not in st.session_state:
                    result = st.radio(
                        f"Result vs {opponent}",
                        ["Win", "Draw", "Loss"],
                        key=widget_key,
                        horizontal=True
                    )
                    match_results[match_key] = result
                    match_results[reverse_key] = result_mapping[result]
                else:
                    result = st.session_state[widget_key]
                    match_results[match_key] = result
                    match_results[reverse_key] = result_mapping[result]
            else:
                if match_key in match_results:
                    mirrored_result = result_mapping[match_results[match_key]]
                    st.markdown(f"🔒 **Result vs {opponent}: {mirrored_result} (auto-filled)**")
                else:
                    st.markdown(f"🕒 **Result vs {opponent}: Not yet selected**")

# -------------------- STANDINGS -------------------- #

# Save original order
original_ranks = {
    team: i for i, (team, _) in enumerate(
        sorted(tracked_teams.items(), key=lambda x: x[1], reverse=True)
    )
}

updated_points = tracked_teams.copy()

for match_key, result in match_results.items():
    team, _ = match_key.split(" vs ")
    if team in updated_points:
        if result == "Win":
            updated_points[team] += 3
        elif result == "Draw":
            updated_points[team] += 1

df = pd.DataFrame(updated_points.items(), columns=["Team", "Points"])
df = df.sort_values(by="Points", ascending=False).reset_index(drop=True)

def get_movement_icon(team, new_idx):
    old_idx = original_ranks[team]
    if new_idx < old_idx:
        return "🔺"
    elif new_idx > old_idx:
        return "🔻"
    return "⏸️"

df["Movement"] = [get_movement_icon(row["Team"], i) for i, row in df.iterrows()]
df = df[["Movement", "Team", "Points"]]

st.subheader("🏆 Projected Final Serie A Standings")
st.dataframe(df, height=400)
