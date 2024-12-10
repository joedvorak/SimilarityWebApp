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
df_similarity = pd.read_pickle("nomic_similarities_oral.pkl") # Similarities for the presentations. Indexes and Columns are the same and match the Indexes in df_presentation.

df_presentations = df_presentations_all[['Owner-First Name', 'Owner-Last Name', 'Title', 'Abstract']]

screen_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',)

st.subheader("Check similarity between presentations.")
st.write("Select a presentation by clicking on the checkbox. You can sort the presentation list or search as well.")
st.write("Once a presentation is selected, its abstract and the ten most similar presentations will appear.")
st.write("If you move your mouse over the table, a menu will appear in the top left corner that lets you search within the table or download. Clicking on columns will let you sort by the column too. If text is cut off, click on an cell to see the full text.")
sleep(75/1000) # Pause to allow javascript to return screen_width.

if screen_width > 800:  # Wide screen layout
    col_preslist, col_similar = st.columns([1,1])

    with col_preslist:
        st.header("Select a Presentation")
        event = st.dataframe(
                df_presentations,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
            )


        st.header("Presentation Details")
        if event.selection.rows: # Check if a presentation has been selected.
            selected_pres = df_presentations.iloc[event.selection.rows] # Create a dataframe from the selected presentation row.
            st.write(selected_pres.iloc[0]['Title']) # It is necessary to request the first row, [0], since it is a dataframe and not just one entry.
            st.write(f"**Presenter:** {selected_pres.iloc[0]['Owner-First Name']} {selected_pres.iloc[0]['Owner-Last Name']}")
            st.write(f"**Abstract:** {selected_pres.iloc[0]['Abstract']}")
    with col_similar:
        if event.selection.rows:
            st.header("Most Similar Presentations")
            similar_presentations = df_similarity.loc[selected_pres.iloc[0].name].sort_values(ascending=False) # Create a Series with the 10 most similar presentations
            # Remove the selected presentation itself from the similar presentations
            similar_presentations = similar_presentations.drop(selected_pres.iloc[0].name)
            # Build the similarity dataframe. Add the similarity score and similarity rank to the dataframe and show it.
            similar_df = df_presentations.loc[similar_presentations.index]
            similar_df.insert(0, "Similarity Score", similar_presentations)
            similar_df.insert(0, "Similarity Rank", np.arange(1,similar_df.shape[0]+1))
            st.dataframe(
                similar_df,
                use_container_width=True,
                hide_index=True,
                )
else:
    st.header("Select a Presentation")
    event = st.dataframe(
            df_presentations,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )

    st.header("Presentation Details")
    if event.selection.rows: # Check if a presentation has been selected.
        selected_pres = df_presentations.iloc[event.selection.rows]  # Create a dataframe from the selected presentation row.
        st.write(selected_pres.iloc[0]['Title'])  # It is necessary to request the first row, [0], since it is a dataframe and not just one entry.
        st.write(f"**Presenter:** {selected_pres.iloc[0]['Owner-First Name']} {selected_pres.iloc[0]['Owner-Last Name']}")
        st.write(f"**Abstract:** {selected_pres.iloc[0]['Abstract']}")

    if event.selection.rows:
        st.header("Most Similar Presentations")
        similar_presentations = df_similarity.loc[selected_pres.iloc[0].name].sort_values(ascending=False) # Create a Series with the 10 most similar presentations
        # Remove the selected presentation itself from the similar presentations
        similar_presentations = similar_presentations.drop(selected_pres.iloc[0].name)
        # Build the similarity dataframe. Add the similarity score and similarity rank to the dataframe and show it.
        similar_df = df_presentations.loc[similar_presentations.index]
        similar_df.insert(0, "Similarity Score", similar_presentations)
        similar_df.insert(0, "Similarity Rank", np.arange(1,similar_df.shape[0]+1))
        st.dataframe(
            similar_df,
            use_container_width=True,
            hide_index=True,
            )
