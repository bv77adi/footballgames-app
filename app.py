import streamlit as st
import requests

st.set_page_config(page_title="Top 12 - 2026 LIVE", layout="wide")
st.title("⚽ Top 12 Powerhouses - LAST 5 FROM 2026")
st.caption("FREE: football-data.org | Green=Win Red=Loss")

TEAMS = {
    "Barcelona": 81, "Real Madrid": 86, "Atletico Madrid": 78,
    "Manchester City": 65, "Liverpool": 64, "Arsenal": 57,
    "Chelsea": 61, "Bayern Munich": 5, "Borussia Dortmund": 4,
    "Inter Milan": 108, "AC Milan": 98, "PSG": 524
}

API_TOKEN = st.secrets.get("FOOTBALL_DATA_TOKEN", "")
if not API_TOKEN:
    st.error("Add FOOTBALL_DATA_TOKEN in Secrets!")
    st.stop()

headers = {"X-Auth-Token": API_TOKEN}
selected = st.selectbox("Select Team (Top 12)", list(TEAMS.keys()))
team_id = TEAMS[selected]

if st.button("🔴 LOAD LAST 5 FROM 2026", type="primary"):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?limit=30&status=FINISHED"
    data = requests.get(url, headers=headers, timeout=15).json()
    matches = data.get("matches", [])
    matches_2026 = [m for m in matches if m["utcDate"].startswith("2026")]
    matches_2026.sort(key=lambda x: x["utcDate"], reverse=True)
    last5 = matches_2026[:5]

    wins = draws = losses = 0
    for m in last5:
        home = m["homeTeam"]["shortName"]
        away = m["awayTeam"]["shortName"]
        ft = m["score"]["fullTime"]
        ht = m["score"]["halfTime"]
        date = m["utcDate"][:10]
        comp = m["competition"]["name"]
        winner = m["score"]["winner"]
        
        # Determine if selected team won
        is_home = m["homeTeam"]["id"] == team_id
        if (is_home and winner == "HOME_TEAM") or (not is_home and winner == "AWAY_TEAM"):
            color = "#00C853"  # GREEN WIN
            result_icon = "✅ WIN"
            wins+=1
        elif winner == "DRAW":
            color = "#9E9E9E"  # GREY DRAW
            result_icon = "➖ DRAW"
            draws+=1
        else:
            color = "#D50000"  # RED LOSS
            result_icon = "❌ LOSS"
            losses+=1

        st.markdown(f"""
        <div style="border-left:6px solid {color}; padding:10px; margin:8px 0; background:#f9f9f9; border-radius:8px">
        <b style="color:{color}">{result_icon}</b> — <b>{home} {ft['home']}-{ft['away']} {away}</b><br>
        HT: {ht['home']}-{ht['away']} | {date} | {comp}
        </div>
        """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    c1.metric("✅ Wins", wins)
    c2.metric("➖ Draws", draws)
    c3.metric("❌ Losses", losses)
