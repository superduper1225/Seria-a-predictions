import streamlit as st
import pandas as pd

# Original Serie A Standings as of March 19, 2025
original_teams = {
    "Inter Milan": 64,
    "Napoli": 61,
    "Atalanta": 58,
    "Bologna": 53,
    "Juventus": 52,
    "Lazio": 51,
}

# Fixtures (unchanged)
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

match_results = {}

st.title("⚽ Serie A Match-by-Match Standings Simulator")
st.markdown("### Select match results and view updated standings dynamically!")

tabs = st.tabs(list(original_teams.keys()))

# Radio button UI
for i, team in enumerate(original_teams.keys()):
    with tabs[i]:
        st.subheader(f"{team}'s Remaining Matches")
        for match in fixtures:
            if team in match:
                opponent = match[0] if match[1] == team else match[1]
                match_key = f"{team} vs {opponent}"
                reverse_match_key = f"{opponent} vs {team}"

                if reverse_match_key in match_results:
                    result = match_results[reverse_match_key]
                else:
                    result = st.radio(
                        f"Result vs {opponent}",
                        ["Win", "Draw", "Loss"],
                        key=match_key,
                        horizontal=True
                    )
                    match_results[match_key] = result
                    match_results[reverse_match_key] = result_mapping[result]

# Initialize fresh standings
updated_standings = original_teams.copy()

# Apply match results
for match_key, result in match_results.items():
    team, opponent = match_key.split(" vs ")

    if team in updated_standings:
        if result == "Win":
            updated_standings[team] += 3
        elif result == "Draw":
            updated_standings[team] += 1
    # You can also extend to track points for opponents if needed

# Display standings
final_table = pd.DataFrame(updated_standings.items(), columns=["Team", "Points"])
final_table = final_table.sort_values(by="Points", ascending=False).reset_index(drop=True)

st.subheader("🏆 Projected Final Serie A Standings")
st.dataframe(final_table, height=400)
