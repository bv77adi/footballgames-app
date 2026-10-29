import streamlit as st
import requests

st.set_page_config(page_title="Top 12 LIVE", layout="wide")
st.title("Stats")
st.caption("LIVE data from API-FOOTBALL")

TEAMS = {
    "Barcelona": 529, "Manchester City": 50, "Real Madrid": 541,
    "Bayern Munich": 157, "Liverpool": 40, "Arsenal": 42,
    "PSG": 85, "Inter Milan": 505, "Borussia Dortmund": 165,
    "Chelsea": 49, "Atletico Madrid": 530, "AC Milan": 489
}

API_KEY = st.secrets.get("API_KEY", "")
st.write(f"Key found: {API_KEY[:5]}...") if API_KEY else st.error("No key in Secrets!")

headers = {"x-apisports-key": API_KEY}
selected = st.selectbox("Select Team (Top 12 Powerhouses)", list(TEAMS.keys()))
team_id = TEAMS[selected]

if st.button("🔴 LOAD LIVE LAST 5 GAMES", type="primary"):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    r = requests.get(url, headers=headers, timeout=20)
    data = r.json()
    
    st.subheader("API Response:")
    st.json(data)
    
    games = data.get("response", [])
    if games:
        for f in games:
            h = f["teams"]["home"]["name"]
            a = f["teams"]["away"]["name"]
            gh = f["goals"]["home"]
            ga = f["goals"]["away"]
            date = f["fixture"]["date"][:10]
            st.write(f"**{h} {gh}-{ga} {a}** - {date}")
    else:
        st.error("No games - see JSON above")
