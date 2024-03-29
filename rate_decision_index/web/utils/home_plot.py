import pandas as pd
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px
import json
from web.utils.utils import load_market_data, load_fff_data

#### gmond update this function
def plot_gauge(gauge_final_data, fff_prob_data, date):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = (gauge_final_data.iloc[(gauge_final_data.loc[gauge_final_data.Date == date].index).tolist()[0]]["Federal Funds Rate"]).round(4),
        domain = {'row': 0, 'column': 0},
        title = {'text': "Rate Hike-Cut", 'font': {'size': 30}},
        delta = {'reference': (gauge_final_data.iloc[(gauge_final_data.loc[gauge_final_data.Date == date].index-1).tolist()[0]]["Federal Funds Rate"]), 'increasing': {'color': "mediumseagreen"}},
        gauge = {
            'axis': {'range': [None, 6], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#401664"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0.0, 0.60], 'color': 'forestgreen'},
                {'range': [0.60, 1.2], 'color': 'limegreen'},
                {'range': [1.2, 1.8], 'color': 'lightgreen'},
                {'range': [1.8, 2.4], 'color': 'palegreen'},
                {'range': [2.4, 3.0], 'color': 'floralwhite'},
                {'range': [3.0, 3.6], 'color': 'rosybrown'},
                {'range': [3.6, 4.2], 'color': 'lightcoral'},
                {'range': [4.2, 4.8], 'color': 'indianred'},
                {'range': [4.8, 5.4], 'color': 'firebrick'},
                {'range': [5.4, 6.0], 'color': 'maroon'}],
            'threshold': {
                'line': {'color': "#401664", 'width': 4},
                'thickness': 0.75,
                'value': (gauge_final_data.iloc[(gauge_final_data.loc[gauge_final_data.Date == date].index).tolist()[0]]["Federal Funds Rate"]).round(4)}}))
        
    # fff probability
    fig.add_trace(go.Indicator(
        mode = "number",
        number = {'suffix': "%", "font":{"size":80}},
        value = (((fff_prob_data.iloc[(fff_prob_data.loc[fff_prob_data.Date == "2021-11"].index).tolist()[0]].Hike)*100).round(2)),
        title = {'text':"Probability of Rate Hike for Novemeber 2021", 
                 'font.size': 20, 
                 'font.color': '#401664', 
                 'font.family':'Times New Roman Bold'},
        domain = {'row': 0, 'column': 1}))

    fig.update_layout(
        grid = {'rows': 1, 'columns': 2, 'pattern': "independent"},
        paper_bgcolor = "white", 
        font_family="Times New Roman Bold",
        font_color="black",
        title={
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font.size':15},
        margin=dict(l=200, r=150, t=75, b=20))
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return plot_json
     
def plot_market(market_data, date):
    df_senti = market_data
    fig = go.Figure()
    #Statement
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = (df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Score_Statement).round(4),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference': (df_senti.iloc[(df_senti.loc[df_senti.Date == date].index-1).tolist()[0]].Score_Statement).round(4), "font":{"size":20}},
        title = {'text':"FOMC STATEMENT SENTIMENTS SCORE"+'<br>'+ '='*len("FOMC Statement Sentiments Score"), 
                 'font.size': 15, 
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 1, 'column': 0}))
    
    fig.add_trace(go.Indicator(
        title = {'text': "<"+df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Statement_Sentiments+">", 
                 'font.size': 17,
                 'font.family': 'Courier New', 
                 'font.color': '#401664',
                 'align': 'right'},
        mode = 'delta',
        delta = {'reference': 0, 'font.size': 1},
        domain = {'row': 1, 'column': 1}))

    #Minutes
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = (df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Score_Minutes).round(4),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference': (df_senti.iloc[(df_senti.loc[df_senti.Date == date].index-1).tolist()[0]].Score_Minutes).round(4), "font":{"size":20}},
        title = {'text':"FOMC MINUTES SENTIMENTS SCORE"+'<br>'+ '='*len("FOMC Minutes Sentiments Score"),
                 'font.size': 15, 
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 3, 'column': 0}))
    
    fig.add_trace(go.Indicator(
        title = {'text': "<"+df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Minutes_Sentiments+">", 
                 'font.size': 17,
                 'font.color': '#401664',
                 'font.family': 'Courier New', 
                 'align': 'right'},
        mode = 'delta',
        delta = {'reference': 0, 'font.size': 1},
        domain = {'row': 3, 'column': 1}))

    #News
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = (df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Score_News).round(4),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference': (df_senti.iloc[(df_senti.loc[df_senti.Date == date].index-1).tolist()[0]].Score_News).round(4), "font":{"size":20}},
        title = {'text':"NEWS SENTIMENTS SCORE"+'<br>'+ '='*len("News Sentiments Score"), 
                 'font.size': 15, 
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 5, 'column': 0}))
    
    fig.add_trace(go.Indicator(
        title = {'text': "<"+df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].News_Sentiments+">", 
                 'font.size': 17,
                 'font.color': '#401664',
                 'font.family': 'Courier New',
                 'align': 'right'},
        mode = 'delta',
        delta = {'reference': 0, 'font.size': 1},
        domain = {'row': 5, 'column': 1}))

    
    fig.update_layout(
        grid = {'rows': 6, 'columns': 2, 'pattern': "independent"},
        paper_bgcolor = "white", 
        font_family="Times New Roman Bold",
        font_color="black",
        title={
            'text': "Breakdown of Sentiment Scores for " + pd.to_datetime(date).strftime("%B %Y"),
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font.size':20},
        margin=dict(l=150, r=100, t=75, b=20),
        autosize=True)
    fig.update_xaxes(automargin=True)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return plot_json

def get_average_sentiment(market_data, date):
    df_senti = market_data
    state_num = df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Score_Statement
    min_num = df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Score_Minutes
    news_num = df_senti.iloc[(df_senti.loc[df_senti.Date == date].index).tolist()[0]].Score_News
    
    return ((state_num+min_num+news_num) / 3)
    
def plot_market_average(market_data, date):
    avg = get_average_sentiment(market_data, date).round(4)

    word = ""
    if avg > 0:
        word = "Overall Hawkish"
    elif avg < 0:
        word = "Overall Dovish"
    elif avg == 0:
        word = "Overall Neutral"
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        title={
            'text': "Average Sentiment Score for " + pd.to_datetime(date).strftime("%B %Y"), 'font.size': 20},
        mode = "delta",
        delta = {'reference': 0, 'font.size': 1},
        domain = {'row': 0, 'column': 0}))
    
    fig.add_trace(go.Indicator(
        mode = "number",
        number={"font":{"size":80}},
        value = avg,
        domain = {'row': 1, 'column': 0}))
    
    fig.add_trace(go.Indicator(
        title = {'text': "<"+word+">", 
                 'font.size': 20,
                 'font.family': 'Courier New Bold',
                 'font.color':'#401664',            
                 'align': 'center'},
        mode = 'delta',
        delta = {'reference': 0, 'font.size': 1},
        domain = {'row': 2, 'column': 0}))
    
    
    fig.update_layout(
        grid = {'rows': 3, 'columns': 1, 'pattern': "independent"},
        paper_bgcolor = "white", 
        font_family="Times New Roman Bold",
        font_color="black",
       
        margin=dict(l=8, r=8, t=25, b=5),
        autosize=True
        )

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
       
