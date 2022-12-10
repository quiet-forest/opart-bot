import openai
import os

from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

#El bot con OpenAi

conversation = ""

openai.api_key = "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"


def run_preset_10(conversation):
    conversation += "\n" + "\nNaomi:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=conversation,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", "Naomi:"]
    )
    anwer = response.choices[0].text.strip()
    conversation += anwer
    return response.choices[0].text.strip()

#Aplicacion web en jupyter dash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H5("GPT-3 ChatBot API para O-Part Gaming"),
    dcc.Dropdown(
        id='dropdown-preset',
        options=[
            {'label': 'Naomi Assistant', 'value': '10'}
        ],
        placeholder="Load a preset"
    ),
    dcc.Textarea(
        id='textarea-conversation',
        value='',
        placeholder="Escribe tu consulta",
        style={'width': '100%', 'height': 300},
    ),
    html.Div(id='textarea-conversation-output', style={'whiteSpace': 'pre-line', 'padding-top': '10px'}),
    html.Button('Enviar', id='button-generate', n_clicks=0),
    html.Div(id='div-output-results', style={'padding-top': '10px'}),
    html.Pre(
        id='div-output-results2',
        style={
            'height': 200,
            'overflow': 'auto',
            'font-family': 'courier new',
            'font-weight': 'bold',
            'color': 'white',
            'background-color': 'LightSlateGrey',
            'padding': '10px',
            'font-size': '100%',
            'border': 'solid 1px #A2B1C6'
        }

    ),

], style={
    'border': 'solid 1px #A2B1C6',
    'border-radius': '5px',
    'padding': '20px',
    'margin-top': '10px'
})


@app.callback(
    Output(component_id='textarea-conversation', component_property='value'),
    Input(component_id='dropdown-preset', component_property='value'),
)
@app.callback(
    Output(component_id='div-output-results2', component_property='children'),
    State(component_id='textarea-conversation', component_property='value'),
    State(component_id='dropdown-preset', component_property='value'),
    Input('button-generate', 'n_clicks')
)
def update_output2(textarea, preset, n_clicks):
    if n_clicks is None or n_clicks == 0:
        return '(Todavia nada...)'
    else:

        results = globals()['run_preset_%s' % preset](textarea)
        return results


app.run_server(debug=False, host="0.0.0.0", port="8080")
