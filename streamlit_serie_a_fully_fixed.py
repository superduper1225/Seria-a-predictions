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
