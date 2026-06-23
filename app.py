import streamlit as st
from google import genai
import random

st.set_page_config(
    page_title="Business AI Assistant",
    page_icon="📈",
    layout="wide"
)

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Missing GEMINI_API_KEY in Streamlit secrets")
    st.stop()

locations = [
    "District 1", "District 3", "District 5", "District 7", "District 10",
    "Binh Thanh", "Thu Duc", "Tan Binh", "Go Vap", "Phu Nhuan"
]

foot_traffic = {
    "District 1": 125000,
    "District 3": 95000,
    "District 5": 88000,
    "District 7": 73000,
    "District 10": 81000,
    "Binh Thanh": 92000,
    "Thu Duc": 68000,
    "Tan Binh": 85000,
    "Go Vap": 79000,
    "Phu Nhuan": 71000
}

st.title("Business AI Assistant")
st.caption("AI-Powered Startup Consulting for Vietnam")

# -------------------------
# SESSION STATE (MENU LOOP)
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "menu"

# -------------------------
# RESET FUNCTION
# -------------------------
def go_menu():
    st.session_state.page = "menu"

# -------------------------
# MENU PAGE
# -------------------------
if st.session_state.page == "menu":

    st.subheader("Select Service")

    choice = st.radio(
        "Choose option",
        [
            "Business Location Recommendation",
            "Foot Traffic Analysis",
            "Trending Business Ideas"
        ]
    )

    if st.button("Continue"):
        st.session_state.page = choice
        st.rerun()

# -------------------------
# 1. LOCATION
# -------------------------
elif st.session_state.page == "Business Location Recommendation":

    st.subheader("Business Location Recommendation")

    capital = st.number_input("Available Capital (USD)", min_value=0, value=50000)
    experience = st.text_input("Business Experience", value="Restaurant Management")
    interest = st.text_input("Interested Industry", value="Cafe")

    if st.button("Get Recommendation"):

        location = random.choice(locations)

        prompt = f"""
You are a startup consultant.

Capital: {capital}
Experience: {experience}
Interest: {interest}

Recommended Location:
{location}

Return only:
Recommended Location:
Reason:
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt]
            )

            text = getattr(response, "text", "")

            if "Reason:" in text:
                parts = text.split("Reason:")
                location_text = parts[0].replace("Recommended Location:", "").strip()
                reason_text = parts[1].strip() if len(parts) > 1 else ""
            else:
                location_text = text
                reason_text = ""

            st.success("Recommendation Complete")

            st.markdown("### 📍 Recommended Location")
            st.info(location_text)

            st.markdown("### 💡 Reason")
            st.success(reason_text)

        except Exception as e:
            st.error("API request failed")
            st.warning(str(e))

    st.button("⬅ Back to Menu", on_click=go_menu)

# -------------------------
# 2. FOOT TRAFFIC
# -------------------------
elif st.session_state.page == "Foot Traffic Analysis":

    st.subheader("Foot Traffic Analysis")

    district = st.selectbox("Select District", list(foot_traffic.keys()))

    if st.button("Analyze Traffic"):

        traffic = foot_traffic.get(district, 0)

        st.markdown("### 📊 Result")
        st.metric("District", district)
        st.metric("Average Daily Foot Traffic", f"{traffic:,} people")

    st.button("⬅ Back to Menu", on_click=go_menu)

# -------------------------
# 3. TRENDING
# -------------------------
elif st.session_state.page == "Trending Business Ideas":

    st.subheader("Trending Business Ideas")

    if st.button("Generate Ideas"):

        prompt = """
Recommend 5 trending business ideas in Vietnam.

For each idea provide:
- Business Name
- Why it is trending

Keep answers concise.
"""

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash-002",
                contents=[prompt]
            )

            text = getattr(response, "text", "")

            st.markdown("### 🔥 Trending Ideas")
            st.info(text)

        except Exception as e:
            st.error("API request failed")
            st.warning(str(e))

    st.button("⬅ Back to Menu", on_click=go_menu)
