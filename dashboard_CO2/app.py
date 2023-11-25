from flask import Flask, request, jsonify, render_template
import json
import pandas as pd
import plotly.express as px

app = Flask(__name__)

df_total = pd.read_csv('countries_df.csv')
df_percap = pd.read_csv('co-emissions-per-capita.csv')

def get_total(country = 'Germany'):
        d = df_total[df_total['Entity']==country]
        d = d[d['Year']==2021]
        print(d)
        return int(d['Annual CO₂ emissions'])

def get_percap(country = 'Germany'):
        d = df_percap[df_percap['Entity']==country]
        d = d[d['Year']==2021]
        print(d)
        return int(d['Annual CO₂ emissions (per capita)'])

def get_graph(country = 'Germany', emissions = 'total'):
    # Import libraries
    import pandas as pd
    import plotly.express as px

    col = 'Annual CO₂ emissions'

    if emissions == 'total':
        df = df_total
        col = 'Annual CO₂ emissions'
    else:
        df = df_percap
        col = "Annual CO₂ emissions (per capita)"

    fig = px.line(df[df['Entity']==country], x='Year', y = col, color='Entity', title = 'Country',
                   template='none', width=800, height=400)

    
    graphJSON = fig.to_json()
    return graphJSON

def template(params):
    return render_template(params['template'], params=params)

@app.route('/')
@app.route('/ddsimple')
def ddsimpleindex():
    # The root endpoint builds the page
    header = "Global CO2 Emissions"
    subheader = "Global CO2 Emissions since 1850"
    description = """The graph shows the increase in temperature year on year.
    The data spans the years 1881 to 2022 and includes temperature anomalies for periods of each year as indicated.
    """
    menu_label = "Select a country"
    params = {    
        'template': 'ddsimpleindex.html',
        'title': header,
        'subtitle': subheader,
        'content' : description,
        'menu_label': menu_label,
        'options' : [{'code':'United Kingdom', 'desc':'United Kingdom'},
                     {'code':'United States','desc':'United States'},
                     {'code':'China','desc':'China'},
                     {'code':'India','desc':'India'},
                     {'code':'Germany','desc':'Germany'}],
        'graph'   : get_graph(),
        'radio_legend' : "Select total emissions or percapita",
        'radio_options': [{'code':'percap', 'desc':"Emissions Per Capita", 'checked':''},
                          {'code':'total', 'desc':'Total Emissions', 'checked':'checked'}],
        'panel1': {'header': 'Per Capita 2021', 'desc':get_percap()},
        'panel2': {'header': 'Total 2021', 'desc': get_total()}
    }
    return template(params)


#### Callback for drop down menu ####

@app.route('/callback', methods=['POST'])
def callback():
    # The callback updates the page
    if request.is_json:
        data = request.get_json()
        print(data)
        graph = get_graph(country=data['dropdown'], emissions=data['radio1'])
        emissions_total = get_total(country=data['dropdown'])
        emissions_percap = get_percap(country=data['dropdown'])
        return json.dumps({'graph': graph, 'emissions_total': emissions_total, 'emissions_percap': emissions_percap})
    else:
        return jsonify({"error": "Invalid JSON data"}), 400

#### Main ####

if __name__ == '__main__':
    app.run(debug=True)


