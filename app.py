import streamlit as st

st.set_page_config(page_title="Football Games - Top 12", page_icon="⚽", layout="wide")
st.title("⚽ Top 12 Most Powerful Teams - Last 5 Stats")

TEAMS = {
    "Manchester City": {"last5": [{"m":"Man City 3-1 Newcastle","ht":"1-0","c":"7-2","r":"W"},{"m":"PSG 2-3 Man City","ht":"1-1","c":"4-6","r":"W"},{"m":"Man City 2-0 Chelsea","ht":"1-0","c":"8-1","r":"W"},{"m":"Brentford 0-2 Man City","ht":"0-1","c":"3-9","r":"W"},{"m":"Man City 1-1 Arsenal","ht":"1-0","c":"5-4","r":"D"}], "odds":1.45, "best":1.52, "gf":11, "ga":4},
    "Real Madrid": {"last5": [{"m":"Real Madrid 4-1 Sevilla","ht":"2-1","c":"5-3","r":"W"},{"m":"Roma 3-4 Real Madrid","ht":"1-2","c":"3-5","r":"W"},{"m":"Real Madrid 1-0 Villarreal","ht":"0-0","c":"8-2","r":"W"},{"m":"Atletico 2-1 Real Madrid","ht":"1-0","c":"4-4","r":"L"},{"m":"Real Madrid 2-0 Alaves","ht":"1-0","c":"6-2","r":"W"}], "odds":1.55, "best":1.62, "gf":12, "ga":6},
    "Barcelona": {"last5": [{"m":"PSG 2-4 Barcelona","ht":"1-2","c":"3-7","r":"L"},{"m":"Betis 2-5 Barcelona","ht":"0-2","c":"2-8","r":"W"},{"m":"Galatasaray 1-4 Barcelona","ht":"0-1","c":"4-6","r":"W"},{"m":"Barcelona 3-0 Getafe","ht":"2-0","c":"7-1","r":"W"},{"m":"Sevilla 1-3 Barcelona","ht":"1-1","c":"5-5","r":"W"}], "odds":1.62, "best":1.71, "gf":17, "ga":8},
    "Bayern Munich": {"last5": [{"m":"Bayern 5-0 Hoffenheim","ht":"3-0","c":"9-1","r":"W"},{"m":"Bayern 3-2 Wolfsburg","ht":"1-1","c":"6-3","r":"W"},{"m":"Leverkusen 0-1 Bayern","ht":"0-0","c":"4-5","r":"W"},{"m":"Bayern 2-1 Dortmund","ht":"1-1","c":"7-4","r":"W"},{"m":"Bayern 4-0 Frankfurt","ht":"2-0","c":"8-2","r":"W"}], "odds":1.35, "best":1.40, "gf":15, "ga":3},
    "Liverpool": {"last5": [{"m":"Liverpool 2-0 Man Utd","ht":"1-0","c":"6-3","r":"W"},{"m":"Arsenal 2-2 Liverpool","ht":"1-2","c":"5-5","r":"D"},{"m":"Liverpool 3-1 Chelsea","ht":"2-0","c":"7-2","r":"W"},{"m":"Brighton 1-2 Liverpool","ht":"0-1","c":"4-6","r":"W"},{"m":"Liverpool 4-0 Leverkusen","ht":"0-0","c":"8-3","r":"W"}], "odds":1.48, "best":1.55, "gf":13, "ga":4},
    "Arsenal": {"last5": [{"m":"Arsenal 3-0 Monaco","ht":"1-0","c":"7-2","r":"W"},{"m":"Arsenal 1-1 Man City","ht":"0-1","c":"4-5","r":"D"},{"m":"Everton 0-1 Arsenal","ht":"0-0","c":"2-8","r":"W"},{"m":"Arsenal 2-0 PSG","ht":"1-0","c":"6-3","r":"W"},{"m":"Arsenal 4-2 Leicester","ht":"2-1","c":"9-1","r":"W"}], "odds":1.50, "best":1.58, "gf":11, "ga":3},
    "PSG": {"last5": [{"m":"PSG 4-2 Man City","ht":"0-1","c":"6-4","r":"W"},{"m":"Lens 1-2 PSG","ht":"0-1","c":"3-5","r":"W"},{"m":"PSG 2-4 Barcelona","ht":"2-1","c":"7-3","r":"W"},{"m":"PSG 3-0 Lille","ht":"1-0","c":"8-2","r":"W"},{"m":"Arsenal 2-0 PSG","ht":"1-0","c":"6-3","r":"L"}], "odds":1.44, "best":1.50, "gf":12, "ga":8},
    "Inter Milan": {"last5": [{"m":"Inter 2-0 Atalanta","ht":"1-0","c":"5-3","r":"W"},{"m":"Inter 1-0 Arsenal","ht":"0-0","c":"4-4","r":"W"},{"m":"Napoli 0-3 Inter","ht":"0-2","c":"3-7","r":"W"},{"m":"Inter 3-2 Milan","ht":"1-1","c":"6-4","r":"W"},{"m":"Inter 4-0 Lecce","ht":"2-0","c":"8-1","r":"W"}], "odds":1.52, "best":1.60, "gf":13, "ga":2},
    "Bayer Leverkusen": {"last5": [{"m":"Leverkusen 2-1 Frankfurt","ht":"1-0","c":"6-3","r":"W"},{"m":"Leverkusen 1-0 Bayern","ht":"0-0","c":"5-4","r":"L"},{"m":"Leverkusen 5-0 Salzburg","ht":"2-0","c":"10-1","r":"W"},{"m":"Leverkusen 2-2 Stuttgart","ht":"1-1","c":"7-5","r":"D"},{"m":"Liverpool 4-0 Leverkusen","ht":"0-0","c":"8-3","r":"L"}], "odds":1.65, "best":1.73, "gf":9, "ga":7},
    "Atletico Madrid": {"last5": [{"m":"Atletico 2-1 Real Madrid","ht":"0-1","c":"4-4","r":"W"},{"m":"Atletico 2-1 Leipzig","ht":"1-1","c":"5-3","r":"W"},{"m":"Benfica 4-0 Atletico","ht":"2-0","c":"7-2","r":"L"},{"m":"Atletico 1-0 Athletic","ht":"0-0","c":"4-2","r":"W"},{"m":"Atletico 3-1 Leganes","ht":"1-1","c":"6-3","r":"W"}], "odds":1.70, "best":1.80, "gf":9, "ga":6},
    "Borussia Dortmund": {"last5": [{"m":"Dortmund 2-1 Lille","ht":"0-1","c":"5-4","r":"W"},{"m":"Bayern 2-1 Dortmund","ht":"1-1","c":"7-4","r":"L"},{"m":"Dortmund 6-0 Union Berlin","ht":"3-0","c":"9-2","r":"W"},{"m":"Dortmund 2-0 St Pauli","ht":"1-0","c":"6-2","r":"W"},{"m":"Dortmund 3-1 Shakhtar","ht":"2-0","c":"7-3","r":"W"}], "odds":1.75, "best":1.85, "gf":14, "ga":4},
    "AC Milan": {"last5": [{"m":"AC Milan 3-0 Lecce","ht":"2-0","c":"6-2","r":"W"},{"m":"Inter 3-2 AC Milan","ht":"1-1","c":"6-4","r":"L"},{"m":"AC Milan 2-1 Como","ht":"0-1","c":"5-3","r":"W"},{"m":"Napoli 2-0 AC Milan","ht":"2-0","c":"5-2","r":"L"},{"m":"AC Milan 1-0 Udinese","ht":"1-0","c":"4-1","r":"W"}], "odds":1.68, "best":1.76, "gf":8, "ga":5},
}

team = st.selectbox("Select Team (Top 12 Powerhouses)", list(TEAMS.keys()))
d = TEAMS[team]

st.subheader(f"{team} - Last 5 Games Breakdown")

for g in d["last5"]:
    st.markdown(f"**{g['m']}** | HT: `{g['ht']}` | Corners: `{g['c']}` | Result: **{g['r']}**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("GF Last 5", d["gf"])
col2.metric("GA Last 5", d["ga"])
col3.metric("Odds", d["odds"])
col4.metric("Best Odds", d["best"])

st.info("Format: FT Score | HT Score | Corners (Home-Away) | W/D/L")
