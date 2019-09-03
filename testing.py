from textwrap import dedent
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_player as player
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pathlib

FRAMERATE = 24.0

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config.suppress_callback_exceptions = True

BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()


def markdown_popup():
    return html.Div(
        id="markdown",
        className="modal",
        style={"display": "none"},
        children=(
            html.Div(
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=[
                            dcc.Markdown(
                                children=dedent(
                                    """
                                ##### What am I looking at?
                                
                                This app enhances visualization of objects detected using state-of-the-art Mobile Vision Neural Networks.
                                Most user generated videos are dynamic and fast-paced, which might be hard to interpret. A confidence
                                heatmap stays consistent through the video and intuitively displays the model predictions. The pie chart
                                lets you interpret how the object classes are divided, which is useful when analyzing videos with numerous
                                and differing objects.
                                ##### More about this Dash app
                                
                                The purpose of this demo is to explore alternative visualization methods for object detection. Therefore,
                                the visualizations, predictions and videos are not generated in real time, but done beforehand. To read
                                more about it, please visit the [project repo](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-object-detection).
                                """
                                )
                            )
                        ],
                    ),
                ],
            )
        ),
    )



app.layout = html.Div(
    children=[
        html.Div(id="top-bar", className="row"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    id="left-side-column",
                    className="eight columns",
                    children=[
                        html.Img(
                            id="logo-mobile", src=app.get_asset_url("dash-logo.png")
                        ),
                        html.Div(
                            id="header-section",
                            children=[
                                html.H4("Object Detection Explorer"),
                                html.P(
                                    "To get started, select the footage you want to view, and choose the display mode (with or without "
                                    "bounding boxes). Then, you can start playing the video, and the result of objects detected "
                                    "will be displayed in accordance to the current video-playing time."
                                ),
                                html.Button(
                                    "Learn More", id="learn-more-button", n_clicks=0
                                ),
                            ],
                        ),
                        html.Div(
                            className="video-outer-container",
                            children=html.Div(
                                className="video-container",
                                children=player.DashPlayer(
                                    id="video-display",
                                    url="https://www.youtube.com/watch?v=gPtn6hD7o8g",
                                    controls=True,
                                    playing=False,
                                    volume=1,
                                    width="100%",
                                    height="100%",
                                ),
                            ),
                        ),
                        html.Div(
                            className="control-section",
                            children=[
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(
                                            children=["Minimum Confidence Threshold:"]
                                        ),
                                        html.Div(
                                            dcc.Slider(
                                                id="slider-minimum-confidence-threshold",
                                                min=20,
                                                max=80,
                                                marks={
                                                    i: f"{i}%"
                                                    for i in range(20, 81, 10)
                                                },
                                                value=30,
                                                updatemode="drag",
                                            )
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(children=["Footage Selection:"]),
                                        dcc.Dropdown(
                                            id="dropdown-footage-selection",
                                            options=[
                                                {
                                                    "label": "Drone recording of canal festival",
                                                    "value": "DroneCanalFestival",
                                                },
                                                {
                                                    "label": "Drone recording of car festival",
                                                    "value": "car_show_drone",
                                                },
                                                {
                                                    "label": "Drone recording of car festival #2",
                                                    "value": "DroneCarFestival2",
                                                },
                                                {
                                                    "label": "Drone recording of a farm",
                                                    "value": "FarmDrone",
                                                },
                                                {
                                                    "label": "Lion fighting Zebras",
                                                    "value": "zebra",
                                                },
                                                {
                                                    "label": "Man caught by a CCTV",
                                                    "value": "ManCCTV",
                                                },
                                                {
                                                    "label": "Man driving expensive car",
                                                    "value": "car_footage",
                                                },
                                                {
                                                    "label": "Restaurant Robbery",
                                                    "value": "RestaurantHoldup",
                                                },
                                            ],
                                            value="car_show_drone",
                                            clearable=False,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(children=["Video Display Mode:"]),
                                        dcc.Dropdown(
                                            id="dropdown-video-display-mode",
                                            options=[
                                                {
                                                    "label": "Regular Display",
                                                    "value": "regular",
                                                },
                                                {
                                                    "label": "Display with Bounding Boxes",
                                                    "value": "bounding_box",
                                                },
                                            ],
                                            value="bounding_box",
                                            searchable=False,
                                            clearable=False,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(children=["Graph View Mode:"]),
                                        dcc.Dropdown(
                                            id="dropdown-graph-view-mode",
                                            options=[
                                                {
                                                    "label": "Visual Mode",
                                                    "value": "visual",
                                                },
                                                {
                                                    "label": "Detection Mode",
                                                    "value": "detection",
                                                },
                                            ],
                                            value="visual",
                                            searchable=False,
                                            clearable=False,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="right-side-column",
                    className="four columns",
                    children=[
                        html.Div(
                            className="img-container",
                            children=html.Img(
                                id="logo-web", src=app.get_asset_url("dash-logo.png")
                            ),
                        ),
                        html.Div(id="div-visual-mode"),
                        html.Div(id="div-detection-mode"),
                    ],
                ),
            ],
        ),
        markdown_popup(),
    ]
)



if __name__ == "__main__":
    app.run_server(debug=True, port=8053)
