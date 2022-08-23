#!/usr/bin/env python
# coding: utf-8
# %%

# ## Hotel Modelling Dashboard

# %%


# !pip install plotly


# %%


# !pip install dash


# %%


import numpy as np
import pandas as pd 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import plotly.express as px

#Import datasets 
df_details = pd.read_csv('dfclean_1adult.csv')
df_details = df_details.rename(columns = {'Unnamed: 0':'Name',
                                         'reviews': 'no. of reviews'})

df_dates = pd.read_csv('final_df.csv').drop('Unnamed: 0', 1)

# Merge datasets
df = df_details.merge(df_dates,  on='Name')
df = df.replace(to_replace = ['Y','N'],value = [1,0])

df.iloc[:,7:37] = df.iloc[:,7:37].apply(lambda x: x.astype(str))
df.iloc[:,7:37] = df.iloc[:,7:37].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)

user_df = df.copy()
date_cols = user_df.columns[7:37]
hotel_types = user_df['Property Type'].unique()
features = ['Price'] + list(user_df.columns[2:5]) + list(user_df.columns[37:])
continuous_features = features[:9]
continuous_features_A = ['Price', 'Distance to Mall', 'Distance to MRT']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Hotel Booking'

def generate_table(dataframe, max_rows=5):
    df_drop_link = dataframe.drop(columns='link')
    
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df_drop_link.columns]) 
        ),
        html.Tbody([
            html.Tr([
            html.Td(dataframe.iloc[i][col]) if col != 'Name' else html.Td(html.A(href=dataframe.iloc[i]['link'], children=dataframe.iloc[i][col], target='_blank')) for col in df_drop_link.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

colors = {'background': '#111111', 'text': '#7FDBFF'}

app.layout = html.Div([
    
    #introduction
    html.Div([
    html.H2(children='Hello!',
            style={'color': colors['text']}),
    
    #inputs for date and hotel type    
    html.Div([html.H4("Step 1: Input Date (eg. 4Nov): "),
              dcc.Input(id='date-input', value='4Nov', type='text')],
            style={'width':'30%', 'float':'left'}),
    
    html.Div(id='date-output-hotel'),
    
    html.Div([ 
    html.H4('Step 2: Select Your Preferred Hotel Types:'),
    dcc.Dropdown(id='hotel-input',
                options=[{'label': i, 'value': i} for i in hotel_types],
                value= hotel_types,
                multi=True)],
    style={'width':'70%', 'float':'right'}),
    html.Br(), html.Br()
    ]),
    
    #return available hotels for given date
    html.Div([
    html.Br(), html.Br(), html.Hr(),
    dcc.Graph(id='output-submit'),
    html.Hr(),
    ]),
    
    #input top 3 features
    html.Div([
    html.H4(children='Step 3: Select Your Top 3 Features:'),
    ]),
    
    html.Div([
    dcc.Dropdown(
        id='feature1',
        options=[{'label': i, 'value': i} for i in features],
                value= features[0]
    ), html.Br(), 
    dcc.Slider(id='weight1',
        min= 10, max= 90, step= 10,
        marks={i: '{}%'.format(i) for i in np.arange(10, 90, 10).tolist()},
        value=50)
    ], style={"display": "grid", "grid-template-columns": "20% 10% 70%", "grid-template-rows": "50px"}
    ),
    
    html.Div([
    dcc.Dropdown(
        id='feature2',
        options=[{'label': i, 'value': i} for i in features],
                value= features[1]
    ), html.Br(),
    dcc.Slider(id='weight2',
        min= 10, max= 90, step= 10,
        marks={i: '{}%'.format(i) for i in np.arange(10, 90, 10).tolist()},
        value=30)
    ], style={"display": "grid", "grid-template-columns": "20% 10% 70%", "grid-template-rows": "50px"}
    ),
    
    html.Div([
    dcc.Dropdown(
        id='feature3',
        options=[{'label': i, 'value': i} for i in features],
                value= features[2]
    ), html.Br(),
    dcc.Slider(id='weight3',
        min= 10, max= 90, step= 10,
        marks={i: '{}%'.format(i) for i in np.arange(10, 90, 10).tolist()},
        value=20)
    ], style={"display": "grid", "grid-template-columns": "20% 10% 70%", "grid-template-rows": "50px"}
    ),
    
    #return top 5 hotels recommended
    html.Div([ 
    html.Hr(),
    html.H2(children='Top 5 Hotels Recommended For You',
            style={'color': colors['text']}),
    html.Div(id='output-feature'),
    html.Hr()
    ])
])

#update available hotels for given date
@app.callback(Output('output-submit', 'figure'),
                [Input('hotel-input', 'value'), Input('date-input', 'value')])
def update_hotels(hotel_input, date_input):
    user_df = df.copy()
    user_df = user_df[user_df[date_input].notnull()]
    user_df = user_df[user_df['Property Type'].isin(hotel_input)]
    plot_df = pd.DataFrame(user_df.groupby('Property Type')['Name'].count()).reset_index()
    fig = px.bar(plot_df, x='Property Type', y='Name', color="Property Type", title="Hotel Types available on {}:".format(date_input))
    fig.update_layout(transition_duration=500)
    return fig

#update top 5 hotels recommended
@app.callback(Output('output-feature', 'children'),
                [Input('hotel-input', 'value'), Input('date-input', 'value'), 
                 Input('feature1', 'value'),  Input('feature2', 'value'), Input('feature3', 'value'),
                 Input('weight1', 'value'), Input('weight2', 'value'), Input('weight3', 'value')])
def update_features(hotel_input, date_input, feature1, feature2, feature3, weight1, weight2, weight3):
    user_df = df.copy()
    user_df = user_df[user_df[date_input].notnull()]
    user_df['Price'] = user_df[date_input]
    user_df = user_df[user_df['Property Type'].isin(hotel_input)]
    features= [feature1, feature2, feature3]
    selected_features = features.copy()
    selected_continuous = set(selected_features) & set(continuous_features)

    for i in selected_continuous:
        col = i + str(' rank')

        if i in continuous_features_A:
            user_df[col] = user_df[i].rank(ascending=False) #higher value, lower score
        else:
            user_df[col] = user_df[i].rank(ascending=True) #higher value, higher score

        selected_features[selected_features.index(i)] = col #replace element in list name with new col name

    #Scoring: weight * feature's score
    user_df['Score'] = (((weight1/100) * user_df[selected_features[0]]) 
                      + ((weight2/100) * user_df[selected_features[1]]) 
                      + ((weight3/100) * user_df[selected_features[2]])).round(1)
    
    #Score-to-Price ratio
    user_df['Value_to_Price ratio'] = (user_df['Score'] / user_df['Price']).round(1)
    user_df = user_df.sort_values(by=['Value_to_Price ratio'], ascending = False).reset_index()
    features_result = [i for i in features if i != 'Price']
    selected_features_result = [i for i in selected_features if i not in features_result]
    user_df_results = user_df[['Name', 'Property Type', 'Price', 'Score', 'Value_to_Price ratio'] + ['link'] + features_result + selected_features_result] 

    return generate_table(user_df_results.head(5))

port = 8050
url = "http://127.0.0.1:{}".format(port)
def open_browser():
    webbrowser.open_new(url)

if __name__ == '__main__':
    Timer(0.5, open_browser).start();
    app.run_server( debug= False, port=port)


# %%




