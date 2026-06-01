import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="Esports AI Betting Model", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Esports AI Betting Model")
st.caption("MelBet Screenshot Analyzer + Betting Scorecard")

uploaded_file = st.file_uploader(
    "Upload MelBet screenshot",
    type=["png", "jpg", "jpeg"]
)

def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded screenshot", use_container_width=True)

    if st.button("Analyze Screenshot"):
        with st.spinner("Reading screenshot..."):
            img_b64 = image_to_base64(image)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are an esports betting odds extraction assistant.
Extract betting info from the screenshot only.
Do not invent data.
Return clear structured text.
"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """
Extract:
- Game/esport
- Team A
- Team B
- Market
- Team A odds
- Team B odds
- Handicap lines
- Total lines
- Live score if visible
- Any important betting context visible

If unclear, say UNCLEAR.
"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_b64}"
                                }
                            }
                        ]
                    }
                ]
            )

            st.subheader("Extracted Betting Info")
            st.write(response.choices[0].message.content)

st.divider()

st.header("Manual Confirmation")

team_a = st.text_input("Team A")
team_b = st.text_input("Team B")
market = st.selectbox(
    "Market",
    ["Moneyline", "Map Handicap", "Round Handicap", "Total Rounds", "Team Total", "Other"]
)
odds = st.number_input("Odds", min_value=1.01, value=1.80, step=0.01)
unit_value = st.number_input("1 Unit Value (AED)", min_value=1, value=80)

st.header("Model Scores")

team_form = st.slider("Team Form", 0, 20, 10)
map_advantage = st.slider("Map Advantage", 0, 20, 10)
player_form = st.slider("Player Form", 0, 15, 8)
opponent_strength = st.slider("Opponent Strength", 0, 15, 8)
odds_value = st.slider("Odds Value", 0, 20, 10)
live_momentum = st.slider("Live Momentum", 0, 10, 5)
risk_penalty = st.slider("Risk Penalty", 0, 20, 5)

score = (
    team_form
    + map_advantage
    + player_form
    + opponent_strength
    + odds_value
    + live_momentum
    - risk_penalty
)

st.subheader(f"Final Edge Score: {score}/100")

if score >= 85:
    decision = "BET"
    units = 1.0
elif score >= 75:
    decision = "SMALL BET"
    units = 0.5
elif score >= 65:
    decision = "WAIT LIVE"
    units = 0
else:
    decision = "NO BET"
    units = 0

stake = units * unit_value

st.success(f"Decision: {decision}")
st.write(f"Recommended Units: {units}")
st.write(f"Recommended Stake: AED {stake}")

st.header("Technical Note")

if team_a and team_b:
    st.write(
        f"{team_a} vs {team_b} | Market: {market} | Odds: {odds} | "
        f"Edge Score: {score}/100 | Decision: {decision}"
    )
