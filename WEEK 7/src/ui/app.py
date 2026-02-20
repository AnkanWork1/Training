import streamlit as st
import requests
from pathlib import Path

API = "http://localhost:8000"

st.set_page_config(layout="wide")
st.title("Multimodal RAG + SQL Assistant")

tabs = st.tabs(["Ask (Text)", "Ask (Image)", "Ask (SQL)"])

# ------------------------------------------------------
# TEXT
# ------------------------------------------------------
with tabs[0]:

    st.header("Text RAG")

    question = st.text_area("Question")
    top_k = st.number_input("top_k", 1, 50, 10)

    if st.button("Ask (text)"):
        r = requests.post(
            f"{API}/ask",
            data={
                "question": question,
                "top_k": top_k
            }
        )

        out = r.json()

        st.subheader("Answer")
        st.write(out["answer"])

        if out.get("image"):
            st.subheader("Top image")
            st.image(out["image"])

        st.subheader("Metrics")
        st.json(out["metrics"])


# ------------------------------------------------------
# IMAGE
# ------------------------------------------------------
with tabs[1]:

    st.header("Image RAG")

    file = st.file_uploader("Upload image", type=["png","jpg","jpeg","bmp","webp"])
    top_k = st.number_input("top_k (image)", 1, 50, 10, key="img_k")

    if st.button("Ask (image)") and file is not None:

        r = requests.post(
            f"{API}/ask-image",
            files={"file": file},
            data={"top_k": top_k}
        )

        out = r.json()

        st.subheader("Answer")
        st.write(out["answer"])

        if out.get("image"):
            st.subheader("Top image")
            st.image(out["image"])

        st.subheader("Metrics")
        st.json(out["metrics"])


# ------------------------------------------------------
# SQL
# ------------------------------------------------------
with tabs[2]:

    st.header("SQL QA")

    db_path = st.text_input("SQLite DB path")
    question = st.text_area("Question (SQL)")

    if st.button("Ask SQL"):

        r = requests.post(
            f"{API}/ask-sql",
            data={
                "db_path": db_path,
                "question": question
            }
        )

        out = r.json()

        st.subheader("Generated SQL")
        st.code(out["sql"], language="sql")

        st.subheader("Summary")
        st.write(out["summary"])

        st.subheader("Rows")
        st.write(out["rows"])
