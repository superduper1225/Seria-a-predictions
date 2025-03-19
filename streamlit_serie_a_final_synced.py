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
    "Inter Milan": ["Udinese (H)", "Parma (A)", "Monza (A)", "Genoa (A)", "Lazio (H)", "Cagliari (A)", "Verona (H)"],
    "Napoli": ["Milan (H)", "Lecce (A)", "Parma (A)", "Udinese (H)", "Genoa (A)", "Lazio (H)", "Cagliari (A)", "Verona (H)"],
    "Atalanta": ["Fiorentina (A)", "Lazio (H)", "Milan (A)", "Udinese (H)", "Genoa (A)", "Cagliari (H)", "Verona (A)", "Empoli (H)"],
    "Bologna": ["Venezia (A)", "Napoli (H)", "Empoli (A)", "Lazio (H)", "Milan (A)", "Udinese (H)", "Genoa (A)"],
    "Juventus": ["Genoa (H)", "Roma (A)", "Fiorentina (A)", "Udinese (H)", "Lazio (H)", "Cagliari (A)", "Verona (H)", "Empoli (A)"],
    "Lazio": ["Torino (H)", "Atalanta (A)", "Genoa (A)", "Empoli (A)", "Juventus (A)", "Inter Milan (A)", "Napoli (A)", "Monza (H)", "Udinese (A)"],
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

# Apply results to standings
for match_key, result in match_results.items():
    team, opponent = match_key.split(" vs ")
    
    if result == "Win":
        teams[team] += 3
    elif result == "Draw":
        teams[team] += 1

# Generate final table
final_table = pd.DataFrame(teams.items(), columns=["Team", "Points"])
final_table = final_table.sort_values(by="Points", ascending=False).reset_index(drop=True)

st.subheader("🏆 Projected Final Serie A Standings")
st.dataframe(final_table, height=400)
