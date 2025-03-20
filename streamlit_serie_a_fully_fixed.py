import streamlit as st
import pandas as pd

# Corrected Serie A Standings as of March 19, 2025
teams = {
    "Inter Milan": 64,
    "Napoli": 61,
    "Atalanta": 58,
    "Bologna": 53,
    "Juventus": 52,
    "Lazio": 51,
}

# Corrected Remaining Fixtures for Each Team (Bidirectional Matching)
fixtures = [
    ("Inter Milan", "Udinese"),
    ("Inter Milan", "Parma"),
    ("Inter Milan", "Monza"),
    ("Inter Milan", "Genoa"),
    ("Inter Milan", "Lazio"),
    ("Inter Milan", "Cagliari"),
    ("Inter Milan", "Verona"),

    ("Napoli", "Milan"),
    ("Napoli", "Lecce"),
    ("Napoli", "Parma"),
    ("Napoli", "Udinese"),
    ("Napoli", "Genoa"),
    ("Napoli", "Lazio"),
    ("Napoli", "Cagliari"),
    ("Napoli", "Verona"),

    ("Atalanta", "Fiorentina"),
    ("Atalanta", "Lazio"),
    ("Atalanta", "Milan"),
    ("Atalanta", "Udinese"),
    ("Atalanta", "Genoa"),
    ("Atalanta", "Cagliari"),
    ("Atalanta", "Verona"),
    ("Atalanta", "Empoli"),

    ("Bologna", "Venezia"),
    ("Bologna", "Napoli"),
    ("Bologna", "Empoli"),
    ("Bologna", "Lazio"),
    ("Bologna", "Milan"),
    ("Bologna", "Udinese"),
    ("Bologna", "Genoa"),

    ("Juventus", "Genoa"),
    ("Juventus", "Roma"),
    ("Juventus", "Fiorentina"),
    ("Juventus", "Udinese"),
    ("Juventus", "Lazio"),
    ("Juventus", "Cagliari"),
    ("Juventus", "Verona"),
    ("Juventus", "Empoli"),

    ("Lazio", "Torino"),
    ("Lazio", "Atalanta"),
    ("Lazio", "Genoa"),
    ("Lazio", "Empoli"),
    ("Lazio", "Juventus"),
    ("Lazio", "Inter Milan"),
    ("Lazio", "Napoli"),
    ("Lazio", "Monza"),
    ("Lazio", "Udinese"),
]

# Mapping for mirroring results
result_mapping = {
    "Win": "Loss",
    "Loss": "Win",
    "Draw": "Draw",
}

# Dictionary to store results and ensure synchronization across both teams
match_results = {}

st.title("⚽ Serie A Match-by-Match Standings Simulator")

st.markdown("### Select match results and view updated standings dynamically!")

# Creating UI tabs for teams
tabs = st.tabs(list(teams.keys()))

# Process each team's matches
for i, team in enumerate(teams.keys()):
    with tabs[i]:
        st.subheader(f"{team}'s Remaining Matches")
        
        for match in fixtures:
            if team in match:
                opponent = match[0] if match[1] == team else match[1]

                match_key = f"{team} vs {opponent}"
                reverse_match_key = f"{opponent} vs {team}"

                # Ensure synchronized result across both teams
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

# Apply results to standings, ensuring valid teams are updated
for match_key, result in match_results.items():
    team, opponent = match_key.split(" vs ")

    if team in teams:
        if result == "Win":
            teams[team] += 3
        elif result == "Draw":
            teams[team] += 1

# Generate final table
final_table = pd.DataFrame(teams.items(), columns=["Team", "Points"])
final_table = final_table.sort_values(by="Points", ascending=False).reset_index(drop=True)

st.subheader("🏆 Projected Final Serie A Standings")
st.dataframe(final_table, height=400)
