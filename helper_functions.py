""" Helper functions for use in app.py """
import plotly.graph_objects as go
import sqlite3

def generate_graph(data):
    """
    To generate a dynamic graph front-end via Plotly with drop down menu based on variables in input data.
    input : data (List)
            A list of tuples for each row of data provided.
            e.g. data[0] = ('13-05-2022', 985.0, 985.0, 920.0, 920.0, 920.0, 211)
    output: fig (plotly fig)
            A plotly graph with the processed information from the input data
    """

    # create graph
    fig = go.Figure(layout_yaxis_range=[0,1600], layout_xaxis_range=["03-01-2022", "06-10-2022"])
    x = [row[0] for row in data]
    vars = ['All', 'Open', 'High', 'Low', 'Close*', 'Adj_Close**', 'Volume']
    line_colours = [
    '#ff7f0e',  # muted blue
    '#1f77b4',  # safety orange
    'burlywood',  # burlywood
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#e377c2',  # raspberry yogurt pink
    '#17becf'   # blue-teal
    ]
    for v in range(1,7):
        y = [row[v] for row in data]
        fig.add_trace(
            go.Scatter(
                x = x,
                y = y,
                name = vars[v],
                line_color = line_colours[v]
            )
        )

    # Create drop down menu with multi-choice options
    fig.update_layout(
        width=1400,
        height=700,
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=list(
                # Options for dropdown menu to dynamically display on graph
                [dict(label = 'All',
                    method = 'update',
                    # Bool values select which table elements to display or not
                    args = [{'visible': [True, True, True, True, True, True]},
                            {'title': 'All',
                            'showlegend':True}]),
                dict(label = 'Open',
                    method = 'update',
                    args = [{'visible': [True, False, False, False, False, False]}, 
                            {'title': 'Open',
                            'showlegend':True}]),
                dict(label = 'High',
                    method = 'update',
                    args = [{'visible': [False, True, False, False, False, False]},
                            {'title': 'High',
                            'showlegend':True}]),
                dict(label = 'Low',
                    method = 'update',
                    args = [{'visible': [False, False, True, False, False, False]},
                            {'title': 'Low',
                            'showlegend':True}]),
                dict(label = 'Close*',
                    method = 'update',
                    args = [{'visible': [False, False, False, True, False, False]},
                            {'title': 'Close*',
                            'showlegend':True}]),
                dict(label = 'Adj Close**',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, True, False]},
                            {'title': 'Adj Close**',
                            'showlegend':True}]),
                dict(label = 'Volume',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, True]},
                            {'title': 'Volume',
                            'showlegend':True}]),
                ])
            )
        ])
    
    # adjust xaxis formatting 
    fig.update_xaxes(
        tickangle = 55,
        title_text = "Date",
        title_font = {"size": 20},
        title_standoff = 25)
    
    # adjust yaxis formatting 
    fig.update_yaxes(
        title_text = "Units",
        title_font = {"size": 20},
        title_standoff = 25)
    
    return fig

def fetch_all_data():
    """
    Gets all data from database.
    input: None
    output: Data from database in rows by tuple
    """
    
    # Connect to the database
    conn = sqlite3.connect('timbers_future.db')
    cursor = conn.cursor()
    
    # Get the data (reversing order to keep date from earlier to later)
    cursor.execute('''
        SELECT DISTINCT STRFTIME('%d-%m-%Y', date), open, high, low, close, adj_close, volume  
        FROM lumber_futures 
        WHERE COALESCE(date, open, high, low, close, adj_close, volume) IS NOT NULL 
        AND open NOT LIKE '%-%'
        ORDER BY date ASC;
        
    ''')

    data = cursor.fetchall()
    
    # Close connection
    conn.close()
    return data