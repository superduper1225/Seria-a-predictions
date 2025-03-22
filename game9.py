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
    keys_to_clear = [key for key in list(st.session_state.keys()) if "::" in key or key.startswith("match_results")]
    for key in keys_to_clear:
        del st.session_state[key]
    st.rerun()

# -------------------- MATCH SELECTION -------------------- #
st.subheader("📅 Match Results by Week")

weekly_fixtures = defaultdict(list)
for fixture in fixtures:
    weekly_fixtures[fixture[0]].append(fixture[1:])

if "match_results" not in st.session_state:
    st.session_state.match_results = {}
match_results = st.session_state.match_results

weeks_missing_results = set()

points_progression = {team: [tracked_teams[team]] for team in tracked_teams}

for week, matches in weekly_fixtures.items():
    with st.expander(f"🗓️ {week} Matches", expanded=False):
        for i, (team1, team2) in enumerate(matches):
            match_key = f"{team1} vs {team2}"
            reverse_key = f"{team2} vs {team1}"
            widget_key = f"{week}::{team1}::{team2}"

            result = st.radio(
                f"{team1} vs {team2}",
                ["Win", "Draw", "Loss"],
                key=widget_key,
                horizontal=True,
                index=None if widget_key not in st.session_state or st.session_state[widget_key] not in ["Win", "Draw", "Loss"] else ["Win", "Draw", "Loss"].index(st.session_state[widget_key])
            )

            match_results[match_key] = result
            if result in ["Win", "Draw", "Loss"]:
                match_results[reverse_key] = {"Win": "Loss", "Loss": "Win", "Draw": "Draw"}[result]
            else:
                weeks_missing_results.add(week)

    # Recalculate updated points fresh each week
    updated_points = tracked_teams.copy()
    for match_key, result in match_results.items():
        if result not in ["Win", "Draw", "Loss"]:
            continue
        team1, team2 = match_key.split(" vs ")
        if team1 in updated_points and team2 in updated_points:
            if result == "Win":
                updated_points[team1] += 3
            elif result == "Draw":
                updated_points[team1] += 1
                updated_points[team2] += 1
            elif result == "Loss":
                updated_points[team2] += 3

    df_week = pd.DataFrame({"Team": list(updated_points.keys()), "Points": list(updated_points.values())})
    df_week = df_week.sort_values(by="Points", ascending=False).reset_index(drop=True)
    st.markdown(f"**{week} Standings**")
    st.dataframe(df_week, height=300)

# Final week standings
if current_week is not None:
    df_week = pd.DataFrame({"Team": list(updated_points.keys()), "Points": list(updated_points.values())})
    df_week = df_week.sort_values(by="Points", ascending=False).reset_index(drop=True)
    st.markdown(f"**{current_week} Standings**")
    st.dataframe(df_week, height=300)

# -------------------- FINAL STANDINGS -------------------- #
original_ranks = {
    team: idx for idx, (team, _) in enumerate(
        sorted(tracked_teams.items(), key=lambda x: x[1], reverse=True)
    )
}

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
if weeks_missing_results:
    st.warning(f"⚠️ You have unselected matches in: {', '.join(sorted(weeks_missing_results))}. Final standings may be incomplete.")

st.subheader("🏆 Projected Final Standings")
st.dataframe(standings_df, height=400)
