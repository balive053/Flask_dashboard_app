""" 
Main app.py file for Flask views. 
Calls helper functions from helper_functions.py and database_builder.py 
"""

from flask import Flask, render_template
import plotly, json
import matplotlib
matplotlib.use('SVG') # Needed fix for back-end issue with plotting matplotlib graphs in Flask 
# import local functions
from helper_functions import generate_graph, fetch_all_data 
from database_builder import create_database, import_data_to_database, key_values


# create sqlite3 database and table 
create_database()
# import data into database 
import_data_to_database()


# main app setup and config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

key_vals = key_values()

@app.route('/view')
def view_data():
    """
    Flask View to display data in tabular form
    """
    # Fetch the data from the database and render template
    data = fetch_all_data()
    return render_template('view_data.html', data=data)


@app.route('/graph')
def view_graph():
    """
    Flask View to display dynamic graph of selected data
    """
    # Fetch the data from the database
    data = fetch_all_data()
    
    # Generate graph
    fig = generate_graph(data)
    # Convert the plot to JSON for HTML view
    data = [fig]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('view_graph.html', graphJSON=graphJSON, key_vals=key_vals)
    

# View function for Home Page
@app.route('/')
def home():
    return render_template('home.html')


# View function for About Us Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "main":
    app.run(debug=True)