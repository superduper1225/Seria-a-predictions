import streamlit as st
import pandas as pd

# Initial Serie A Standings (as of March 19, 2025)
teams = {
    "Inter Milan": 64,
    "Napoli": 61,
    "Atalanta": 58,
    "Bologna": 53,
    "Juventus": 52,
    "Lazio": 51,
}

# Remaining fixtures (all matches for each team)
fixtures = [
    ("Inter Milan", "Parma"),
    ("Inter Milan", "Bologna"),
    ("Inter Milan", "Lecce"),
    ("Inter Milan", "Monza"),
    ("Inter Milan", "Udinese"),
    ("Inter Milan", "Genoa"),
    ("Inter Milan", "Lazio"),
    ("Inter Milan", "Cagliari"),
    ("Inter Milan", "Verona"),
    
    ("Napoli", "Bologna"),
    ("Napoli", "Lecce"),
    ("Napoli", "Monza"),
    ("Napoli", "Parma"),
    ("Napoli", "Udinese"),
    ("Napoli", "Genoa"),
    ("Napoli", "Lazio"),
    ("Napoli", "Cagliari"),
    ("Napoli", "Verona"),
    
    ("Atalanta", "Lazio"),
    ("Atalanta", "Milan"),
    ("Atalanta", "Monza"),
    ("Atalanta", "Udinese"),
    ("Atalanta", "Genoa"),
    ("Atalanta", "Cagliari"),
    ("Atalanta", "Verona"),
    ("Atalanta", "Empoli"),
    ("Atalanta", "Fiorentina"),
    
    ("Bologna", "Napoli"),
    ("Bologna", "Inter Milan"),
    ("Bologna", "Fiorentina"),
    ("Bologna", "Cagliari"),
    ("Bologna", "Empoli"),
    ("Bologna", "Lazio"),
    ("Bologna", "Milan"),
    ("Bologna", "Udinese"),
    ("Bologna", "Genoa"),
    
    ("Juventus", "Fiorentina"),
    ("Juventus", "Roma"),
    ("Juventus", "Parma"),
    ("Juventus", "Udinese"),
    ("Juventus", "Genoa"),
    ("Juventus", "Lazio"),
    ("Juventus", "Cagliari"),
    ("Juventus", "Verona"),
    ("Juventus", "Empoli"),
    
    ("Lazio", "Atalanta"),
    ("Lazio", "Genoa"),
    ("Lazio", "Empoli"),
    ("Lazio", "Juventus"),
    ("Lazio", "Inter Milan"),
    ("Lazio", "Napoli"),
    ("Lazio", "Bologna"),
    ("Lazio", "Monza"),
    ("Lazio", "Udinese"),
]

# Mapping for mirrored results
result_mapping = {
    "Win": ("Win", "Loss"),
    "Draw": ("Draw", "Draw"),
    "Loss": ("Loss", "Win"),
}

st.title("Serie A Match-by-Match Standings Simulator")

st.write("Select the result of each match, and standings will update dynamically.")

# Dictionary to store results
match_results = {}

# Collect user input for each fixture and apply mirrored results
for team1, team2 in fixtures:
    st.subheader(f"{team1} vs {team2}")
    match_key = f"{team1}_{team2}"
    
    # Check if the match has already been entered (to avoid duplicate input)
    if (team2, team1) in match_results:
        mirrored_result = match_results[(team2, team1)]
        result = result_mapping[mirrored_result][1]  # Automatically set result based on previous selection
    else:
        result = st.selectbox(f"Select result for {team1} vs {team2}", ["Win", "Draw", "Loss"], key=match_key)
    
    # Store result for both teams (mirroring results)
    match_results[(team1, team2)] = result
    match_results[(team2, team1)] = result_mapping[result][1]

# Apply results to standings
for (team1, team2), result in match_results.items():
    if result == "Win":
        teams[team1] += 3
    elif result == "Draw":
        teams[team1] += 1

# Generate final table
final_table = pd.DataFrame(teams.items(), columns=["Team", "Points"])
final_table = final_table.sort_values(by="Points", ascending=False).reset_index(drop=True)

st.subheader("Projected Final Serie A Standings")
st.dataframe(final_table)
