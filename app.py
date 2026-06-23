import streamlit as st
from google import genai
import random

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)
st.write(st.secrets)
st.write(GEMINI_API_KEY)
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

st.set_page_config(
    page_title="Business AI Assistant",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Business AI Assistant")
st.caption("AI-Powered Startup Consulting for Vietnam")

menu = st.sidebar.selectbox(
    "Select Service",
    [
        "Business Location Recommendation",
        "Foot Traffic Analysis",
        "Trending Business Ideas"
    ]
)

if menu == "Business Location Recommendation":

    st.subheader("Business Location Recommendation")

    capital = st.number_input(
        "Available Capital (USD)",
        min_value=0,
        value=50000
    )

    experience = st.text_input(
        "Business Experience",
        value="Restaurant Management"
    )

    interest = st.text_input(
        "Interested Industry",
        value="Cafe"
    )

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

        Keep the answer under 2 sentences.
        """

        with st.spinner("Generating recommendation..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.success("Recommendation Complete")
        st.markdown(response.text)

elif menu == "Foot Traffic Analysis":

    st.subheader("Foot Traffic Analysis")

    district = st.selectbox(
        "Select District",
        list(foot_traffic.keys())
    )

    if st.button("Analyze Traffic"):

        traffic = foot_traffic[district]

        st.metric(
            "Average Daily Foot Traffic",
            f"{traffic:,} people"
        )

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

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.markdown(response.text)
