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

# Remaining fixtures for each team
fixtures = {
    "Inter Milan": ["Parma (A)", "Bologna (A)", "Lecce (H)", "Monza (A)", "Udinese (H)", "Genoa (A)", "Lazio (H)", "Cagliari (A)", "Verona (H)"],
    "Napoli": ["Bologna (A)", "Lecce (A)", "Monza (H)", "Parma (A)", "Udinese (H)", "Genoa (A)", "Lazio (H)", "Cagliari (A)", "Verona (H)"],
    "Atalanta": ["Lazio (H)", "Milan (A)", "Monza (A)", "Udinese (H)", "Genoa (A)", "Cagliari (H)", "Verona (A)", "Empoli (H)", "Fiorentina (A)"],
    "Bologna": ["Napoli (H)", "Inter (H)", "Fiorentina (A)", "Cagliari (H)", "Empoli (A)", "Lazio (H)", "Milan (A)", "Udinese (H)", "Genoa (A)"],
    "Juventus": ["Fiorentina (A)", "Roma (A)", "Parma (A)", "Udinese (H)", "Genoa (A)", "Lazio (H)", "Cagliari (A)", "Verona (H)", "Empoli (A)"],
    "Lazio": ["Atalanta (A)", "Genoa (A)", "Empoli (A)", "Juventus (A)", "Inter (A)", "Napoli (A)", "Bologna (A)", "Monza (H)", "Udinese (A)"],
}

st.title("Serie A Match-by-Match Standings Simulator")

st.write("Enter the results of each remaining match, and the standings will be updated dynamically.")

# Match result inputs
for team, match_list in fixtures.items():
    st.subheader(f"{team}'s Remaining Matches")
    for match in match_list:
        result = st.selectbox(f"Result for {team} vs {match} (W=3, D=1, L=0)", ["Win", "Draw", "Loss"], key=f"{team}_{match}")
        if result == "Win":
            teams[team] += 3
        elif result == "Draw":
            teams[team] += 1

# Generate final table
final_table = pd.DataFrame(teams.items(), columns=["Team", "Points"])
final_table = final_table.sort_values(by="Points", ascending=False).reset_index(drop=True)

st.subheader("Projected Final Serie A Standings")
st.dataframe(final_table)
