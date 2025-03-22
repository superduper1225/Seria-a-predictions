import streamlit as st
import pandas as pd

# ---------------------- SETUP ---------------------- #

# Tracked teams for standings + tab UI
tracked_teams = {
    "Inter Milan": 64,
    "Napoli": 61,
    "Atalanta": 58,
    "Bologna": 53,
    "Juventus": 52,
    "Lazio": 51,
}

# Full fixture list — must cover ALL matches involving tracked teams
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
    ("Bologna", "Inter Milan"),
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
    ("Lazio", "Inter Milan"),
    ("Lazio", "Lecce"),
]

result_mapping = {
    "Win": "Loss",
    "Loss": "Win",
    "Draw": "Draw",
}

# ---------------------- STATE ---------------------- #

if "match_results" not in st.session_state:
    st.session_state.match_results = {}

match_results = st.session_state.match_results

# ---------------------- UI HEADER ---------------------- #

st.title("⚽ Serie A Match-by-Match Standings Simulator")
st.markdown("Simulate all remaining matches for the top 6 teams.")

if st.button("🔄 Reset All Results"):
    st.session_state.match_results = {}
    st.rerun()

# ---------------------- TEAM TABS ---------------------- #

tabs = st.tabs(list(tracked_teams.keys()))

for i, team in enumerate(tracked_teams):
    with tabs[i]:
        st.subheader(f"{team}'s Remaining Matches")

        for fixture_index, match in enumerate(fixtures):
            if team not in match:
                continue

            opponent = match[0] if match[1] == team else match[1]
            owner = match[0]  # Team listed first in fixture "owns" the input

            match_key = f"{match[0]} vs {match[1]}"
            reverse_key = f"{match[1]} vs {match[0]}"
            widget_key = f"{match_key}::{fixture_index}"

            if team == owner:
                result = st.radio(
                    f"Result vs {opponent}",
                    ["Win", "Draw", "Loss"],
                    key=widget_key,
                    horizontal=True
                )
                match_results[match_key] = result
                match_results[reverse_key] = result_mapping[result]
            else:
                if match_key in match_results:
                    mirrored = result_mapping[match_results[match_key]]
                    st.markdown(f"🔒 **Result vs {opponent}: {mirrored} (auto-filled)**")
                else:
                    st.markdown(f"🕒 **Result vs {opponent}: Not yet selected**")

# ---------------------- STANDINGS ---------------------- #

# Track original ranks
original_positions = {
    team: rank for rank, (team, _) in enumerate(
        sorted(tracked_teams.items(), key=lambda x: x[1], reverse=True)
    )
}

updated = tracked_teams.copy()

for match_key, result in match_results.items():
    team, _ = match_key.split(" vs ")
    if team in updated:
        if result == "Win":
            updated[team] += 3
        elif result == "Draw":
            updated[team] += 1

df = pd.DataFrame(updated.items(), columns=["Team", "Points"])
df = df.sort_values(by="Points", ascending=False).reset_index(drop=True)

def get_arrow(team, new_pos):
    old = original_positions[team]
    if new_pos < old:
        return "🔺"
    elif new_pos > old:
        return "🔻"
    return "⏸️"

df["Movement"] = [get_arrow(row["Team"], i) for i, row in df.iterrows()]
df = df[["Movement", "Team", "Points"]]

st.subheader("🏆 Projected Final Serie A Standings")
st.dataframe(df, height=400)
