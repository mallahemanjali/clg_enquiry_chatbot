import streamlit as st
import joblib
import json
import os

# ====================== YOUR PATH ======================
MODELS_PATH = r'C:\Users\hemanjali\Desktop\clg enquiry chatbot\models'
# ======================================================

st.set_page_config(page_title="College Chatbot", layout="wide")

# Load Model
@st.cache_resource
def load_model():
    model = joblib.load(f'{MODELS_PATH}/chatbot_model.pkl')
    vectorizer = joblib.load(f'{MODELS_PATH}/tfidf_vectorizer.pkl')
    encoder = joblib.load(f'{MODELS_PATH}/label_encoder.pkl')
    return model, vectorizer, encoder

model, vectorizer, encoder = load_model()

# Load responses from intents.json
with open('data/intents.json', 'r', encoding='utf-8') as f:
    intents_data = json.load(f)

response_dict = {item['tag']: item['responses'] for item in intents_data['intents']}

# Sidebar
st.sidebar.title("🎓 Navigation")
page = st.sidebar.radio("Choose Page", ["Home", "💬 Chatbot", "Project Info", "Model Performance"])

# Home Page
if page == "Home":
    st.title("🎓 College Enquiry AI Chatbot")
    st.subheader("Welcome! Ask me anything about the college")

# Chatbot Page
if page == "💬 Chatbot":
    st.title("💬 Chat with College AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        try:
            vector = vectorizer.transform([prompt])
            pred = model.predict(vector)[0]
            intent = encoder.inverse_transform([pred])[0]
            
            reply = response_dict.get(intent, ["Sorry, I don't understand."])[0]
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)
        except Exception as e:
    st.error(f"Error: {e}")

# Other Pages
if page == "Project Info":
    st.title("About the Project")
    st.info("This is an AI Chatbot for College Enquiry System - B.Tech Project")

if page == "Model Performance":
    st.title("Model Performance")
    st.success("✅ Final Accuracy: Greater than 95%")
    st.write("Best Model: Optimized Logistic Regression")

st.caption("B.Tech Project | AI College Enquiry Chatbot")