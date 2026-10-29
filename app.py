import streamlit as st
import requests

st.set_page_config(page_title="Top 12 LIVE Form", layout="wide")
st.title("Stats")
st.caption("LIVE data from API-FOOTBALL")

TEAMS = {
    "Barcelona": 529, "Manchester City": 50, "Real Madrid": 541,
    "Bayern Munich": 157, "Liverpool": 40, "Arsenal": 42,
    "PSG": 85, "Inter Milan": 505, "Borussia Dortmund": 165,
    "Chelsea": 49, "Atletico Madrid": 530, "AC Milan": 489
}

API_KEY = st.secrets.get("API_KEY", "")
if not API_KEY:
    st.error("API_KEY not found in Secrets!")
    st.stop()

headers = {"x-apisports-key": API_KEY}

selected = st.selectbox("Select Team (Top 12 Powerhouses)", list(TEAMS.keys()))
team_id = TEAMS[selected]

@st.cache_data(ttl=600)
def get_form(team_id):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    r = requests.get(url, headers=headers, timeout=15)
    return r.json().get("response", [])

games = get_form(team_id)

if not games:
    st.warning("No games / API limit reached (100/day free). Wait 1 min and refresh.")
else:
    gf = 0
    ga = 0
    btts = 0
    for f in games:
        home = f["teams"]["home"]["name"]
        away = f["teams"]["away"]["name"]
        gh = f["goals"]["home"] or 0
        go = f["goals"]["away"] or 0
        ht = f["score"]["halftime"]
        date = f["fixture"]["date"][:10]
        
        if f["teams"]["home"]["id"] == team_id:
            gf += gh
            ga += go
        else:
            gf += go
            ga += gh
        
        if gh > 0 and go > 0:
            btts += 1

        st.markdown(f"**{home} {gh}-{go} {away}** | HT: {ht['home']}-{ht['away']} - {date}")

    col1, col2, col3 = st.columns(3)
    col1.metric("GF Last 5", gf)
    col2.metric("GA Last 5", ga)
    col3.metric("BTTS", f"{btts}/5")
