import streamlit as st

st.title("Esports AI Betting Model")

st.header("Match Information")

team_a = st.text_input("Team A")
team_b = st.text_input("Team B")

team_form = st.slider("Team Form", 0, 20, 10)
map_advantage = st.slider("Map Advantage", 0, 20, 10)
player_form = st.slider("Player Form", 0, 15, 8)
opponent_strength = st.slider("Opponent Strength", 0, 15, 8)
odds_value = st.slider("Odds Value", 0, 20, 10)
momentum = st.slider("Live Momentum", 0, 10, 5)
risk_penalty = st.slider("Risk Penalty", 0, 20, 5)

score = (
    team_form +
    map_advantage +
    player_form +
    opponent_strength +
    odds_value +
    momentum -
    risk_penalty
)

st.subheader(f"Final Edge Score: {score}")

if score >= 85:
    decision = "BET"
    units = 1
elif score >= 75:
    decision = "SMALL BET"
    units = 0.5
elif score >= 65:
    decision = "WAIT LIVE"
    units = 0
else:
    decision = "NO BET"
    units = 0

stake = units * 80

st.success(f"Decision: {decision}")
st.write(f"Units: {units}")
st.write(f"Stake: AED {stake}")
