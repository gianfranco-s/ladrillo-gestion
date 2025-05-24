import streamlit as st

def hide_deploy_button() -> None:
    """
    Hides the deploy button and the top-right menu in Streamlit.
    """
    hide_deploy_css = """
    <style>
      /* target the Deploy button by its data-test id */
      [data-testid="stAppDeployButton"] {
        display: none !important;
      }
      /* hide the top-right “…” menu */
      .stMainMenu,
      .st-emotion-cache-czk5ss.e8lvnlb8 {
        display: none !important;
      }
    </style>
    """
    st.markdown(hide_deploy_css, unsafe_allow_html=True)