def plot_fff(fff_data):
    df_fff =fff_data
    #transform df
    new_df_fff = df_fff.melt(id_vars=["Date"],
                             var_name="Basis Points",
                             value_name="Probability")
    fig = px.bar(new_df_fff, x='Basis Points', y='Probability', animation_frame='Date', 
             color_discrete_sequence =['#401664']*len(new_df_fff))
    
    fig.update_layout(
        font_family="Courier New",
        font_color="black",
        title_font_family="Times New Roman Bold",
        title_font_color="black",
        title_text='Probability of Change in Target Rates by Basis Points', 
        title_x=0.5, 
        title_font_size = 20,
        
        xaxis_title="",
        yaxis_title="Probability of Change", 
        plot_bgcolor = 'white',
        autosize=True
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ECECEC', zeroline=True, zerolinecolor='lightgrey')
    fig.update_yaxes(range=[-0.1, 1.1],showgrid=True, gridwidth=1, gridcolor='#ECECEC', zeroline=True, zerolinecolor='lightgrey')
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

def plot_macro_maindashboard(df_plot, date):
    ## Setting up values
    # T10Y3M
    B_T10Y3M = 0.043143
    X_T10Y3M = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].T10Y3M #change to actual date to date
    value_T10Y3M = B_T10Y3M * X_T10Y3M

    X_T10Y3M_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].T10Y3M
    value_T10Y3M_prev = B_T10Y3M * X_T10Y3M_prev
    
    # EMRATIO
    B_EMRATIO = 0.033783
    B_EMRATIO_MEDWAGES = 0.006322
    X_EMRATIO = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].EMRATIO #change to actual date to date
    X_EMRATIO_MEDWAGES = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].EMRATIO_MEDWAGES #change to actual date to date
    X_MEDWAGES = X_EMRATIO_MEDWAGES / X_EMRATIO
    value_EMRATIO = (B_EMRATIO + (B_EMRATIO_MEDWAGES*X_MEDWAGES)) * X_EMRATIO

    X_EMRATIO_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].EMRATIO
    X_EMRATIO_MEDWAGES_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].EMRATIO_MEDWAGES #change to actual date to date
    X_MEDWAGES_prev = X_EMRATIO_MEDWAGES_prev / X_EMRATIO_prev
    value_EMRATIO_prev = (B_EMRATIO + (B_EMRATIO_MEDWAGES*X_MEDWAGES_prev)) * X_EMRATIO_prev

    # GDP
    B_GDPC1 = 0.036187
    X_GDPC1 = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].GDPC1 #change to actual date to date
    value_GDPC1 = B_GDPC1 * X_GDPC1
    
    X_GDPC1_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].GDPC1 #change to actual date to date
    value_GDPC1_prev = B_GDPC1 * X_GDPC1_prev
    
    # MEDCPI
    B_MEDCPI = 0.063183
    B_MEDCPI_PPIACO = -0.077871
    X_MEDCPI = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].MEDCPI #change to actual date to date
    X_MEDCPI_PPIACO = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].MEDCPI_PPIACO #change to actual date to date
    X_PPIACO = X_MEDCPI_PPIACO / X_MEDCPI
    value_MEDCPI = (B_MEDCPI + (B_MEDCPI_PPIACO*X_PPIACO)) * X_MEDCPI

    X_MEDCPI_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].MEDCPI #change to actual date to date
    X_MEDCPI_PPIACO_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].MEDCPI_PPIACO #change to actual date to date
    X_PPIACO_prev = X_MEDCPI_PPIACO_prev / X_MEDCPI_prev
    value_MEDCPI_prev = (B_MEDCPI + (B_MEDCPI_PPIACO*X_PPIACO_prev)) * X_MEDCPI_prev
    
    # HD index
    B_HD_index = 0.051086
    X_HD_index = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].HD_index #change to actual date to date
    value_HD_index = B_HD_index * X_HD_index
    
    X_HD_index_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].HD_index #change to actual date to date
    value_HD_index_prev = B_HD_index * X_HD_index_prev
    
    # shifted_target
    B_shifted_target = 1.7117595779058272
    X_shifted_target = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].shifted_target #change to actual date to date
    value_shifted_target = B_shifted_target * X_shifted_target
    
    X_shifted_target_prev = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index-1).tolist()[0]].shifted_target #change to actual date to date
    value_shifted_target_prev = B_shifted_target * X_shifted_target_prev
    
    ## Plotting figures
    fig = go.Figure()

    # T10Y3M Indicator
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = abs(value_T10Y3M.round(4)),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference':abs(value_T10Y3M_prev.round(4)), "font":{"size":20}},
        title = {'text':"BOND YIELD SPREAD"+'<br>'+ '='*len("Bond Yield Spread"), 
                 'font.size': 15, 
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 0, 'column': 0}))

    # EMRATIO Indicator
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = abs(value_EMRATIO.round(4)),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference':abs(value_EMRATIO_prev.round(4)), "font":{"size":20}},
        title = {'text':"EMPLOYMENT"+'<br>'+ '='*len("Employment"), 
                 'font.size': 15,
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 0, 'column': 1}))

    # GDP Indicator
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = abs(value_GDPC1.round(4)),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference':abs(value_GDPC1_prev.round(4)), "font":{"size":20}},
        title = {'text':"DOMESTIC OUTPUT"+'<br>'+ '='*len("Domestic Output"), 
                 'font.size': 15,
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 1, 'column': 0}))

    # MEDCPI Indicator
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = abs(value_MEDCPI.round(4)),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference':abs(value_MEDCPI_prev.round(4)), "font":{"size":20}},
        title = {'text':"INFLATION"+'<br>'+ '='*len("Inflation"), 
                 'font.size': 15,
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 1, 'column': 1}))

    # HD index Indicator
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = abs(value_HD_index.round(4)),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference':abs(value_HD_index_prev.round(4)), "font":{"size":20}},
        title = {'text':"HAWKISH-DOVISH INDEX"+'<br>'+ '='*len("Hawisk-Dovish Index"), 
                 'font.size': 15,
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 2, 'column': 0}))

    # shifted target Indicator
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = abs(value_shifted_target.round(4)),
        number={"font":{"size":40}},
        delta = {'position': "right", 'reference':abs(value_shifted_target_prev.round(4)), "font":{"size":20}},
        title = {'text':"PREVIOUS MONTH RATE"+'<br>'+ '='*len("Previous Month Rate"), 
                 'font.size': 15,
                 'font.color': '#401664', 
                 'font.family':'Courier New'},
        domain = {'row': 2, 'column': 1}))

    # Configure layout
    fig.update_layout(
        grid = {'rows': 3, 'columns': 2, 'pattern': "independent"},
        paper_bgcolor = "white", 
        font_family="Times New Roman Bold",
        font_color="black",
        title={
            'text': "Contribution of Indicators for " + pd.to_datetime(date).strftime("%B %Y"),
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font.size': 20},
        margin=dict(l=50, r=50, t=100, b=15),
        autosize=True)
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

def plot_contributions_pie(df_plot, date):
    ## Setting up values
    # T10Y3M
    B_T10Y3M = 0.043143
    X_T10Y3M = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].T10Y3M #change to actual date to date
    value_T10Y3M = B_T10Y3M * X_T10Y3M

    # EMRATIO
    B_EMRATIO = 0.033783
    B_EMRATIO_MEDWAGES = 0.006322
    X_EMRATIO = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].EMRATIO #change to actual date to date
    X_EMRATIO_MEDWAGES = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].EMRATIO_MEDWAGES #change to actual date to date
    X_MEDWAGES = X_EMRATIO_MEDWAGES / X_EMRATIO
    value_EMRATIO = (B_EMRATIO + (B_EMRATIO_MEDWAGES*X_MEDWAGES)) * X_EMRATIO

    # GDP
    B_GDPC1 = 0.036187
    X_GDPC1 = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].GDPC1 #change to actual date to date
    value_GDPC1 = B_GDPC1 * X_GDPC1

    # MEDCPI
    B_MEDCPI = 0.063183
    B_MEDCPI_PPIACO = -0.077871
    X_MEDCPI = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].MEDCPI #change to actual date to date
    X_MEDCPI_PPIACO = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].MEDCPI_PPIACO #change to actual date to date
    X_PPIACO = X_MEDCPI_PPIACO / X_MEDCPI
    value_MEDCPI = (B_MEDCPI + (B_MEDCPI_PPIACO*X_PPIACO)) * X_MEDCPI

    # HD index
    B_HD_index = 0.051086
    X_HD_index = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].HD_index #change to actual date to date
    value_HD_index = B_HD_index * X_HD_index

    # shifted_target
    B_shifted_target = 1.7117595779058272
    X_shifted_target = df_plot.iloc[(df_plot.loc[df_plot.Date == date].index).tolist()[0]].shifted_target #change to actual date to date
    value_shifted_target = B_shifted_target * X_shifted_target

    labels = ['Bond Yield Spread', 'Employment', 'Domestic Output', 'Inflation', 'Hawisk-Dovish Index', 'Previous Month Rate']
    values = [abs(value_T10Y3M), abs(value_EMRATIO), abs(value_GDPC1), abs(value_MEDCPI), abs(value_HD_index), abs(value_shifted_target)]
    colors = ['#401664', '#D71C2B', '#EE2033', '#F78E99', '#FBC9CF', 'lavender']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, 
                                 textfont = {'family':'Courier New', 'color':'black'},
                                 textfont_size=13,
                                 showlegend=True, 
                                 marker = dict(colors=colors,line=dict(color='#000000', width=0.4)))])
    fig.update_traces(textposition='outside', textinfo='percent')
    fig.update_layout(
        paper_bgcolor = "white",
        font_color="black",
        title={
            'text': "Indicators Contributions for " + pd.to_datetime(date).strftime("%B %Y"),
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font.size':20,
            'font.family': 'Times New Roman Bold'},
        margin=dict(l=100, r=100, t=100, b=100),)

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

