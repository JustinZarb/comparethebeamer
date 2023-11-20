import streamlit as st
import pandas as pd
import src.scripts as scripts
import os

st.set_page_config(layout="wide")

st.title("Beamers on Kleinanzeigen")

saved_selections = os.listdir("./data")
specifications = [
    s
    for s in saved_selections
    if s.startswith("Projector Specifications Comparison") and s.endswith(".csv")
]

specifications_sorted = {
    s.split("Price ")[1].split(".csv")[0]: s for s in specifications
}
specifications_sorted = dict(sorted(specifications_sorted.items(), reverse=True))

st.session_state["retrieval_date"] = list(specifications_sorted.keys())[0]

filename = specifications_sorted.get(st.session_state["retrieval_date"])

st.markdown(f"Data from {st.session_state['retrieval_date'].replace('.',':')}")

########################################################################
st.header("Identified Models")
st.session_state["specifications"] = pd.read_csv(f"./data/{filename}")


st.slider(
    label="Minimum Brightness (lm)",
    min_value=0,
    step=1000,
    max_value=10000,
    key="brightness_slider",
)
st.slider(
    label="Minimum Resolution width (px)",
    min_value=0,
    step=100,
    max_value=2000,
    key="resolution_slider",
)
st.slider(
    label="Minimum Contrast",
    min_value=0,
    step=1000,
    max_value=100000,
    key="contrast_slider",
)

sub_selection = st.session_state.specifications.loc[
    (
        st.session_state.specifications.loc[:, "Brightness_number"]
        > st.session_state.brightness_slider
    )
    & (
        st.session_state.specifications.loc[:, "Contrast_number"]
        > st.session_state.contrast_slider
    )
    & (
        st.session_state.specifications.loc[:, "Resolution_width"]
        > st.session_state.resolution_slider
    ),
    :,
]

fig = scripts.plot_identified_models(
    sub_selection,
    specifications_sorted.get(st.session_state.retrieval_date),
)
st.plotly_chart(fig, use_container_width=True)


st.text_input(label="Filter known models:", key="search_text")

st.dataframe(
    sub_selection.loc[
        st.session_state.specifications.loc[:, "Title"]
        .str.lower()
        .str.contains(st.session_state.search_text.lower())
    ]
    .drop("Unnamed: 0", axis=1)
    .loc[
        :,
        [
            "Title",
            "Matched Model",
            "ResResolution",
            "Contrast",
            "Brightness",
            "Technology",
            "Audible Noise",
            "Year",
            "Link",
        ],
    ]
)

################################################################
st.header("Unidentified Models")
st.markdown(
    "Below are the remaining search results where no model could be identified. "
)
unidentified_filename = [
    s
    for s in saved_selections
    if s.startswith("unidentified")
    and s.endswith(f"{st.session_state.retrieval_date}.csv")
]
st.session_state["unidentified_df"] = pd.read_csv(f"./data/{unidentified_filename[0]}")

# Create scatter plot

st.plotly_chart(
    scripts.plot_unidentified_listings(st.session_state["unidentified_df"]),
    use_container_width=True,
)

st.text_input(label="Filter unidentified listings:", key="search_text_unidentified")
st.dataframe(
    st.session_state.unidentified_df.loc[
        st.session_state.unidentified_df.loc[:, "Title"]
        .str.lower()
        .str.contains(st.session_state.search_text_unidentified.lower())
    ].drop("Unnamed: 0", axis=1)
)
