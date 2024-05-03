# Libraries
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

# Dataset
df = pd.read_csv('assets/anime_data.csv')

# Setup
df['year'] = df["aired_from"].str[:4]
df = df[df["year"].notna()].astype({'year': 'int'})

genres = []
for row in df['genres'].unique():
    for genre in eval(row):
        if genre not in genres:
            genres += [genre]


def byYear(group):
    out_frame = pd.DataFrame(genres)
    gq = [0 for i in genres]  # Genre Quantity
    tsbg = [0 for i in genres]  # Total Scores By Genre

    for genres_list, score in zip(group['genres'], group['score']):
        for genre_name in eval(genres_list):
            genre_index = genres.index(genre_name)
            gq[genre_index] += 1
            tsbg[genre_index] += score

    out_frame['Quantity'] = pd.DataFrame(gq)
    out_frame['Mean Score'] = pd.DataFrame([
        total / quantity if quantity > 0 else float("NaN")
        for total, quantity in zip(tsbg, gq)
    ])
    out_frame.rename(columns={0: "Genre"}, inplace=True)

    return out_frame


by_year = df.groupby('year').apply(byYear).reset_index().drop("level_1",
                                                              axis=1)

# Figures
score_dist = px.histogram(df, x="score",
                          title="Distribution of Scores").update_layout(
                              yaxis_title="Count", xaxis_title="Score")
genre_count = by_year.groupby("Genre")["Quantity"].sum().reset_index()
genre_count.loc[genre_count['Quantity'] < genre_count['Quantity'].sum() / 100 *
                1.5, 'Genre'] = 'Other'
genre_dist = px.pie(genre_count,
                    values="Quantity",
                    names="Genre",
                    title="Pie chart of genres")
rating_score_dist = px.box(df,
                           x='score',
                           y="rating",
                           title="Score distribution by rating").update_layout(
                               yaxis_title="Rating", xaxis_title="Score")
scores_over_time = px.box(df, x="year", y="score",
                          title="Scores Over Time").update_layout(
                              yaxis_title="Score", xaxis_title="Year")
animated_quantity_score_boot = px.scatter(
    by_year,
    x="Quantity",
    y="Mean Score",
    animation_frame="year",
    title="Quantity and Mean Score of Anime by Genre over Time",
    size="Quantity",
    animation_group="Genre",
    color="Genre",
    size_max=55,
    range_x=[1, 260],
    range_y=[3.5, 8.5],
    log_x=True)
quantity_over_time_boot = px.scatter(by_year,
                                     x="year",
                                     y="Quantity",
                                     color="Genre",
                                     title="Quantity of Anime over Time")
mean_score_over_time_boot = px.scatter(by_year,
                                       x="year",
                                       y="Mean Score",
                                       color="Genre",
                                       title="Mean Score of Anime over Time")

# Dash Related
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card([
    html.Span(className="dot", id="closer"),
    html.Div([
        html.
        P("I used the dataset below to mess around with data visualization."
          ),
        html.
        A("Anime Data",
          href=
          "https://www.kaggle.com/datasets/thunderz/anime-dataset?resource=download&select=anime_data.csv"
          ),
        html.
        P("To toggle genres, click on the genre names on the right side of the graphs. Select a section of the graph to zoom in. The dot in the top left closes this menu. Made using Plotly, Dash and severe sleep deprivation. Please send feedback :)"
          ),
        html.A("Send Feedback", href="https://forms.gle/J5C1vvxtw6qjsjQ26")
    ],
             id="close"),
    html.H5("Made By Kian :)")
],
                    body=True,
                    id="card")

app.layout = dbc.Container([
    controls,
    dbc.Row(
        dbc.Col(dcc.Loading(dcc.Graph(figure=animated_quantity_score_boot)),
                md=12)),
    dbc.Row(
        dbc.Col(dcc.Loading(dcc.Graph(figure=quantity_over_time_boot)),
                md=12)),
    dbc.Row(
        dbc.Col(dcc.Loading(dcc.Graph(figure=mean_score_over_time_boot)),
                md=12)),
dbc.Row(dbc.Col(dcc.Loading(dcc.Graph(figure=score_dist)), md=12)),
    dbc.Row(dbc.Col(dcc.Loading(dcc.Graph(figure=genre_dist)), md=12)),
    dbc.Row(dbc.Col(dcc.Loading(dcc.Graph(figure=rating_score_dist)), md=12)),
    dbc.Row(dbc.Col(dcc.Loading(dcc.Graph(figure=scores_over_time)), md=12))
],
                           id="main-container")

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=False)
