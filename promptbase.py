import os
import datetime
import zoneinfo

import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

con = psycopg2.connect(os.getenv("DATABASE_URL"))

with con:
    with con.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS prompts 
            (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                prompt TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

def edit_page(prompt_id):
    with con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM prompts WHERE id = %s", (prompt_id,))
            prompt = cur.fetchone()
    with st.form("edit_prompt"):
        title = st.text_input("Title", prompt[1])
        prompt_text = st.text_area("Prompt", prompt[2])
        is_save = st.form_submit_button('Save')
    if is_save:
        with con:
            with con.cursor() as cur:
                cur.execute(
                    "UPDATE prompts SET title = %s, prompt = %s, updated_at = %s WHERE id = %s",
                    (title, prompt_text, datetime.datetime.now(datetime.UTC), prompt_id)
                )
        st.query_params['page'] = "detail"
        st.rerun()

def detail_page(prompt_id):
    st.button("Back", on_click=set_page, args=("list",))
    with con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM prompts WHERE id = %s", (prompt_id,))
            prompt = cur.fetchone()
    st.header(prompt[1])
    st.write(prompt[4].astimezone(zoneinfo.ZoneInfo('America/Los_Angeles')))
    st.write(prompt[2])
    cols = st.columns(2)
    cols[0].button("Edit", on_click=set_page, args=("edit",))

    if cols[1].button("Delete", type="primary"):
        with con:
            with con.cursor() as cur:
                cur.execute("DELETE FROM prompts WHERE id = %s", (prompt_id,))
        st.query_params.clear()
        st.rerun()

def list_page():
    search_input = st.text_input("Search")
    with con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM prompts")
            prompts = cur.fetchall()
    prompts = [prompt for prompt in prompts if search_input.lower() in prompt[1].lower()]
    for prompt in prompts:
        st.markdown(f'<a href="?id={prompt[0]}&page=detail" target="_self">{prompt[1]}</a>', unsafe_allow_html=True)

def create_page():
    st.write("Create a new prompt")
    with st.form("prompt"):
        title = st.text_input("Title")
        prompt = st.text_area('Prompt')
        is_save = st.form_submit_button('Save')
    if is_save:
        with con:
            with con.cursor() as cur:
                cur.execute(
                    "INSERT INTO prompts (title, prompt) VALUES (%s, %s)",
                    (title, prompt)
                )
        st.query_params.clear()
        st.rerun()


def set_page(page):
    st.query_params["page"] = page

prompt_id = st.query_params.get("id")
if st.query_params.get("page") == "detail":
    detail_page(prompt_id)
elif st.query_params.get("page") == "create":
    create_page()
elif st.query_params.get("page") == "edit":
    edit_page(prompt_id)
else:
    st.button("Create a new prompt", on_click=set_page, args=("create",))
    list_page()