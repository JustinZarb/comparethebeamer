import streamlit as st
import pandas as pd
import src.scripts as scripts
import os

st.set_page_config(layout="wide")
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


################################################################
st.title(":film_projector: Beamers on Kleinanzeigen ")
st.markdown(f"Latest retrieval: {st.session_state['retrieval_date'].replace('.',':')}")
st.markdown(
    """Hello, and welcome to the Beamer (aka. Projector) comparison page! The goal of \
        this project is to make good deals easier to spot by identifying the model of \
        the Beamer and displaying the specifications according to projectorcentral.com. \
        The matching is not perfect, so look out for mis-matches between the title \
        and matched model, and always check the photos! Use the sliders to change \
        the minimum value of brightness, resolution width and 
        contrast ratio. The graphs and table below will update. Use the link in the table to \
        get back to the original listing."""
)
########################################################################
st.header(":sparkles: Identified Models")

st.markdown(
    "Around 35\% of all the listings can be matched to a model on projectorcentral.com. Mismatches are mainly caused by typos in the listings."
)

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
    "Listing Prices by Brightness, Resolution and Contrast",
)
st.plotly_chart(fig, use_container_width=True)


st.text_input(label="Search for specific text in the title:", key="search_text")

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
            "Price",
            "Title",
            "Description",
            "Matched Model",
            "ResResolution",
            "Contrast",
            "Brightness",
            "Technology",
            "Audible Noise",
            "Year",
            "Link",
        ],
    ],
    use_container_width=True,
)

################################################################
st.header(":grey_question: Unidentified Listings")
st.markdown(
    "There may be some hidden gems among the remaining ~65\% of search results where no model could be identified. To make things easier, some common irrelevant listings like 'Jim Beam' were removed."
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
    ].drop("Unnamed: 0", axis=1),
    use_container_width=True,
)
