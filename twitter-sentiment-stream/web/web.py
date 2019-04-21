import datetime
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
import sys
import pickle
import threading
import util
from plotly import tools


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([

        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
        ),
        html.Div(id='live-update-text'),
        dcc.Graph(id = 'pie-graph')
    ])

)

# initial Datastructure
time_cnt = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
throughput = []
global data


@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):

    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.1, subplot_titles=('Sentiment Monitor for Players', 'Throughput Monitor'))
    fig['layout']['margin'] = {
            'l': 30, 'r': 10, 'b': 30, 't': 50
    }
    fig['layout'].update(height=800, width=1400)

    ####################################################
    # Receive Data
    data =  util.getData();
    sentiment = data['count']
    num = data['throughput']

    # Convert to list
    name =[]
    positive = []
    negative = []
    for i in sentiment.keys():
        name.append(i)
        positive.append(sentiment[i][0])
        negative.append(sentiment[i][1])

    time_cnt.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    throughput.append(num)

    # Time Window for throughput
    if(len(time_cnt) > 30):
        time_cnt.pop(0)
        throughput.pop(0)

    ###################################################
    #Bar Chart
    trace0 = go.Bar(
        x = name,
        y = positive,
        name='Positive',
        marker=dict(
            color='rgb(0, 102, 255)'
        )
    )

    trace1 = go.Bar(
        x = name,
        y = negative,
        name='Negative',
        marker=dict(
            color='rgb(255, 230, 0)',
        )
    )

    fig.append_trace(trace0,1,1)
    fig.append_trace(trace1,1,1)
    fig['layout']['barmode'] = 'group'

    ##################################################################
    # ThroughPut
    fig.append_trace({
        'x': time_cnt,
        'y': throughput,

        'name': 'Throughput',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig

#####################################################################
# Update text
@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    data = util.getData()
    twitter_before = data['original']
    twitter_after = data['text']
    session = data['session']
    #print(twitter_before)
    timenow = [util.convertime(i[0]) for i in session]
    his = [i[1] for i in session]
    sessionnow = dict(zip(timenow, his))

    # print(timenow)
    # print(his)
    style = {'padding': '5px', 'fontSize': '25px'}
    result = []
    result.append(html.Span('Before PreProcess: ' + twitter_before, style=style))
    result.append(html.Div())
    result.append(html.Span('After PreProcess: ' + twitter_after, style=style))
    result.append(html.Div())
    for key, value in sessionnow.items():
        result.append(html.Span('History Session : ' + str(key) + str(value), style = style))
        result.append(html.Div())


    return result

#####################################################################
@app.callback(Output('pie-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):

    data = util.getData()
    # most recent session
    session = data['session'][-1]

    time = session[0]
    count = session[1]

    num = len(count.keys())

    sentiment_number = []
    for i in count.keys():
        sentiment_number.append((count[i][0], count[i][1]))


    labels = ['Positive','Negative']

    # generate singel pie format
    piedata = []
    for i in range(num):
        onepie = util.PieOneData([sentiment_number[i][0], sentiment_number[i][1]], labels, i)
        piedata.append(onepie)

    # generate annotations
    annotations = []
    # position:


    if num == 1:
        position = [0.5]
    elif num == 2:
        position = [0.2, 0.8]
    elif num == 3:
        position = [0.15, 0.5, 0.85]
    elif num == 4:
        position = [0.11, 0.375, 0.625, 0.89]

    tmp = 0
    names = []
    for i in count.keys():
        annotations.append(util.subtitle(i,position[tmp]))
        names.append(i)
        tmp +=1

    title = " -- ".join(names)

    #print(piedata)
    #print(annotations)
    layout = util.layout(annotations, num, title)


    fig = util.PieAllData(piedata,layout)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
