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

# Fixtures (Matches where teams play each other)
fixtures = [
    ("Inter Milan", "Bologna"),
    ("Napoli", "Bologna"),
    ("Atalanta", "Lazio"),
    ("Juventus", "Lazio"),
    ("Inter Milan", "Lazio"),
    ("Napoli", "Lazio"),
    ("Juventus", "Bologna"),
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

# Collect user input for each fixture
for team1, team2 in fixtures:
    st.subheader(f"{team1} vs {team2}")
    match_key = f"{team1}_{team2}"
    result = st.selectbox(f"Select result for {team1}", ["Win", "Draw", "Loss"], key=match_key)

    # Automatically assign the mirrored result
    mirrored_result = result_mapping[result][1]

    # Store results
    match_results[(team1, team2)] = result
    match_results[(team2, team1)] = mirrored_result

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
