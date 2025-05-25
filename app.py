import streamlit as st
import re
from textblob import TextBlob
import openai

# Get OpenAI API key from Streamlit secrets or environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Make sure you set this in Streamlit secrets

# Crisis keywords regex
CRISIS_PATTERN = re.compile(
    r"\b(kill\s+myself|suicid(?:e|al)|end\s+my\s+life|don't\s+want\s+to\s+live|"
    r"take\s+my\s+own\s+life|hurt\s+myself|die)\b", re.I
)

def is_crisis(text: str) -> bool:
    return bool(CRISIS_PATTERN.search(text))

def query_openai(user_input: str) -> str:
    messages = [
        {"role": "system", "content": "You are a compassionate mental health assistant."},
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        temperature=0.7,
        top_p=0.9,
        n=1,
        stop=None,
    )
    return response.choices[0].message.content.strip()

# Streamlit UI setup
st.set_page_config(page_title="🧠 AI Mental Health Chatbot", layout="centered")
st.title("🧠 AI Mental Health Chatbot")
st.caption("Free, empathetic mental health support (not a replacement for professional help)")

user_message = st.text_input("Type your message here:")

if user_message:
    polarity = TextBlob(user_message).sentiment.polarity
    if polarity > 0.1:
        st.info("😊 Sentiment: Positive")
    elif polarity < -0.1:
        st.info("☹️ Sentiment: Negative")
    else:
        st.info("😐 Sentiment: Neutral")

    if is_crisis(user_message):
        st.warning(
            "⚠️ It sounds like you're in a very difficult place. "
            "You're **not alone** and help is available.\n\n"
            "• India (AASRA 24×7): 9152987821\n"
            "• Worldwide helplines: https://findahelpline.com"
        )
        st.stop()

    with st.spinner("Thinking..."):
        try:
            response = query_openai(user_message)
            st.markdown("### 🤖 AI Response")
            st.write(response)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if st.button("🩺 Show Self-care Tips"):
    st.markdown("""
    ### 🩺 Self-Care Tips
    - 🧘 Practice deep breathing or meditation
    - 🏃 Go for a short walk
    - 📖 Write down your thoughts
    - 🗣️ Talk to someone you trust
    - 💧 Drink water and eat well
    """)
