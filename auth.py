import streamlit as st
from db import users_collection
from utils import hash_password, verify_password
import extra_streamlit_components as stx


cookie_manager = stx.CookieManager()



def init_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "username" not in st.session_state:
        st.session_state.username = None

   
    user = cookie_manager.get("username")

    if user:
        st.session_state.authenticated = True
        st.session_state.username = user



def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return False

    users_collection.insert_one({
        "username": username,
        "password": hash_password(password)
    })
    return True


def login_user(username, password):
    user = users_collection.find_one({"username": username})

    if user and verify_password(password, user["password"]):
        return True
    return False



def show_auth_page():
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("🔑 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username

                
                cookie_manager.set("username", username)

                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Sign Up":
        st.subheader("📝 Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            if register_user(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("User already exists")

    st.stop()



def logout():
    st.session_state.authenticated = False
    st.session_state.username = None

    cookie_manager.delete("username")

    st.rerun()