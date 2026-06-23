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
    st.error("Missing or invalid GEMINI_API_KEY in Streamlit secrets")
    st.stop()

locations = [
    "District 1",
    "District 3",
    "District 5",
    "District 7",
    "District 10",
    "Binh Thanh",
    "Thu Duc",
    "Tan Binh",
    "Go Vap",
    "Phu Nhuan"
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

menu = st.sidebar.selectbox(
    "Select Service",
    [
        "Business Location Recommendation",
        "Foot Traffic Analysis",
        "Trending Business Ideas"
    ]
)

# -----------------------------
# LOCATION RECOMMENDATION
# -----------------------------
if menu == "Business Location Recommendation":

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

        with st.spinner("Generating recommendation..."):

            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt]
                )

                text = getattr(response, "text", None)

                if not text:
                    st.warning("Empty response from AI")
                    st.stop()

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
                st.error("AI request failed safely (no crash)")
                st.warning(str(e))

# -----------------------------
# FOOT TRAFFIC
# -----------------------------
elif menu == "Foot Traffic Analysis":

    st.subheader("Foot Traffic Analysis")

    district = st.selectbox(
        "Select District",
        list(foot_traffic.keys())
    )

    if st.button("Analyze Traffic"):

        traffic = foot_traffic.get(district, 0)

        st.markdown("### 📊 Result")
        st.metric("District", district)
        st.metric("Average Daily Foot Traffic", f"{traffic:,} people")

# -----------------------------
# TRENDING IDEAS
# -----------------------------
elif menu == "Trending Business Ideas":

    st.subheader("Trending Business Ideas")

    if st.button("Generate Ideas"):

        prompt = """
Recommend 5 trending business ideas in Vietnam.

For each idea provide:
- Business Name
- Why it is trending

Keep answers concise.
"""

        with st.spinner("Searching trends..."):

            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt]
                )

                text = getattr(response, "text", None)

                if not text:
                    st.warning("Empty response from AI")
                    st.stop()

                st.markdown("### 🔥 Trending Ideas")
                st.info(text)

            except Exception as e:
                st.error("AI request failed safely (no crash)")
                st.warning(str(e))
