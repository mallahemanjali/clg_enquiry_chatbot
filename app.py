import streamlit as st
import random
import re
import os
import joblib

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main {
    background-color: #f5f7fb;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #7F5AF0, #6246EA);
    color: white;
}

[data-testid="stSidebar"] * {
    color: white;
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    color: #2b2d42;
    margin-top: 10px;
}

.sub-title {
    text-align: center;
    color: #6c757d;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.feature-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.06);
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.chat-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #2b2d42;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    margin-top: 30px;
    color: gray;
    font-size: 16px;
}

.stChatMessage {
    border-radius: 18px;
    padding: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL + VECTORIZER
# =========================================================

MODELS_PATH = r"C:\Users\hemanjali\Desktop\clg enquiry chatbot\models"

best_model = joblib.load(
    os.path.join(MODELS_PATH, "best_model.pkl")
)

vectorizer = joblib.load(
    os.path.join(MODELS_PATH, "tfidf_vectorizer.pkl")
)

# =========================================================
# TEXT PREPROCESSING
# =========================================================

def preprocess_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', '', text)

    return text

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎓 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Chatbot", "Project Info", "Model Performance"]
)

st.sidebar.markdown("---")

st.sidebar.subheader("⚡ Quick Questions")

quick_question = None

if st.sidebar.button("💰 Fees"):
    quick_question = "fee details"

if st.sidebar.button("📚 Courses"):
    quick_question = "courses offered"

if st.sidebar.button("🏢 Placements"):
    quick_question = "placement details"

if st.sidebar.button("🏠 Hostel"):
    quick_question = "hostel facilities"

if st.sidebar.button("📌 Admissions"):
    quick_question = "admission process"

# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    st.markdown(
        "<div class='main-title'>🎓 College AI Assistant</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sub-title'>Smart AI-powered chatbot for college enquiries</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1,1])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
            width=300
        )

    with col2:

        st.markdown("""
        <div class='card'>

        ## ✨ What This Chatbot Can Do

        ✔️ Admission Details  
        ✔️ Fee Structure  
        ✔️ Courses Information  
        ✔️ Placements  
        ✔️ Hostel Facilities  
        ✔️ Campus Facilities  

        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 🚀 Features")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class='feature-card'>
        <h3>🤖 Smart AI</h3>
        <p>Understands student queries instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='feature-card'>
        <h3>⚡ Fast Replies</h3>
        <p>Quick and accurate responses.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='feature-card'>
        <h3>🎨 Cute UI</h3>
        <p>Modern ChatGPT-style experience.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# CHATBOT PAGE
# =========================================================

elif page == "Chatbot":

    st.markdown(
        "<div class='chat-title'>💬 Chat with College AI Assistant</div>",
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    user_input = st.chat_input(
        "Ask anything about the college..."
    )

    if quick_question:
        user_input = quick_question

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        try:

            user_lower = user_input.lower()

            # =====================================================
            # MANUAL SMART RESPONSES
            # =====================================================

            if user_lower in ["hi", "hello", "hey"]:

                response = random.choice([
                    """
Hello 👋 Welcome to College AI Assistant!

✨ You can ask:
• admission process
• fee details
• placements
• hostel facilities
• courses offered
""",

                    """
Hi 😊 Glad to see you!

🎓 Ask me anything related to:
• admissions
• courses
• hostel
• placements
"""
                ])

            elif "fee" in user_lower:

                response = """
💰 Fee Structure

• CSE → ₹1,25,000  
• ECE → ₹1,10,000  
• EEE → ₹1,00,000  
• CIVIL → ₹90,000  

✨ You can also ask:
• hostel fee
• scholarship details
• payment options
"""

            elif "course" in user_lower:

                response = """
📚 Courses Offered

• Computer Science Engineering  
• Electronics & Communication  
• Electrical Engineering  
• Civil Engineering  
• Mechanical Engineering  

✨ You can also ask:
• best course
• duration
• syllabus
"""

            elif "placement" in user_lower:

                response = """
🏢 Placement Details

• Average Package → ₹4-6 LPA  
• Highest Package → ₹12 LPA  
• Top companies visit every year  

✨ You can also ask:
• highest package
• placement percentage
• recruiters
"""

            elif "hostel" in user_lower:

                response = """
🏠 Hostel Facilities

• Separate hostels for boys & girls  
• WiFi available  
• Hygienic food  
• 24/7 security  

✨ You can also ask:
• hostel fee
• room details
• hostel timings
"""

            elif "admission" in user_lower:

                response = """
📌 Admission Process

• Admissions through EAMCET/JEE  
• Management quota available  
• Online application supported  

✨ You can also ask:
• eligibility
• required documents
• last date
"""

            elif "facility" in user_lower:

                response = """
🏫 Campus Facilities

• Library  
• Computer Labs  
• Sports Complex  
• WiFi Campus  
• Transportation  

✨ You can also ask:
• canteen
• classrooms
• transport
"""

            elif "scholarship" in user_lower:

                response = """
🎓 Scholarship Details

• Merit scholarships available
• Government scholarships supported
• Fee reimbursement available

✨ You can also ask:
• eligibility
• scholarship amount
"""

            elif user_lower in ["thank you", "thanks", "tq", "thankyou"]:

                response = random.choice([
                    """
You're welcome 😊

💜 Thank you for visiting College AI Assistant!

✨ Visit again anytime.
""",

                    """
Happy to help 🎓

✨ You can return anytime for more queries.
"""
                ])

            elif user_lower in ["bye", "goodbye", "see you", "bye bye"]:

                response = random.choice([
                    """
Goodbye 👋

💜 Thank you for visiting our college assistant.

✨ Visit again anytime!
""",

                    """
See you again 😊

🎓 All the best for your future!
"""
                ])

            # =====================================================
            # ML MODEL RESPONSE
            # =====================================================

            else:

                cleaned = preprocess_text(user_input)

                vector = vectorizer.transform([cleaned])

                prediction = best_model.predict(vector)

                predicted_tag = prediction[0]

                if predicted_tag.lower() == "fees":

                    response = """
💰 Fee Details

• Tuition fee starts from ₹90,000 per year
• Scholarships available
• Installment payment option available

✨ You can also ask:
• hostel fee
• scholarship details
• branch-wise fee
"""

                elif predicted_tag.lower() == "admission":

                    response = """
📌 Admission Information

• Admissions through EAMCET/JEE
• Management quota available
• Online application supported

✨ You can also ask:
• eligibility
• required documents
• admission last date
"""

                elif predicted_tag.lower() == "courses":

                    response = """
📚 Courses Offered

• CSE
• ECE
• EEE
• CIVIL
• MECHANICAL

✨ You can also ask:
• course duration
• best branch
• seat intake
"""

                elif predicted_tag.lower() == "placements":

                    response = """
🏢 Placement Details

• Average Package → ₹4-6 LPA
• Top companies visit every year
• Placement training available

✨ You can also ask:
• highest package
• recruiting companies
"""

                elif predicted_tag.lower() == "hostel":

                    response = """
🏠 Hostel Facilities

• Separate hostels available
• WiFi enabled rooms
• Security available

✨ You can also ask:
• hostel fee
• food facility
"""

                else:

                    response = f"""
🤖 I understood your query related to: {predicted_tag}

✨ Suggested Questions:

• admission process
• fee details
• hostel facilities
• placements
• scholarship details
"""

            # =====================================================
            # DISPLAY BOT RESPONSE
            # =====================================================

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            with st.chat_message("assistant"):
                st.write(response)

        except Exception as e:

            st.error(f"Error: {e}")

# =========================================================
# PROJECT INFO PAGE
# =========================================================

elif page == "Project Info":

    st.markdown(
        "<div class='main-title'>📘 Project Information</div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='card'>

    ## 🎓 AI College Enquiry Chatbot

    This chatbot is developed using:

    ✔️ Machine Learning  
    ✔️ NLP (Natural Language Processing)  
    ✔️ TF-IDF Vectorization  
    ✔️ Logistic Regression  
    ✔️ Streamlit Frontend  

    ### 📌 Objective

    To provide instant responses to student queries related to:

    • Admissions  
    • Fees  
    • Courses  
    • Placements  
    • Hostel Facilities  

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MODEL PERFORMANCE PAGE
# =========================================================

elif page == "Model Performance":

    st.markdown(
        "<div class='main-title'>📊 Model Performance</div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='card'>

    ## ✅ Models Used

    • Logistic Regression  
    • Random Forest  
    • Decision Tree  

    ## 🎯 Best Model

    Logistic Regression achieved best accuracy.

    ## ⚡ Technologies Used

    • Python  
    • Scikit-learn  
    • Streamlit  
    • Pandas  
    • NLP  

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    "<div class='footer'>💜 Thank you for visiting College AI Assistant</div>",
    unsafe_allow_html=True
)