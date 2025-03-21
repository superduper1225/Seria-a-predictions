import streamlit as st
import pandas as pd

# ---------------------- SETUP ---------------------- #

# Initial standings as of March 19, 2025
original_teams = {
    "Inter Milan": 64,
    "Napoli": 61,
    "Atalanta": 58,
    "Bologna": 53,
    "Juventus": 52,
    "Lazio": 51,
}

# Fixtures
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
    ("Bologna", "Inter"),
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
    ("Lazio", "Inter"),
    ("Lazio", "Lecce"),
]

result_mapping = {
    "Win": "Loss",
    "Loss": "Win",
    "Draw": "Draw",
}

# ---------------------- STATE & RESET ---------------------- #

if "match_results" not in st.session_state:
    st.session_state.match_results = {}

match_results = st.session_state.match_results

st.title("⚽ Serie A Match-by-Match Standings Simulator")
st.markdown("### Select match results and view updated standings dynamically!")

if st.button("🔄 Reset All Results"):
    st.session_state.match_results = {}
    st.rerun()

# ---------------------- TEAM TABS ---------------------- #

tabs = st.tabs(list(original_teams.keys()))

for i, team in enumerate(original_teams.keys()):
    with tabs[i]:
        st.subheader(f"{team}'s Remaining Matches")

        for match in fixtures:
            if team in match:
                opponent = match[0] if match[1] == team else match[1]

                # Consistently sort teams to get a unique widget key
                key_team1, key_team2 = sorted([team, opponent])
                widget_key = f"{key_team1}_vs_{key_team2}"

                # Only create the radio once (in the "owning" team's tab)
                if team == key_team1:
                    result = st.radio(
                        f"Result vs {opponent}",
                        ["Win", "Draw", "Loss"],
                        key=widget_key,
                        horizontal=True
                    )
                    match_results[f"{team} vs {opponent}"] = result
                    match_results[f"{opponent} vs {team}"] = result_mapping[result]
                else:
                    if f"{team} vs {opponent}" in match_results:
                        mirrored_result = match_results[f"{team} vs {opponent}"]
                        st.markdown(f"🔒 **Result vs {opponent}: {mirrored_result} (auto-filled)**")
                    else:
                        st.markdown(f"🕒 **Result vs {opponent}: Not yet selected**")

# ---------------------- STANDINGS ---------------------- #

original_positions = {
    team: rank for rank, (team, _) in enumerate(
        sorted(original_teams.items(), key=lambda x: x[1], reverse=True)
    )
}

updated_standings = original_teams.copy()

for match_key, result in match_results.items():
    team, opponent = match_key.split(" vs ")
    if team in updated_standings:
        if result == "Win":
            updated_standings[team] += 3
        elif result == "Draw":
            updated_standings[team] += 1

final_table = pd.DataFrame(updated_standings.items(), columns=["Team", "Points"])
final_table = final_table.sort_values(by="Points", ascending=False).reset_index(drop=True)

def get_movement_icon(team, new_rank):
    old_rank = original_positions[team]
    if new_rank < old_rank:
        return "🔺"
    elif new_rank > old_rank:
        return "🔻"
    else:
        return "⏸️"

final_table["Movement"] = [
    get_movement_icon(row["Team"], idx) for idx, row in final_table.iterrows()
]

final_table = final_table[["Movement", "Team", "Points"]]

# ---------------------- DISPLAY ---------------------- #

st.subheader("🏆 Projected Final Serie A Standings")
st.dataframe(final_table, height=400)
