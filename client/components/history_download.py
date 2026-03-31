
import streamlit as st 


def render_history_download():
    if st.session_state.get("conversation_history"):
        st.download_button(
            label="Download Conversation History",
            data="\n\n".join(st.session_state.conversation_history),
            file_name="conversation_history.txt",
            mime="text/plain"
        )