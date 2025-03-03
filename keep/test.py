import dash
from dash import html
import dash_mantine_components as dmc

app = dash.Dash(__name__)

app.layout = dmc.MantineProvider(  # Wrap the layout inside MantineProvider
    children=html.Div([
        dmc.Button("Click Me", color="blue", size="lg"),
        dmc.Text("This is a test Mantine component.", size="md"),
    ])
)

if __name__ == "__main__":
    app.run_server(debug=True)
