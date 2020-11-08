import csv

import streamlit as st


@st.cache
def load_talks():
    with open("talks.csv") as f:
        return list(csv.DictReader(f))


st.title("May you find a great talk.")

data_load_state = st.text("Loading Data...")
talks = load_talks().copy()  # TODO: copyは必須？
tracks = list({t["track"] for t in talks})
python_levels = list({t["audience_python_level"] for t in talks})
expertises = list({t["audience_expertise"] for t in talks})
data_load_state.text("Loading Data...Done!")

track_selections = st.multiselect("Select track", tracks)
talks = [t for t in talks if t["track"] in track_selections]

python_level_selections = st.multiselect(
    "Select audience Python level", python_levels
)
if python_level_selections:
    talks = [
        t
        for t in talks
        if t["audience_python_level"] in python_level_selections
    ]

expertise_selections = st.multiselect("Select audience expertise", expertises)
if expertise_selections:
    talks = [
        t for t in talks if t["audience_expertise"] in expertise_selections
    ]

# TODO: ブラッシュアップ
keyword = st.text_input("Keyword")
if keyword:
    talks = [t for t in talks if keyword in t["title"]]

if st.checkbox("Only English talks"):
    talks = [
        t
        for t in talks
        if t["lang_of_talk"] == "English"
        or t["lang_of_slide"] != "Japanese only"
    ]

searched = [
    {
        "title": talk["title"],
        "day": talk["day"],
        "track": talk["track"],
        "room": talk["room"],
        "audience": talk["audience_python_level"],
        "expertise": talk["audience_expertise"],
        "speaking": talk["lang_of_talk"],
        "slide": talk["lang_of_slide"],
    }
    for talk in talks
]
st.table(searched)
