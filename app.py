import streamlit as st
import pickle
import numpy as np
from PIL import Image

# Load the trained model
with open("best_model_lr.pkl", "rb") as f:
    data = pickle.load(f)
    model = data["model"]
    scaler = data["scaler"]

st.set_page_config(page_title="Admission Predictor", page_icon="🎓", layout="wide")

st.title("🎓 Graduate Admission Predictor")
st.markdown("Fill in your details below to predict your **Chance of Admit**")

# Add university logos at the top - optimized size
st.markdown("### 🏛️ Top Universities Worldwide")
col_us, col_uk = st.columns([1, 1])

with col_us:
    us_unis_image = Image.open("ivyyy.png")
    st.image(us_unis_image, width=555, caption="Top US Universities")


with col_uk:
    uk_unis_image = Image.open("russell.jpg")
    st.image(uk_unis_image, width=555, caption="Prestigious UK Universities")

st.markdown("---")

# Main layout: Students photo on left, inputs on right
col1, col2 = st.columns([2, 2])

with col1:
    # Students photo on the left - better sized
    st.markdown("#### 👥 Success Stories")

    students_image = Image.open("study-abroad.jpg")
    st.image(
        students_image,
        # width=400,
        caption="Your Journey to Graduate School!",
    )


with col2:
    # All input fields on the right
    st.markdown("### 📝 Enter Your Academic Details")

    gre = st.number_input(
        "GRE Score (out of 340)", min_value=0, max_value=340, value=300
    )
    toefl = st.number_input(
        "TOEFL Score (out of 120)", min_value=0, max_value=120, value=100
    )
    rating = st.slider(
        "University Rating (out of 5)", min_value=1, max_value=5, value=3
    )
    sop = st.number_input("SOP Strength (0.0 - 5.0)", 0.0, 5.0, 3.5, format="%.1f")
    lor = st.number_input("LOR Strength (0.0 - 5.0)", 0.0, 5.0, 3.0, format="%.1f")
    cgpa = st.number_input(
        "Undergraduate GPA (out of 10)",
        min_value=0.0,
        max_value=10.0,
        value=8.0,
        format="%.2f",
    )

    # Research input (Yes/No → 1/0)
    research = st.radio("Research Experience", ["No", "Yes"])
    research_val = 1 if research == "Yes" else 0

    # Prediction
    if st.button("🔮 Predict", use_container_width=True):
        # Arrange features in the same order as training
        features = np.array([[gre, toefl, rating, sop, lor, cgpa, research_val]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        prediction_percent = np.clip(prediction * 100, 0, 100)

        # Bigger font for prediction result
        st.markdown(
            f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    color: white; padding: 2rem; border-radius: 15px; text-align: center; 
                    margin: 1rem 0; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
            <h1 style="margin: 0; font-size: 3rem; font-weight: bold;">
                🎯 Estimated Chance of Admit: {prediction_percent:.1f}%
            </h1>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Show celebration or encouragement based on prediction
        if prediction_percent >= 70:
            st.balloons()
            st.markdown("### 🌟 Excellent chances! You're on the right track!")
        elif prediction_percent >= 50:
            st.markdown("### ✨ Good prospects! Keep up the great work!")
        else:
            st.markdown(
                "### 💪 Room for improvement! Consider strengthening your profile."
            )

st.markdown("---")
st.markdown("*Good luck with your graduate school applications! 🍀*")
