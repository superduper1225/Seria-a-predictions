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

# Corrected Remaining Fixtures for Each Team (Matches stored bidirectionally)
fixtures = {
    "Inter Milan": ["Udinese", "Parma", "Monza", "Genoa", "Lazio", "Cagliari", "Verona"],
    "Napoli": ["Milan", "Lecce", "Parma", "Udinese", "Genoa", "Lazio", "Cagliari", "Verona"],
    "Atalanta": ["Fiorentina", "Lazio", "Milan", "Udinese", "Genoa", "Cagliari", "Verona", "Empoli"],
    "Bologna": ["Venezia", "Napoli", "Empoli", "Lazio", "Milan", "Udinese", "Genoa"],
    "Juventus": ["Genoa", "Roma", "Fiorentina", "Udinese", "Lazio", "Cagliari", "Verona", "Empoli"],
    "Lazio": ["Torino", "Atalanta", "Genoa", "Empoli", "Juventus", "Inter Milan", "Napoli", "Monza", "Udinese"],
}

# Mirroring logic to ensure both teams in a match have the same result
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

for i, team in enumerate(teams.keys()):
    with tabs[i]:
        st.subheader(f"{team}'s Remaining Matches")
        
        for opponent in fixtures[team]:
            if opponent not in teams:
                continue  # Ensure only valid teams are processed

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

# Apply results to standings, ensuring only valid teams are updated
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
