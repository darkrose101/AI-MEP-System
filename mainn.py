import streamlit as st
from tryy import MEP
from stc import Home

def main():
    st.set_page_config(page_title="Modular Streamlit App",
                        page_icon="🏂",
                        layout="wide")

    page_options = ["Home", "Monitoring, Evaluation and Performance"]
    selected_page = st.sidebar.selectbox("Select Page", page_options)

    if selected_page == "Home":
        Home()
    elif selected_page == "Monitoring, Evaluation and Performance":
        MEP()
    elif selected_page == "Contact":
        st.write("Contacts and About PAge will be uploaded soon")


if __name__ == "__main__":
    main()
