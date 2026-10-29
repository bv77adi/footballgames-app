import streamlit as st
import requests

st.title("Top 12 - 2026 LIVE with football-data.org FREE")

TEAMS_FD = {"Barcelona": 81, "Man City": 65, "Real Madrid": 86, "Bayern": 5, "Liverpool": 64, "Arsenal": 57, "PSG": 524, "Inter": 108, "Dortmund": 4, "Chelsea": 61, "Atletico Madrid": 78, "AC Milan": 98}

token = st.secrets["FOOTBALL_DATA_TOKEN"] # get free at football-data.org
headers = {"X-Auth-Token": token}

team = st.selectbox("Select Team", list(TEAMS_FD.keys()))

if st.button("🔴 LOAD LAST 5 FROM 2026"):
    url = f"https://api.football-data.org/v4/teams/{TEAMS_FD[team]}/matches?limit=5&status=FINISHED"
    r = requests.get(url, headers=headers).json()
    for m in r["matches"][-5:][::-1]:
        ht = m["score"]["halfTime"]
        ft = m["score"]["fullTime"]
        st.write(f"{m['homeTeam']['name']} {ft['home']}-{ft['away']} {m['awayTeam']['name']} | HT {ht['home']}-{ht['away']} | {m['utcDate'][:10]} | {m['competition']['name']}")
