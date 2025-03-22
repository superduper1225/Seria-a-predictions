import streamlit as st
import pandas as pd
from collections import defaultdict

# -------------------- TRACKED TEAMS -------------------- #
tracked_teams = {
    "Inter Milan": 64,
    "Napoli": 61,
    "Atalanta": 58,
    "Bologna": 53,
    "Juventus": 52,
    "Lazio": 51,
}

# -------------------- CLEAN WEEKLY FIXTURES (FROM USER DATA) -------------------- #
fixtures = [
    ("Week 30", "Inter Milan", "Udinese"), ("Week 30", "Napoli", "Milan"), ("Week 30", "Atalanta", "Fiorentina"),
    ("Week 30", "Bologna", "Venezia"), ("Week 30", "Juventus", "Genoa"), ("Week 30", "Lazio", "Torino"),

    ("Week 31", "Inter Milan", "Parma"), ("Week 31", "Napoli", "Bologna"), ("Week 31", "Atalanta", "Lazio"),
    ("Week 31", "Juventus", "Roma"),

    ("Week 32", "Inter Milan", "Cagliari"), ("Week 32", "Napoli", "Empoli"), ("Week 32", "Atalanta", "Bologna"),
    ("Week 32", "Juventus", "Lecce"), ("Week 32", "Lazio", "Roma"),

    ("Week 33", "Inter Milan", "Bologna"), ("Week 33", "Napoli", "Monza"), ("Week 33", "Atalanta", "Milan"),
    ("Week 33", "Juventus", "Parma"), ("Week 33", "Lazio", "Genoa"),

    ("Week 34", "Inter Milan", "Roma"), ("Week 34", "Napoli", "Torino"), ("Week 34", "Atalanta", "Lecce"),
    ("Week 34", "Bologna", "Udinese"), ("Week 34", "Juventus", "Monza"), ("Week 34", "Lazio", "Parma"),

    ("Week 35", "Inter Milan", "Verona"), ("Week 35", "Napoli", "Lecce"), ("Week 35", "Atalanta", "Monza"),
    ("Week 35", "Bologna", "Juventus"), ("Week 35", "Lazio", "Empoli"),

    ("Week 36", "Inter Milan", "Torino"), ("Week 36", "Napoli", "Genoa"), ("Week 36", "Atalanta", "Roma"),
    ("Week 36", "Bologna", "Milan"), ("Week 36", "Juventus", "Lazio"),

    ("Week 37", "Inter Milan", "Lazio"), ("Week 37", "Napoli", "Parma"), ("Week 37", "Atalanta", "Genoa"),
    ("Week 37", "Bologna", "Fiorentina"), ("Week 37", "Juventus", "Udinese"),

    ("Week 38", "Inter Milan", "Como"), ("Week 38", "Napoli", "Cagliari"), ("Week 38", "Atalanta", "Parma"),
    ("Week 38", "Bologna", "Genoa"), ("Week 38", "Juventus", "Venezia"), ("Week 38", "Lazio", "Lecce"),
]

# -------------------- SESSION INIT -------------------- #
if "match_results" not in st.session_state:
    st.session_state.match_results = {}
match_results = st.session_state.match_results

# -------------------- UI HEADER -------------------- #
st.title("⚽ Serie A Fixture Simulator")
st.markdown("Simulate all remaining matches. Standings reflect only the top 6 teams.")

if st.button("🔄 Reset All Results"):
    for key in list(st.session_state.keys()):
        if "::" in key:
            del st.session_state[key]
    st.session_state.match_results = {}
    st.rerun()

# -------------------- MATCH SELECTION -------------------- #
st.subheader("📅 Match Results by Week")
weekly_results = defaultdict(list)

for i, (week, team1, team2) in enumerate(fixtures):
    match_key = f"{team1} vs {team2}"
    reverse_key = f"{team2} vs {team1}"
    widget_key = f"{i}::{team1}::{team2}"

    if i == 0 or fixtures[i - 1][0] != week:
        st.markdown(f"### 🗓️ {week}")

    result = st.radio(
        f"{team1} vs {team2}",
        ["Win", "Draw", "Loss"],
        key=widget_key,
        horizontal=True
    )
    match_results[match_key] = result
    match_results[reverse_key] = {"Win": "Loss", "Loss": "Win", "Draw": "Draw"}[result]
    weekly_results[week].append((team1, result))

# -------------------- STANDINGS AFTER EACH WEEK -------------------- #
st.subheader("📊 Standings After Each Week")
original_ranks = {
    team: idx for idx, (team, _) in enumerate(
        sorted(tracked_teams.items(), key=lambda x: x[1], reverse=True)
    )
}

points_progression = {team: [points] for team, points in tracked_teams.items()}
updated_points = tracked_teams.copy()

for week in sorted(weekly_results.keys(), key=lambda w: int(w.split()[1])):
    for team, result in weekly_results[week]:
        if team in updated_points:
            if result == "Win":
                updated_points[team] += 3
            elif result == "Draw":
                updated_points[team] += 1
    for team in tracked_teams:
        points_progression[team].append(updated_points[team])

    df_week = pd.DataFrame({"Team": list(updated_points.keys()), "Points": list(updated_points.values())})
    df_week = df_week.sort_values(by="Points", ascending=False).reset_index(drop=True)
    st.markdown(f"**{week} Standings**")
    st.dataframe(df_week, height=300)

# -------------------- LINE CHART -------------------- #
st.subheader("📈 Points Progression by Week")
points_df = pd.DataFrame(points_progression)
points_df.index = ["Start"] + [f"Week {i}" for i in range(30, 30 + len(points_df.index) - 1)]
st.line_chart(points_df)

# -------------------- FINAL STANDINGS -------------------- #
standings_df = pd.DataFrame(updated_points.items(), columns=["Team", "Points"])
standings_df = standings_df.sort_values(by="Points", ascending=False).reset_index(drop=True)

# Add movement arrows
def movement_icon(team, new_idx):
    old_idx = original_ranks[team]
    if new_idx < old_idx:
        return "🔺"
    elif new_idx > old_idx:
        return "🔻"
    return "⏸️"

standings_df["Movement"] = [movement_icon(row["Team"], idx) for idx, row in standings_df.iterrows()]
standings_df = standings_df[["Movement", "Team", "Points"]]

# -------------------- DISPLAY -------------------- #
st.subheader("🏆 Projected Final Standings")
st.dataframe(standings_df, height=400)
