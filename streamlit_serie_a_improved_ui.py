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

# Corrected Remaining Fixtures for Each Team
fixtures = {
    "Inter Milan": ["Udinese (H)", "Parma (A)", "Monza (A)", "Genoa (A)", "Lazio (H)", "Cagliari (A)", "Verona (H)"],
    "Napoli": ["Milan (H)", "Lecce (A)", "Parma (A)", "Udinese (H)", "Genoa (A)", "Lazio (H)", "Cagliari (A)", "Verona (H)"],
    "Atalanta": ["Fiorentina (A)", "Lazio (H)", "Milan (A)", "Udinese (H)", "Genoa (A)", "Cagliari (H)", "Verona (A)", "Empoli (H)"],
    "Bologna": ["Venezia (A)", "Napoli (H)", "Empoli (A)", "Lazio (H)", "Milan (A)", "Udinese (H)", "Genoa (A)"],
    "Juventus": ["Genoa (H)", "Roma (A)", "Fiorentina (A)", "Udinese (H)", "Lazio (H)", "Cagliari (A)", "Verona (H)", "Empoli (A)"],
    "Lazio": ["Torino (H)", "Atalanta (A)", "Genoa (A)", "Empoli (A)", "Juventus (A)", "Inter Milan (A)", "Napoli (A)", "Monza (H)", "Udinese (A)"],
}

# Mapping for mirrored results
result_mapping = {
    "Win": ("Win", "Loss"),
    "Draw": ("Draw", "Draw"),
    "Loss": ("Loss", "Win"),
}

st.title("⚽ Serie A Match-by-Match Standings Simulator")

st.markdown("### Select match results and view updated standings dynamically!")

# Dictionary to store results
match_results = {}

# User-friendly input layout with sections per team
tabs = st.tabs(list(teams.keys()))

for i, team in enumerate(teams.keys()):
    with tabs[i]:
        st.subheader(f"{team}'s Remaining Matches")
        for opponent in fixtures[team]:
            match_key = f"{team}_{opponent}"
            
            # Check if the match has already been entered (to avoid duplicate input)
            if match_key in match_results:
                mirrored_result = match_results[match_key]
                result = result_mapping[mirrored_result][1]  # Automatically set mirrored result
            else:
                result = st.radio(
                    f"Result vs {opponent}",
                    ["Win", "Draw", "Loss"],
                    key=match_key,
                    horizontal=True
                )
            
            # Store result for both teams (mirroring results)
            match_results[match_key] = result

# Apply results to standings
for match_key, result in match_results.items():
    team, opponent = match_key.split("_", 1)
    if result == "Win":
        teams[team] += 3
    elif result == "Draw":
        teams[team] += 1

# Generate final table
final_table = pd.DataFrame(teams.items(), columns=["Team", "Points"])
final_table = final_table.sort_values(by="Points", ascending=False).reset_index(drop=True)

st.subheader("🏆 Projected Final Serie A Standings")
st.dataframe(final_table, height=400)
