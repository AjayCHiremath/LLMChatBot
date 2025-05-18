import streamlit as st

def get_user_input(disabled=False):
    with st.form(key="user_input_form", clear_on_submit=True):
        cols = st.columns([7.5, 0.3, 0.3])

        user_input = cols[0].text_input(
            "Message",
            label_visibility="collapsed",
            placeholder="Type your message here..."
        )
        submitted = cols[1].form_submit_button("➤", disabled=disabled)
        cleared = cols[2].form_submit_button("🗑️", disabled=disabled)  # Clear chat button

    # Clear state if Clear button clicked
    if cleared:
        st.session_state.chat_history = []
        st.session_state.generating_response = False
        st.session_state.run_chain = False
        st.session_state.current_input = ""
        st.rerun()

    return user_input, submitted