def plot_fed_rates_ts(data):
    df_plot=data
    plot = go.Figure(data=[go.Scatter(
        name='Actual Rate',
        x=df_plot.Date.tolist(),
        y=df_plot.Actual_Rate.tolist(),
        marker_color='#D71C2B' #change color of line
    ),
        go.Scatter(
        name='Predicted Rate',
        x=df_plot.Date.tolist(),
        y=df_plot.Predicted_Rate.tolist(),
        marker_color='#401664' #change color of line
    )
    ])

    plot.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True]},
                               {"title": "Time Series of Both Actual and Predicted Federal Funds Rates"}]),
                    dict(label="Actual",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Time Series of Actual Federal Funds Rates",
                                }]),
                    dict(label="Predicted",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Time Series of Predicted Federal Funds Rates",
                                }]),
                ]),
            )
        ])

    plot.update_layout(
        font_family="Courier New",
        font_color="black",
        title_font_family="Times New Roman Bold",
        title_font_color="black",
        title_text='Time Series of Both Actual and Predicted Federal Funds Rates', 
        title_x=0.5,
        title_font_size = 20,
        plot_bgcolor = 'white', autosize=True
    )

    plot.update_xaxes(rangeslider_visible=True, showgrid=True, gridwidth=1, gridcolor='#ECECEC', zeroline=True, zerolinecolor='lightgrey')
    plot.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ECECEC', zeroline=True, zerolinecolor='lightgrey')
    plot.update_xaxes(rangeslider_visible=True)

    plot_json = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json