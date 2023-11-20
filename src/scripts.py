import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def plot_identified_models(listings_with_specs: pd.DataFrame, fig_title: str):
    # Define the specifications for the subplots
    specs = {
        "Brightness_number": "Brightness",
        "Resolution_width": "ResResolution",
        "Contrast_number": "Contrast",
    }
    titles = ["Brightness vs Price", "Resolution Width vs Price", "Contrast vs Price"]
    x_titles = ["Brightness (lumens)", "Resolution Width (pixels)", "Contrast Ratio"]

    # Create a subplot with 1 row and 3 columns
    fig = make_subplots(rows=1, cols=3, subplot_titles=titles)

    # Loop through the specs to create each plot
    for i, spec in enumerate(list(specs.keys()), start=1):
        link = listings_with_specs["Link"]
        fig.add_trace(
            go.Scatter(
                x=listings_with_specs[spec],
                y=listings_with_specs["Price"],
                text="Title: "
                + listings_with_specs["Title"]
                + "<br>"
                + specs[spec]
                + ": "
                + listings_with_specs[specs[spec]]
                + "<br>"
                + "Specs based on: "
                + listings_with_specs["Matched Model"]
                + "<br>"
                + f'<a href="{link}"> Link to Kleinanzeigen</a>',
                mode="markers",
                hoverinfo="text",
                name=spec,
            ),
            row=1,
            col=i,
        )

        # Update x-axis title
        fig.update_xaxes(title_text=x_titles[i - 1], row=1, col=i)

    # Update y-axis title (common for all subplots)
    fig.update_yaxes(title_text="Price (EUR)", row=1, col=1)

    # Update layout to fit your preferences
    fig.update_layout(
        height=600,
        width=1800,
        title_text=fig_title,
        showlegend=False,
        clickmode="select",
        hovermode="closest",
    )
    return fig


def plot_unidentified_listings(unidentified_listings):
    scatter_trace = go.Scatter(
        y=unidentified_listings["Title"],
        x=unidentified_listings["Price"],
        text="Title: "
        + unidentified_listings["Title"]
        + "<br>"
        + "Price: "
        + unidentified_listings["Price"].astype(str)
        + "<br>"
        + "Description: "
        + unidentified_listings["Description"],
        mode="markers",
        hoverinfo="text",
    )
    fig = go.Figure(scatter_trace)
    fig.update_layout(
        height=1200,
        title="Unidentified Listings",
    )
    return fig
