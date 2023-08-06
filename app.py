#!/usr/bin/env python
# coding: utf-8

# In[6]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import mysql.connector
from pymongo import MongoClient
import dash_table
import plotly.graph_objs as go
from neo4j import GraphDatabase
from mysql_utils import * 
from mongodb_utils import * 
from neo4j_utils import * 


# In[7]:


mysql_universities = return_uni_names().squeeze().tolist()
mongo_words = return_keywords()
neo4j_universities = return_universities()


# In[8]:


app = dash.Dash(__name__)


# In[9]:


app.layout = html.Div([
    # First Row
    html.Div([
        html.Div([
            html.H1("A High Schooler's Guide to Choosing a College"), 
            html.H3("Research Interests by University"),
    dcc.Dropdown(
        id="university-dropdown",
        options=[{'label': university, 'value': university} for university in mysql_universities],
        value="College of William Mary",
        placeholder="Select a university"
    ),
    dcc.Graph(id="bar-graph"), 
        ], className='four columns'),
        
        
        html.Div([
            html.H3("Publications Filtered by Research Interest"),
                dcc.Dropdown(
        id="keyword-dropdown2",
        options=[{'label': keyword, 'value': keyword} for keyword in mongo_words],
        value="frame rate",
        placeholder="Select a keyword"
    ),
    html.Div(id='table-container'),
        ], className='four columns'),
       
        
        html.Div([
            html.H3("Keyword Frequency By University"),
            dcc.Graph(id='pie-chart'),
        ], className='four columns'),
    ], className='row'),

    # Second Row
    html.Div([
        html.Div([
            html.H3("KRC Score for Keyword by University"),
                dcc.Dropdown(
        id="keyword-dropdown",
        options=[{'label': keyword, 'value': keyword} for keyword in mongo_words],
        value="frame rate",
        placeholder="Select a keyword"
    ),
    html.Div(id="search-results"), 
    
    dcc.Graph(id = "bar-graph2"),
        ], className='four columns'),
        
        
        html.Div([
            html.H3("Number of Publications Over the Years"),
                dcc.Dropdown(
        id="university2-dropdown",
        options=[{'label': keyword, 'value': keyword} for keyword in neo4j_universities],
        value="College of William Mary",
        placeholder="Select a university"
    ),
    dcc.Graph(id='line-plot'),
        ], className='four columns'),
        
        
        html.Div([
            html.H3("University Characteristics"),
                dcc.Dropdown(
        id="university3-dropdown",
        options=[{'label': college, 'value': college} for college in mysql_universities],
        value="College of William Mary",
        placeholder="Select a university"
    ),
    html.Div(id='table-container2'),
        ], className='four columns'),
    ], className='row'),
])

@app.callback(
    Output("bar-graph", "figure"),
    [Input("university-dropdown", "value")]
)
def widget1(selected_university):
    df = widget1_helper(selected_university)
    
    fig = {
    'data': [
        {'x': df['words'], 'y': df['counts'], 'type': 'bar', 'name': 'University Data'}
    ],
    'layout': {
        'title': f'{selected_university}',
        'xaxis': {'title': 'words'},
        'yaxis': {'title': 'counts'}
    }
    }

    return fig


 
@app.callback(
    Output('table-container', 'children'),
    Input('keyword-dropdown2', 'value')
)
def widget2(input_words):
    df = widget2_helper(input_words)
    return dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'}
    )


@app.callback(
    Output('pie-chart', 'figure'),
    Input('keyword-dropdown2', 'value')
)
def widget3(input_words):
    df = widget3_helper(input_words)
    
    data = [go.Pie(labels=df.university,
                   values=df.num_of_mentions)]
    layout = go.Layout(title='')
    return {'data': data, 'layout': layout}




@app.callback(
    Output("bar-graph2", "figure"),
    [Input("keyword-dropdown", "value")]
)
def widget4(selected_keyword='Deep Learning'):
    universities, scores = widget4_helper(selected_keyword)


    fig = {
    'data': [
        {'x': universities, 'y': scores, 'type': 'bar', 'name': 'University Keywords'}
    ],
    'layout': {
        'title': f'{selected_keyword}',
        'xaxis': {'title': 'University'},
        'yaxis': {'title': 'Score'}
    }
}

    return fig



@app.callback(
    Output('line-plot', 'figure'),
    Input("university2-dropdown", 'value'),
)
def widget5(college):
    if college: 
        df = widget5_helper(college)
        df = df.loc[(df.year >= 2000) & (df.year <= 2020)]

        trace = go.Scatter(x=df['year'], y=df['count_of_publications'], mode='lines+markers')
        layout = go.Layout(title=f'{college}', xaxis=dict(title='Date'), yaxis=dict(title='Value'))
        return {'data': [trace], 'layout': layout}
    

@app.callback(
    Output('table-container2', 'children'),
    Input('university3-dropdown', 'value')
)
def widget6(college):
    upload_final_table(college) 
    query = "SELECT * FROM university_table"
    df = widget6_helper(query)
    return dash_table.DataTable(
        id='table2',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'}
    )


# In[10]:


if __name__ == "__main__":
    app.run_server(debug=True,port=8053)


# In[ ]:




