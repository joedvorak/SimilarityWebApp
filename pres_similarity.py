import numpy as np
import streamlit as st
import pandas as pd
from streamlit_js_eval import streamlit_js_eval
from time import sleep

st.set_page_config(
    page_title="Presentation Similarity",
    page_icon=":material/category_search:",
    layout="wide",
)


# Load your DataFrames
df_presentations_all = pd.read_pickle("oral_df_doc.pkl")
df_similarity = pd.read_pickle("nomic_similarities_oral.pkl")

df_presentations = df_presentations_all[['Owner-First Name', 'Owner-Last Name', 'Title', 'Abstract']]

screen_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',)
#sleep(1)
st.subheader("Check similarity between presentations.")
st.write("Select a presentation by clicking on the checkbox. You can sort the presentation list or search as well.")
st.write("Once a presentation is selected, its abstract and the ten most similar presentations will appear.")
sleep(75/1000)
st.write(screen_width)

if screen_width > 800:  # Wide screen layout
    col_preslist, col_similar = st.columns([1,1])

    with col_preslist:
        st.header("Select a Presentation")
        event = st.dataframe(
                df_presentations,
                #column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
            )


        st.header("Presentation Details")
        if event.selection.rows:
            selected_pres = df_presentations.iloc[event.selection.rows]
            st.write(selected_pres.iloc[0]['Title'])
            st.write(f"**Presenter:** {selected_pres.iloc[0]['Owner-First Name']} {selected_pres.iloc[0]['Owner-Last Name']}")
            st.write(f"**Abstract:** {selected_pres.iloc[0]['Abstract']}")
    with col_similar:
        if event.selection.rows:
            st.header("Most Similar Presentations")
            similar_presentations = df_similarity.loc[selected_pres.iloc[0].name].sort_values(ascending=False)
            # Remove the selected presentation itself from the similar presentations
            similar_presentations = similar_presentations.drop(selected_pres.iloc[0].name)

            for i, (index, score) in enumerate(similar_presentations.head(10).items(), 1):  # Start enumeration from 1  # Show top 10
                similar_row = df_presentations.loc[index]
                st.write(f"**{i}:** {similar_row["Title"]}")
                st.write(f"**Presenter:** {similar_row['Owner-First Name']} {similar_row['Owner-Last Name']} ")
                #st.write(f"**Abstract:** {similar_row['Abstract']}")
                st.write(f"**Similarity Score:** {score:.2f}")
else:
    st.header("Select a Presentation")
    event = st.dataframe(
            df_presentations,
            #column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )


    st.header("Presentation Details")
    if event.selection.rows:
        selected_pres = df_presentations.iloc[event.selection.rows]
        st.write(selected_pres.iloc[0]['Title'])
        st.write(f"**Presenter:** {selected_pres.iloc[0]['Owner-First Name']} {selected_pres.iloc[0]['Owner-Last Name']}")
        st.write(f"**Abstract:** {selected_pres.iloc[0]['Abstract']}")

    if event.selection.rows:
        st.header("Most Similar Presentations")
        similar_presentations = df_similarity.loc[selected_pres.iloc[0].name].sort_values(ascending=False)
        # Remove the selected presentation itself from the similar presentations
        similar_presentations = similar_presentations.drop(selected_pres.iloc[0].name)

        for i, (index, score) in enumerate(similar_presentations.head(10).items(), 1):  # Start enumeration from 1  # Show top 10
            similar_row = df_presentations.loc[index]
            st.write(f"**{i}:** {similar_row["Title"]}")
            st.write(f"**Presenter:** {similar_row['Owner-First Name']} {similar_row['Owner-Last Name']} ")
            #st.write(f"**Abstract:** {similar_row['Abstract']}")
            st.write(f"**Similarity Score:** {score:.2f}")
