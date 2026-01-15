import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.io import write_html
import random

def process_age_data():
    raw_age_data = pd.read_csv("data/raw/paris-2024-liste-athletes-engages-olypara.csv",delimiter=';')
    
    cleaned_age_data = raw_age_data[["Nationality","Discipline"]]
    cleaned_age_data.insert(cleaned_age_data.shape[1], 'Last Name', raw_age_data['Preferred Family Name'])
    cleaned_age_data.insert(cleaned_age_data.shape[1], 'First Name', raw_age_data['Preferred Given Name'])
    cleaned_age_data.insert(cleaned_age_data.shape[1], 'Age', raw_age_data['Date of Birth'].apply(lambda x: datetime.now()-datetime.strptime(x, '%Y-%m-%d')).apply(lambda x: int(x.days/365.25)))

    cleaned_age_data.to_csv("data/cleaned/paris-2024-athletes-age.csv", index=False, sep=';')

def ScatterDisciplineAge(age_data, color):
    trace = go.Scatter( x=age_data["Discipline"], y=age_data["Age"], mode="markers", text=age_data["Nationality"])#, marker=go.Marker(size=df["pop"]))
    trace.marker.size = 5
    trace.marker.color = color
    return trace


def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

def multi_trace_age(generate_html=False):
    age_data = pd.read_csv("data/cleaned/paris-2024-athletes-age.csv",delimiter=';')
    traces = []
    # Further processing and visualization can be added here
    disciplines = age_data['Discipline'].unique()
    countrys = age_data['Nationality'].unique()
    # for discipline in disciplines:
    #     one_trace = age_data.query(f"Discipline=='{discipline}'")
    #     one_trace = ScatterDisciplineAge(one_trace, random_color())
    #     traces.append(one_trace)
    for country in countrys:
        one_trace = pd.DataFrame()
        country_data = age_data.query(f"Nationality=='{country}'")
        for discipline in disciplines:
            disciplined_data = country_data.query(f"Discipline=='{discipline}'")
            one_trace = pd.concat([one_trace, disciplined_data.sort_values(by=['Age'])[disciplined_data.shape[0]//2:disciplined_data.shape[0]//2+1]], ignore_index=True)
        one_trace = ScatterDisciplineAge(one_trace, random_color())
        traces.append(one_trace)

    layout = go.Layout( title="Age vs Discipline of Athletes", xaxis_title="Discipline", yaxis_title="Age", xaxis=go.layout.XAxis(), yaxis=go.layout.YAxis())

    fig = go.Figure(data=traces, layout=layout)
    if(generate_html):
        write_html(fig, file="html/fig_age.html", auto_open=False, include_plotlyjs="cdn")
    return fig


if __name__ == "__main__":
    print("graph_age module")

    # process_age_data()
    multi_trace_age(generate_html=True)