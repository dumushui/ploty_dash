from textwrap import dedent
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_player as player
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from path_testing import files_
import pathlib
import flask


f = files_('data')


external_stylesheets = ['https:/codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.config.suppress_callback_exceptions = True



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





# app.layout = html.Div(
#     children=[
#         html.Img(id="logo-mobile", src="http://www.walterhuang.xyz/aidriving/logo.jpg"),
#         html.Button("Learn More", id="learn-more-button", n_clicks=0),
#         markdown_popup(),
#    #      dcc.Markdown('''
#             # #### Dash and Markdown

#             # Dash supports [Markdown](http://commonmark.org/help).

#             # Markdown is a simple way to write and format text.
#             # It includes a syntax for things like **bold text** and *italics*,
#             # [links](http://commonmark.org/help), inline `code` snippets, lists,
#             # quotes, and more.
#             # '''),
#         dcc.RadioItems(
#             options=[
#             {'label': '良好', 'value': 'GOOD'},
#             {'label': '复杂', 'value': 'BAD'},],
#             value='GOOD',
#             labelStyle={'display': 'inline-block'}
#             ),
#         dcc.RadioItems(
#             options=[
#             {'label': '良好', 'value': 'GOOD'},
#             {'label': '复杂', 'value': 'BAD'},],
#             value='GOOD',
#             labelStyle={'display': 'inline-block'}
#         ),

#         html.Div(
#                     className="video-outer-container",
#                     children=html.Div(
#                         className="video-container",
#                         children=player.DashPlayer(
#                             id="video-display",
#                             url=f.return_relative_dir().__str__(),
#                             loop=True,
#                             playing=True,
#                             controls=True,
#                             volume=1,
#                             width="80%",
#                             height="80%",
#                         ),
#                     ),
#                 ),
#         html.Button(id='submit-button', n_clicks=0, children='Submit'),
#         html.Div(id='output-state')

# ], style={'columnCount': 2})



# Main App
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
                            id="logo-mobile", src=app.get_asset_url("logo.jpg")
                        ),
                        html.Div(
                            id="header-section",
                            children=[
                                html.H4("视频打标系统"),
                                html.P(
                                    "首先，确认工作的目录是否正确，可以通过输入修改"
                                ),
                                html.P(
                                    "打标开始，选择右边栏框内需要的标签，点击确定即可"
                                ),
                                html.P(id = "current_working_dir",
                                    children=f"{f.return_relative_dir().__str__()}"
                                ),
                                html.Button(
                                    "需要帮助", id="help-button", n_clicks=0
                                ),
                            ],
                        ),
                        html.Div(
                            className="video-outer-container",
                            children=html.Div(
                                className="video-container",
                                children=player.DashPlayer(
                                    id="video-display",
                                    url="",
                                    loop=True,
                                    controls=True,
                                    playing=True,
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
                                            children=["偏移情况:"]
                                        ),
                                        dcc.RadioItems(
                                            id = "shift",
                                            options=[
                                                {'label': '没偏移', 'value': 'MPY'},
                                                {'label': '有左偏', 'value': 'ZP'},
                                                {'label': '有右偏', 'value': 'YP'}
                                            ],
                                            value="MPY",
                                            labelStyle={'display': 'inline-block'}
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(children=["车道情况:"]),
                                    dcc.RadioItems(
                                            id = "road",
                                            options=[
                                                {'label': '直道', 'value': 'ZD'},
                                                {'label': '弯道', 'value': 'WD'},
                                                {'label': '急弯道', 'value': 'JWD'}
                                            ],
                                            value="ZD",
                                            labelStyle={'display': 'inline-block'}
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(children=["所处时间段:"]),
                                    dcc.RadioItems(
                                            id = "timing",
                                            options=[
                                                {'label': '白天', 'value': 'DAY'},
                                                {'label': '夜晚', 'value': 'NIG'},
                                                {'label': '黄昏', 'value': 'DUSk'},
                                                {'label': '夜晚', 'value': 'DAWN'}
                                            ],
                                            value="DAY",
                                            labelStyle={'display': 'inline-block'}
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(children=["天气情况:"]),
                                    dcc.RadioItems(
                                            id = "weather",
                                            options=[
                                                {'label': '晴天', 'value': 'SUN'},
                                                {'label': '雨天', 'value': 'RAIN'},
                                                {'label': '小雪', 'value': 'SNOW'},
                                                {'label': '雾天', 'value': 'FOG'},
                                                {'label': '阴天', 'value': 'CLO'}
                                            ],
                                            value="SUN",
                                            labelStyle={'display': 'inline-block'}
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
                                id="logo-web", src=app.get_asset_url("logo.jpg")
                            )
                        ),
                        html.Div(
                            className="control-element",
                            children=[
                                html.Div(children=["道路总体情况:"]),
                            dcc.RadioItems(
                                    id = "road_brief",
                                    options=[
                                        {'label': '良好', 'value': 'GOOD'},
                                        {'label': '复杂', 'value': 'BAD'}
                                    ],
                                    value="GOOD",
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ],
                        ),
                        html.Div(
                            className="control-element",
                            children=[
                                html.Div(children=["车侧:"]),
                            dcc.RadioItems(
                                    id = "side",
                                    options=[
                                        {'label': '左侧', 'value': 'L'},
                                        {'label': '右侧', 'value': 'R'}
                                    ],
                                    value="L",
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ],
                        ),
                        html.Div(
                            className="control-element",
                            children=[
                                html.Div(children=["车道:"]),
                            dcc.RadioItems(
                                    id = "road_color",
                                    options=[
                                        {'label': '白色', 'value': '0'},
                                        {'label': '黄色', 'value': '1'}
                                    ],
                                    value="0",
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ],
                        ),
                        html.Div(
                            className="control-element",
                            children=[
                                html.Div(children=["单双车道:"]),
                            dcc.RadioItems(
                                    id = "single_double",
                                    options=[
                                        {'label': '单车道', 'value': 'd'},
                                        {'label': '双车道', 'value': 's'}
                                    ],
                                    value="d",
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ],
                        ),
                        html.Div(
                            className="control-element",
                            children=[
                                html.Div(children=["车道宽窄:"]),
                            dcc.RadioItems(
                                    id = "width",
                                    options=[
                                        {'label': '宽阔', 'value': 'K'},
                                        {'label': '狭窄', 'value': 'Z'}
                                    ],
                                    value="K",
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ],
                        ),
                        html.Div(
                            className="control-element",
                            children=[
                                html.Div(children=["车道线:"]),
                            dcc.RadioItems(
                                    id = "road_line",
                                    options=[
                                        {'label': '虚线', 'value': '0'},
                                        {'label': '实线', 'value': '1'},
                                        {'label': '虚实线', 'value': '2'}
                                    ],
                                    value="0",
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ],
                        ),
                        html.Div(
                            className="control-element",
                            children=[
                                html.Div(children=["其他情况:"]),
                            dcc.RadioItems(
                                    id = "other",
                                    options=[
                                    {'label': '', 'value': ''},
                                    {'label': '白天前车', 'value': '001'},
                                    {'label': '斑马线', 'value': '002'},
                                    {'label': '侧车阴影', 'value': '003'},
                                    {'label': '车道线模糊', 'value': '004'},
                                    {'label': '导流线', 'value': '005'},
                                    {'label': '反光', 'value': '006'},
                                    {'label': '减速线', 'value': '007'},
                                    {'label': '箭头', 'value': '008'},
                                    {'label': '逆光', 'value': '009'},
                                    {'label': '晚上前车尾灯', 'value': '010'},
                                    {'label': '污迹', 'value': '011'},
                                    {'label': '阴影', 'value': '012'},
                                    {'label': '雨刮', 'value': '013'},
                                    {'label': '长排路灯', 'value': '014'},
                                    {'label': '长字体', 'value': '015'},
                                    {'label': '修补路面', 'value': '016'},
                                    {'label': '路面水渍', 'value': '017'}
                                    ],
                                    value=""
                                ),
                            ],
                        ),
                        
                        
                        html.Button(id='submit-button', n_clicks=0, children='Submit'),
                        html.Div(id='output-state'),
                        html.Div(id="div-visual-mode"),
                        html.Div(id="div-detection-mode"),
                        dcc.ConfirmDialog(
                            id='confirm',
                            message='你已完成目标目录下的打标工作！',
                        )
                    ],
                ),
            ],
        ),
        markdown_popup(),
    ]
)



# # Footage Selection
# @app.callback(
#     Output("video-display", "url"),
#     [
#         Input("dropdown-footage-selection", "value"),
#         Input("dropdown-video-display-mode", "value"),
#     ],
# )
# def select_footage(footage, display_mode):
#     # Find desired footage and update player video
#     url = url_dict[display_mode][footage]
#     return url


# need help popup
@app.callback(
    Output("markdown", "style"),
    [Input("help-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if prop_id == "help-button":
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(Output('current_working_dir', 'children'),
              [Input('submit-button', 'n_clicks')])
def print_output(n_clicks):
    return f.files.__str__()



@app.callback(Output('video-display', 'url'),
              [Input('submit-button', 'n_clicks')])
def update_output(n_clicks):
    _ = f.pop_update()
    return f.return_relative_dir().__str__()



@app.callback(Output('confirm', 'displayed'),
              [Input('current_working_dir', 'children')])
def update_outputx(str_):
    if str_ == 'set()':
        return True
    return False

# @app.callback(Output('video-display', 'url'),
#               [Input('submit-button', 'n_clicks')])
# def print_output(n_clicks):
#     _ = f.pop_update()
#     return f.return_relative_dir().__str__()






server = app.server
@server.route('/data/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'data'), path)





# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8053)
