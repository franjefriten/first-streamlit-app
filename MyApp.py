import streamlit as st
import requests
import pandas as pd
import altair as alt
import datetime

margins_css = """
    <style>
        .main > div {
            padding-left: 0em;
            padding-right: 0em;
        }
    </style>
"""

# st.markdown(margins_css, unsafe_allow_html=True)
st.set_page_config(
    page_title="Spotify Analysis",
    layout="wide",
    page_icon=":material/rocket:"
)

@st.cache_data
def load_data():
    df_dictionary = pd.read_csv("data/spotify_data_dictionary.csv")
    df_data = pd.read_csv("data/spotify_history.csv")
    df_data["ts"] = pd.to_datetime(df_data["ts"], yearfirst=True)
    return df_data, df_dictionary

st.title("Spotify Analysis")
carga_datos = st.text("Loading data ...")
df_data, df_dictionary = load_data()
carga_datos.text("Data Loaded!")

@st.fragment()
def show_data():
    st.dataframe(df_data.head(), use_container_width=True)

if st.checkbox("Show Raw Data"):
    show_data()

container_cols = st.columns(spec=[1, 1, 1])

# TOP TRACKS, ROW:1, COL:1

top_tracks = df_data["track_name"].\
    value_counts().\
        sort_values(ascending=False).reset_index().iloc[:10]

top_tracks = pd.DataFrame(
    index=top_tracks.index,
    columns=top_tracks.columns,
    data=top_tracks.values
)

r1c1 = alt.Chart(
    top_tracks,
    title=alt.Title("Top 10 Tracks", anchor="middle", fontSize=20)
).\
    mark_bar().\
        encode(
            x=alt.X("track_name").sort("-y").title("Track Name"),
            y=alt.Y("count").title("Total"),
            color=alt.value('darkorange')
        )

# TOP ARTISTS, ROW:1, COL:2

top_artists = df_data["artist_name"].\
    value_counts().\
        sort_values(ascending=False).reset_index().iloc[:10]

top_artists = pd.DataFrame(
    index=top_artists.index,
    columns=top_artists.columns,
    data=top_artists.values
)

r1c2 = alt.Chart(
    top_artists,
    title=alt.Title("Top 10 Artists", anchor="middle", fontSize=20),
).\
    mark_bar().\
        encode(
            x=alt.X("artist_name").sort("-y").title("Artist Name"),
            y=alt.Y("count").title("Total"),
            color=alt.value('darkorange')
        )

# TOP ALBUMS, ROW:1, COL:3

top_album = df_data["album_name"].\
    value_counts().\
        sort_values(ascending=False).reset_index().iloc[:10]

top_album = pd.DataFrame(
    index=top_album.index,
    columns=top_album.columns,
    data=top_album.values
)

r1c3 = alt.Chart(
    top_album,
    title=alt.Title("Top 10 Albums", anchor="middle", fontSize=20),
).\
    mark_bar().\
        encode(
            x=alt.X("album_name").sort("-y").title("Album Name"),
            y=alt.Y("count").title("Total"),
            color=alt.value('darkorange')
        )


container_cols[0].altair_chart(r1c1, use_container_width=True)
container_cols[1].altair_chart(r1c2, use_container_width=True)
container_cols[2].altair_chart(r1c3, use_container_width=True)

# ARTIST LINE CHART ROW:2, COLS:ALL

artist_select = st.selectbox(label="Select Artist", options=df_data.artist_name.unique())

min_date = df_data["ts"].min()
max_date = df_data["ts"].max()

time_select = st.select_slider(
    label="Select Date Range",
    options=df_data.loc[(df_data["ts"] >= min_date) & (df_data["ts"] <= max_date), "ts"].values,
    value=(
        min_date,
        max_date
    )
)

artist_line_chart = df_data.loc[df_data.artist_name == artist_select, ["ts", "ms_played"]]
artist_line_chart = artist_line_chart.\
    loc[(artist_line_chart["ts"] > time_select[0]) & (artist_line_chart["ts"] < time_select[1]), :]
artist_line_chart["ms_played"] = artist_line_chart["ms_played"]/1000

artist_altair_chart = alt.Chart(
    data=artist_line_chart,
    title=alt.Title(
        text="Artist Time Series",
        anchor="middle",
        fontSize=20
    )
).mark_bar().encode(
    x=alt.X("ts:T").title("Date"),
    y=alt.Y("ms_played:Q").title("Time played (s)"),
    color=alt.value('darkorange')
)

st.altair_chart(artist_altair_chart, use_container_width=True)