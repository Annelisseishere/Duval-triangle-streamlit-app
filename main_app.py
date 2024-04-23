import streamlit as st

# Ensure this is the very first command executed
st.set_page_config(page_title="Duval Triangle Analysis", layout="wide")

# Now import the other modules
import app3
import app4

def main():
    st.sidebar.title("Navigation")
    app_pages = {
        "Single Triangle Analysis": app3.main,
        "Compare Two Triangles": app4.main
    }

    selected_page = st.sidebar.radio("Choose a page", list(app_pages.keys()))
    app_pages[selected_page]()

if __name__ == "__main__":
    main()
