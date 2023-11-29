import dash
from dash import Dash, dcc, html
import dash_mantine_components as dmc
import dash_leaflet as dl
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


categories_df = pd.read_csv('datasets/entreprise_types.csv')
categories_df.columns = ['APE_code', 'libelle']
categories_df['value'] = categories_df['APE_code'] + ' ' + categories_df['libelle']
# categories_df.head()

ca_categories_df = pd.read_csv('datasets/ca_categories.csv')
ca_categories_df.columns = ['ca_category', 'base_CFE']
# ca_categories_df.head()

local_categories_df = pd.read_csv('datasets/local_categories.csv', header=1)
local_categories_df.columns = ['local_category', 'name', 'secteur_1', 'secteur_2', 'secteur_3', 'secteur_4', 'secteur_5']
# local_categories_df.head()

city_df = pd.read_csv("https://static.data.gouv.fr/resources/communes-de-france-base-des-codes-postaux/20200309-131459/communes-departement-region.csv")
city_df = city_df[city_df['code_departement'] == '16']
# city_df.head()

# Results
all_results_df = pd.read_csv('datasets/results.csv')
all_results_df = all_results_df.drop(columns=['SECTEUR_CFE_Base', 'TARIF_M2', 'BASE', 'CFE', 'TFB', 'ZRC'])
all_results_df['Total d\'impôts à payer'] = all_results_df['Total d\'impôts à payer'].str.replace(',', '.').astype(float)

# Load your GeoJSON data
charente_geojson = 'https://france-geojson.gregoiredavid.fr/repo/departements/16-charente/communes-16-charente.geojson'

def create_table(df):
    new_df = df.drop(columns=['libelle']).sort_values(by='Total d\'impôts à payer').head(10)
    columns, values = new_df.columns, new_df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dmc.Title(
            f"Quelle collectivité territoriale pour mon entreprise ?",
            order=1,
            style={'text-align': 'center', 'marginTop': 40, 'marginBottom': 20}),

        dmc.Grid(
			children=[
				dmc.Col([
                    dmc.Title(
						f"Votre entreprise",
						order=3,
						style={'marginTop': 40, 'marginBottom': 20}),

					dmc.Select(
						id="entreprise-category-input",
						data=categories_df.value,
						placeholder="Secteur d'activité",
						searchable=True,
						style={"width": '100%', "marginBottom": 10},
					),

					dmc.Select(
						id="ca-category-input",
						data=ca_categories_df.ca_category,
						placeholder="Chiffre d\'affaire",
						searchable=True,
						style={"width": '100%', "marginBottom": 10},
					),

					dmc.Title(
						f"Votre local",
						order=3,
						style={'marginTop': 40, 'marginBottom': 20}),

					dmc.Select(
						id="local-category-input",
						data=local_categories_df.name,
						placeholder="Type de local",
						searchable=True,
						style={"width": '100%', "marginBottom": 10},
					),

					dmc.NumberInput(
						id='surface-input',
						label="Surface de votre local (m2):",
						value=0,
						min=0,
						step=5,
						style={"width": '100%', "marginBottom": 10},
					),

					dmc.Checkbox(
						id="owner-input",
						label="Je suis propriétaire de mes locaux",
						style={"width": '100%', "marginBottom": 10},
					),

					dmc.Title(
						f"Implantation",
						order=3,
						style={'marginTop': 40, 'marginBottom': 20}),

					dmc.Select(
						id="locality-input",
						data=['Charente'],
						placeholder="Choisissez votre territoire cible",
						searchable=True,
						style={"width": '100%', "marginBottom": 10},
					),
				], style={"width": '100%', "marginLeft": 20, "marginRight": 20}, span=4),

				dmc.Col([
					dmc.Title(
						f"Carte des communes les plus attractives",
						order=3,
						style={'text-align': 'center', "marginTop": 40}),

					dcc.Graph(
						id='charente-map',
						config={'displayModeBar': False},
					),
				], style={"marginLeft": 0, "marginRight": 20}, span='auto'),
			],
			gutter="xl",
		),
        html.Div(
            [
                dmc.Title(
						f"Classement des communes les plus attractives (Top 10)",
						order=3,
						style={'marginTop': 40, 'marginBottom': 20}),

				dmc.Table(
					id='output-table',
					verticalSpacing="sm",
					striped=True,
					highlightOnHover=True,
					withBorder=True,
					withColumnBorders=True,
					horizontalSpacing=10,
				),
			],
            style={"marginLeft": 40, "marginRight": 40}
		),
        dmc.Footer(
            height=60,
			children=[
                dmc.Text("Données : DGFiP, IGN", size="md", style={"marginTop": 30}),
                dmc.Text("Traitements : Équipe 8", size="md"),
                dmc.Text("Champ : Estimation des impôts locaux à payer, après exonération", size="md", style={"paddingBottom": 30}),
			],
			style={"margin": 50},
		),
        html.Div(id='table-output')
    ]
)

@app.callback(
    Output('output-table', 'children'),
    Input('entreprise-category-input', 'value')
)
def update_output_table(category):
	results_df = all_results_df[all_results_df['libelle'] == category]

	return create_table(results_df)

@app.callback(
    Output('charente-map', 'figure'),
    Input('entreprise-category-input', 'value')
)
def update_output_div(category):
	results_df = all_results_df[all_results_df['libelle'] == category]
	# Join with city_df nom_commune_postal
	results_df = pd.merge(results_df, city_df,
                       left_on='Commune',
                       right_on='nom_commune_postal',
                       how='right')
	results_df.fillna(method='ffill', inplace=True)

	# Create a choropleth map
	fig = px.choropleth_mapbox(
		results_df,
		geojson=charente_geojson,
		locations='code_commune_INSEE',
		featureidkey="properties.code",
		color='Total d\'impôts à payer',
		color_continuous_scale='blues',
		hover_name='nom_commune',
		hover_data='nom_commune',
		mapbox_style="carto-positron",
		zoom=8,
		height=700,
		center={"lat": 45.65, "lon": 0.15}
	)
	fig.update_layout(coloraxis_colorbar=dict(title='Impôts locaux (€)'))
	return fig

if __name__ == '__main__':
    app.run(debug=True)
