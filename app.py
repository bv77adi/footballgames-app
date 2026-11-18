import streamlit as st
import requests
import time

st.set_page_config(page_title="Top 12 - 2026 LIVE", page_icon="⚽", layout="wide")
st.title("⚽ Top 12 Powerhouses - LAST 5 FROM 2026")
st.caption("FREE: football-data.org | Green=Win Red=Loss | BTTS + Over 3.5 calculated from score")

TEAMS = {
    "Barcelona": 81, "Real Madrid": 86, "Atletico Madrid": 78,
    "Manchester City": 65, "Liverpool": 64, "Arsenal": 57,
    "Chelsea": 61, "Bayern Munich": 5, "Manchester United": 66
     "Inter Milan": 108, "AC Milan": 98, "Paris Saint-Germain": 524, 
}

API_TOKEN = st.secrets.get("FOOTBALL_DATA_TOKEN", "")
if not API_TOKEN:
    st.error("Add FOOTBALL_DATA_TOKEN in Secrets!")
    st.stop()

headers = {"X-Auth-Token": API_TOKEN}
@st.cache_data(ttl=3600)
def get_matches(team_id):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=5"
    for _ in range(3):
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json().get("matches", [])[::-1]
        time.sleep(7)  # wait for free API limit
    return []

def analyse(matches, team_name):
    wins = draws = losses = btts = over35 = 0
    goals_for = goals_against = 0
    for m in matches:
        s = m["score"]["fullTime"]
        ht = m["score"]["halfTime"]
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        # find our score
        if team_name in home:
            gf, ga = s["home"], s["away"]
        else:
            gf, ga = s["away"], s["home"]
        if gf is None: continue
        goals_for += gf; goals_against += ga
        if gf > ga: wins += 1
        elif gf == ga: draws += 1
        else: losses += 1
        if gf > 0 and ga > 0: btts += 1
        if gf + ga > 3: over35 += 1
    n = max(1, len(matches))
    return wins, draws, losses, btts, over35, goals_for, goals_against, n

# --- ALL 12 OVERVIEW ---
st.subheader("📊 All 12 Teams - Last 5 Form")
col1, col2 = st.columns(2)
with col1:
    load_first = st.button("🔄 LOAD TEAMS 1-6", type="primary")
with col2:
    load_second = st.button("🔄 LOAD TEAMS 7-12")
if load_first or load_second:
    teams_to_load = list(TEAMS.items())
    if load_first:
        teams_to_load = teams_to_load[:6]
    else:
        teams_to_load = teams_to_load[6:]
    for name, tid in teams_to_load:
        matches = get_matches(tid)
        if not matches:
            st.write(f"{name}: No data")
            continue
        w, d, l, btts, o35, gf, ga, n = analyse(matches, name)
        with st.expander(f"{name}  |  {w}W - {d}D - {l}L  |  BTTS: {btts}/{n}  |  Over 3.5: {o35}/{n}  |  Goals: {gf}-{ga}"):
            for m in matches:
                s = m["score"]["fullTime"]
                ht = m["score"]["halfTime"]
                home = m["homeTeam"]["shortName"] or m["homeTeam"]["name"]
                away = m["awayTeam"]["shortName"] or m["awayTeam"]["name"]
                total = (s["home"] or 0) + (s["away"] or 0)
                is_btts = "✅ YES" if s["home"] > 0 and s["away"] > 0 else "❌ NO"
                is_o35 = "✅ OVER" if total > 3 else "❌ UNDER"
                date = m["utcDate"][:10]
                comp = m["competition"]["name"]
                st.markdown(f"**{home} {s['home']}-{s['away']} {away}** | HT: {ht['home']}-{ht['away']} | {date} | {comp}")
                st.caption(f"BTTS: {is_btts} | Over 3.5: {is_o35} | Total Goals: {total}")
                st.divider()
