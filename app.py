import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Top 12 LIVE", layout="wide")
st.title("Stats")
st.caption("LIVE data from API-FOOTBALL - Free Plan Compatible")

TEAMS = {
    "Barcelona": 529, "Manchester City": 50, "Real Madrid": 541,
    "Bayern Munich": 157, "Liverpool": 40, "Arsenal": 42,
    "PSG": 85, "Inter Milan": 505, "Borussia Dortmund": 165,
    "Chelsea": 49, "Atletico Madrid": 530, "AC Milan": 489
}

API_KEY = st.secrets.get("API_KEY", "")
headers = {"x-apisports-key": API_KEY}

selected = st.selectbox("Select Team (Top 12 Powerhouses)", list(TEAMS.keys()))
team_id = TEAMS[selected]

# Free plan can't use 'last', so we use season + sort
current_season = 2024  # 2024/25 season - allowed on free

if st.button("🔴 LOAD LIVE LAST 5 GAMES", type="primary"):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={current_season}"
    r = requests.get(url, headers=headers, timeout=20)
    data = r.json()
    
    games = data.get("response", [])
    
    if not games:
        st.warning("No games in 2024, trying 2023 season...")
        url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season=2023"
        r = requests.get(url, headers=headers, timeout=20)
        data = r.json()
        games = data.get("response", [])
    
    if games:
        # Sort by date newest first and take last 5 finished
        finished = [g for g in games if g["fixture"]["status"]["short"] == "FT"]
        finished.sort(key=lambda x: x["fixture"]["date"], reverse=True)
        last5 = finished[:5]
        
        st.success(f"Found {len(last5)} LIVE games for {selected} (Season {current_season})")
        for f in last5:
            h = f["teams"]["home"]["name"]
            a = f["teams"]["away"]["name"]
            gh = f["goals"]["home"]
            ga = f["goals"]["away"]
            ht = f["score"]["halftime"]
            date = f["fixture"]["date"][:10]
            league = f["league"]["name"]
            st.markdown(f"**{h} {gh}-{ga} {a}** | HT {ht['home']}-{ht['away']} | {date} | {league}")
        
        with st.expander("Show raw API response"):
            st.json(data)
    else:
        st.error("No games found - API says:")
        st.json(data)
