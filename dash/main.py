'''p'''
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from dash import Output, Input


import numpy as np
import pandas as pd

import os
print(os.listdir("data/"))


df = pd.read_csv('data/bank.csv')
app = dash.Dash()


cat_columns = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month']
num_columns = ['balance', 'day','duration', 'campaign', 'previous']


def plot_marriage_pie_chart():
    _graph = px.pie(df.marital.value_counts().reset_index().rename(columns={'index':'Marital-Status','marital':'Count'}),names='Marital-Status',values='Count',hole=0.5,template='plotly_white',color_discrete_sequence=['HotPink','LightSeaGreen','SlateBlue'])
    _graph.update_layout(title_x=0.5, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return _graph


def plot_default_pie_chart():
    _graph = px.pie(df.default.value_counts().reset_index().rename(columns={'index':'Default','default':'Count'}),names='Default', values='Count',hole=0.5,template='plotly_white',color_discrete_sequence=['HotPink','LightSeaGreen','SlateBlue'], title='Credit in Default')
    _graph.update_layout(title_x=0.5, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return _graph


def plot_housing_pie_chart():
    _graph = px.pie(df.housing.value_counts().reset_index().rename(columns={'index':'Housing','housing':'Count'}),names='Housing', values='Count',hole=0.5, template='plotly_white',color_discrete_sequence=['HotPink','LightSeaGreen','SlateBlue'], title='Housing Loan')
    _graph.update_layout(title_x=0.5, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return _graph


def plot_personal_loan():
    _graph = px.pie(df.loan.value_counts().reset_index().rename(columns={'index':'Loan','loan':'Count'}), names='Loan', values='Count',hole=0.5,template='plotly_white',color_discrete_sequence=['HotPink','LightSeaGreen','SlateBlue'], title='Personal Loan')
    _graph.update_layout(title_x=0.5, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return _graph


def plot_method_of_contact():
    _graph = px.pie(df.contact.value_counts().reset_index().rename(columns={'index':'Contact','contact':'Count'}),names='Contact',values='Count',hole=0.5,template='simple_white', title='Method of contact')
    _graph.update_traces(marker=dict(line=dict(color='#000000', width=1.4)))
    _graph.update_layout(title_x=0.5, showlegend=True, legend_title_text='<b>Contact')
    _graph.update_traces(textposition='outside', textinfo='percent+label')
    _graph.update_layout(title_x=0.5, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return _graph


def plot_last_contact():
    _graph = px.bar(df.month.value_counts().reset_index().rename(columns={'index': 'Month', 'month': 'Count'}), x='Month',
                 y='Count', color='Month', text='Count', template='simple_white')
    _graph.update_traces(marker=dict(line=dict(color='#000000', width=1.2)))
    _graph.update_layout(title_x=0.5, title_text='<b>Last Contact Month of the year', font_family="Times New Roman",
                      title_font_family="Times New Roman")
    return _graph


def plot_avg_balance_based_on_job():
    a = df.groupby(['job'], as_index=False)['balance'].mean()
    a['balance'] = round(a['balance'], 1)
    _graph = px.bar(a.sort_values(by='balance', ascending=False), x='job', y='balance', text='balance', color='job',
                 template='ggplot2')
    _graph.update_traces(marker=dict(line=dict(color='#000000', width=1.2)))
    _graph.update_layout(title_x=0.5, title_text='<b>Average balance of the clients by their job type',
                      legend_title_text='Job Type', font_family="Times New Roman", title_font_family="Times New Roman")
    return _graph


def plot_dist_age_based_on_job():
    _graph = px.box(df, x='job', y='age', color='job', template='simple_white',
                 title='<b>Distribution of age based on job type')
    _graph.update_layout(title_x=0.5, font_family="Times New Roman", legend_title_text="<b>Job type")
    return _graph


def plot_line_age_loan():
    _graph = px.line(df.groupby(['age', 'loan'], as_index=False)['job'].count().rename(columns={'job': 'Count'}), x='age',
                  y='Count', color='loan', template='simple_white', color_discrete_sequence=['DarkBlue', 'ForestGreen'])
    _graph.update_layout(title_x=0.5, font_family="Times New Roman", legend_title_text="<b>Term Deposit",
                      title_text='<b style="font-family: Times New Roman; font-size:1.3vw">Effect of Age on Personal Loan')
    return _graph


def plot_deposits_on_contact():
    a = df.groupby(['month', 'deposit'], as_index=False)['age'].count().rename(columns={'age': 'Count'})
    a['percent'] = round(a['Count'] * 100 / a.groupby('month')['Count'].transform('sum'), 1)
    a['percent'] = a['percent'].apply(lambda x: '{}%'.format(x))
    _graph = px.bar(a, x='month', y='Count', text='percent', color='deposit', barmode='group', template='simple_white',
                 color_discrete_sequence=['MediumPurple', 'YellowGreen'])
    _graph.update_layout(title_x=0.5, template='simple_white', showlegend=True, legend_title_text="Deposit",
                      title_text='<b style="color:black; font-size:100%;">Deposits based on last Contact month',
                      font_family="Times New Roman", title_font_family="Times New Roman")
    _graph.update_traces(marker=dict(line=dict(color='#000000', width=1)), textposition="outside")
    return _graph


def plot_deposit_on_contact():
    a = df.groupby(['month', 'deposit'], as_index=False)['age'].count().rename(columns={'age': 'Count'})
    a['percent'] = round(a['Count'] * 100 / a.groupby('month')['Count'].transform('sum'), 1)
    a['percent'] = a['percent'].apply(lambda x: '{}%'.format(x))
    _graph = px.bar(a, x='month', y='Count', text='percent', color='deposit', barmode='group', template='simple_white',
                 color_discrete_sequence=['MediumPurple', 'YellowGreen'])
    _graph.update_layout(title_x=0.5, template='simple_white', showlegend=True, legend_title_text="Deposit",
                      title_text='<b style="color:black; font-size:100%;">Deposits based on last Contact month',
                      font_family="Times New Roman", title_font_family="Times New Roman")
    _graph.update_traces(marker=dict(line=dict(color='#000000', width=1)), textposition="outside")
    return _graph


def plot_main():
    _graph = px.treemap(df.groupby(['job', 'deposit'], as_index=False)['age'].count().rename(columns={'age': 'Count'}),
                     path=['job', 'deposit', 'Count'], template='simple_white')
    _graph.update_layout(title_x=0.5, template='simple_white',
                      title_text='<b style="color:black; font-size:100%;">Treemap on count of clients who subscribed the Term Deposits or not based on Job',
                      font_family="Times New Roman", title_font_family="Times New Roman")
    _graph.update_traces(marker=dict(line=dict(color='#000000', width=1)))
    return _graph


def plot_main_term_deposit():
    a = df.groupby(['poutcome', 'deposit'], as_index=False)['age'].count().rename(columns={'age': 'Count'})
    a['percentile'] = round(a['Count'] * 100 / a.groupby('poutcome')['Count'].transform('sum'), 1)
    a['percentile'] = a['percentile'].apply(lambda x: '{}%'.format(x))
    _graph = px.bar(a, x='poutcome', y='Count', color='deposit', text='percentile', template='simple_white',
                 barmode='group', color_discrete_sequence=['MediumPurple', 'YellowGreen'])
    _graph.update_layout(title_x=0.08, template='simple_white', showlegend=True, legend_title_text="Deposit",
                      title_text='<b style="color:black; font-size:100%;">Term Deposits based on Outcome of Previous Marketing Campaign<br><b style="font-family: Times New Roman; font-size:1.0vw">% of term deposits opened based on the outcome of previous campaign',
                      font_family="Times New Roman", title_font_family="Times New Roman")
    _graph.update_traces(marker=dict(line=dict(color='#000000', width=1)), textposition="outside")
    return _graph


app.layout = html.Div(children=[
    html.H2(children="Objective: Optimize marketing resources by pinpointing potential customers interested in subscribing to term deposits, to focuse marketing efforts on target audience"),
    html.P("A term deposit is a fixed-term investment that includes the deposit of money into an account at a financial institution. "),

    html.H3(children="Overview of Dataset"),
    dcc.Dropdown(id="cat-select", options=[{"label":k, "value":k}  for k in cat_columns], value=cat_columns[0]),
    dcc.Graph('cat-graph'),

    html.H3(children="Clients description based on Maritial Status"),
    html.P(children="Most of the clients in the bank are Married - 56.9% and Single - 31.5%"),
    dcc.Graph(id='marriage-pie-chart', figure=plot_marriage_pie_chart()),

    html.Div([
        html.H3(children="Credit and Loan analysis"),
        html.P(children="98.3% customers in the bank doesn't have Credit in Default"),
        dcc.Graph(id='default-pie-chart', figure=plot_default_pie_chart(), style={'display': 'inline-block'}),
        html.P(children="On Comparing between housing loan and personal loan , most of the people subscribed for housing loan - 47.3%"),
        dcc.Graph(id='housing-pie-chart', figure=plot_housing_pie_chart(), style={'display': 'inline-block'}),
        dcc.Graph(id='loan-pie-chart', figure=plot_personal_loan(), style={'display': 'inline-block'})
    ]),

    html.Div([
        html.H2(children= "Based on Job type we want to analyse average balance and distribution of age"),
        dcc.Graph(id='avg-balance-bar-chart', figure=plot_avg_balance_based_on_job()),
        dcc.Graph(id='dist-age-job-box-chart', figure=plot_dist_age_based_on_job()),
    ]),

    dcc.Graph(id='age-loan-line-chart', figure=plot_line_age_loan()),
    html.P("From the Analysis, even the mid-age group clients are subscribed more for the personal loans, there are more number of clients who are not subscribing for the personal loans in this age group whereas old age people are not interested in personal loan"),
    dcc.Graph(id='deposits-on-contact-bar-chart', figure=plot_deposits_on_contact()),
    html.P("Most of the clients in the bank are contacted in the months of May, Jun, Jul and in Aug last year. More Clients subscribed to term deposits in this months only whereas very few of the clients are contacted in the months of Sep, Mar and in Dec. Even less contacts performed in these months, more number of clients subscribed to term deposits in these months. It is better to Contact clients more in this months."),
    dcc.Dropdown(id="campaign-effect-select", options=[{"label": k, "value": k} for k in ['Current Campaign', 'Previous Campaign']], value='Previous Campaign'),
    dcc.Graph(id='campaign-effect'),
    html.P("With the increase in previous contacts performed for the clients before this campaign there is more chance for the client to unsubscribe the term deposit"),
    dcc.Graph(id='main-result', figure=plot_main()),
    html.P("Conclusion of analysis that how many clients subscribed Term Deposit based on Job type"),
    dcc.Graph(id='main-term-deposit', figure=plot_main_term_deposit()),
    html.P("From the Outcome of previous Campaign, if the outcome is Success, then there is a high chance to the client will subscribe to the term deposit. out of all success outcomes 91.3% of clients subscribes and 8.7% are not subscribed to the term deposits")
],
    style={"width": "50%"}
)


@app.callback(
    Output(component_id='cat-graph', component_property='figure'),
    Input(component_id='cat-select', component_property='value')
)
def plot_cat(select_cat):
    value_counts = df[select_cat].value_counts()
    _graph = px.bar(value_counts, x=select_cat, title=f"Plot to show {select_cat} vs no. of responses", labels={
                     select_cat: "No. of responses",
                     "index": f"{select_cat} status" if select_cat != "month" else "month"
                 })
    return _graph

def plot_hist(selected_cat):
    _df = df[selected_cat]
    nbins = None
    if selected_cat == "balance":
        nbins = 5
    _graph = px.histogram(df, x=selected_cat, nbins=nbins)
    return _graph


@app.callback(
    Output(component_id='campaign-effect', component_property='figure'),
    Input(component_id='campaign-effect-select', component_property='value')
)
def plot_campaign_effects(selected_value):
    if selected_value == "Current Campaign":
        _graph = px.line(df.groupby(['campaign', 'deposit'], as_index=False)['age'].count().rename(columns={'age': 'Count'}),
                      x='campaign', y='Count', color='deposit', template='simple_white',
                      color_discrete_sequence=['DarkBlue', 'ForestGreen'])
        _graph.update_layout(title_x=0.08, font_family="Times New Roman", legend_title_text="<b>Term Deposit",
                          title_text='<b style="font-family: Times New Roman; font-size:1.3vw">Effect of Campaign on Term Deposits<b><br><b style="font-family: Times New Roman; font-size:1vw">number of contacts performed during the campaign and for this client </b>')
        return _graph
    _graph = px.line(df.groupby(['previous', 'deposit'], as_index=False)['age'].count().rename(columns={'age': 'Count'}),
                  x='previous', y='Count', color='deposit', template='simple_white',
                  color_discrete_sequence=['DarkBlue', 'ForestGreen'])
    _graph.update_layout(title_x=0.08, font_family="Times New Roman", legend_title_text="<b>Term Deposit",
                      title_text='<b style="font-family: Times New Roman; font-size:1.3vw">Effect of Previous Campaign on Term Deposits<b><br><b style="font-family: Times New Roman; font-size:1vw">number of contacts performed before this campaign and for this client </b>')
    return _graph


if __name__ == "__main__":
    app.run(debug=True, port=8049, dev_tools_hot_reload=True)
