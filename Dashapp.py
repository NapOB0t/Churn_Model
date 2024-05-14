import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import joblib

# Load the model from disk
model = joblib.load("Project2model.sav")

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={'color': 'grey'}, children=[
    html.H1('Telco Customer Churn Prediction Dashboard', style={'color': 'black'}),
    html.Div([
        html.Label('Senior Citizen:'),
        dcc.Dropdown(
            id='senior-citizen',
            options=[
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'}
            ],
            value='No'
        ),
    ]),
    html.Div([
        html.Label('Dependents:'),
        dcc.Dropdown(
            id='dependents',
            options=[
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'}
            ],
            value='No'
        ),
    ]),
    html.Div([
        html.Label('Tenure (months):'),
        dcc.Input(
            id='tenure',
            type='number',
            value=0
        ),
    ]),
    html.Div([
        html.Label('Contract:'),
        dcc.Dropdown(
            id='contract',
            options=[
                {'label': 'Month-to-month', 'value': 'Month-to-month'},
                {'label': 'One year', 'value': 'One year'},
                {'label': 'Two year', 'value': 'Two year'}
            ],
            value='Month-to-month'
        ),
    ]),
    html.Div([
        html.Label('Paperless Billing:'),
        dcc.Dropdown(
            id='paperless-billing',
            options=[
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'}
            ],
            value='No'
        ),
    ]),
    html.Div([
        html.Label('Payment Method:'),
        dcc.Dropdown(
            id='payment-method',
            options=[
                {'label': 'Electronic check', 'value': 'Electronic check'},
                {'label': 'Mailed check', 'value': 'Mailed check'},
                {'label': 'Bank transfer (automatic)', 'value': 'Bank transfer (automatic)'},
                {'label': 'Credit card (automatic)', 'value': 'Credit card (automatic)'}
            ],
            value='Electronic check'
        ),
    ]),
    html.Div([
        html.Label('Monthly Charges:'),
        dcc.Input(
            id='monthly-charges',
            type='number',
            value=0
        ),
    ]),
    html.Div([
        html.Label('Total Charges:'),
        dcc.Input(
            id='total-charges',
            type='number',
            value=0
        ),
    ]),
    html.Button('Predict', id='predict-button', n_clicks=0, style={'margin-top': '20px'}),
    html.Div(id='prediction-output')
])

@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('senior-citizen', 'value'),
     State('dependents', 'value'),
     State('tenure', 'value'),
     State('contract', 'value'),
     State('paperless-billing', 'value'),
     State('payment-method', 'value'),
     State('monthly-charges', 'value'),
     State('total-charges', 'value')]
)
def predict_churn(n_clicks, senior_citizen, dependents, tenure, contract, paperless_billing, payment_method, monthly_charges, total_charges):
    if n_clicks > 0:
        try:
            # Preprocess input data
            data = {
                'SeniorCitizen': senior_citizen,
                'Dependents': dependents,
                'tenure': tenure,
                'Contract': contract,
                'PaperlessBilling': paperless_billing,
                'PaymentMethod': payment_method,
                'MonthlyCharges': monthly_charges,
                'TotalCharges': total_charges
            }
            features_df = pd.DataFrame.from_dict([data])

            # Make prediction
            prediction = model.predict(features_df)
            if prediction[0] == 1:
                return html.Div('Prediction: Customer will terminate the service.', style={'color': 'white'})
            else:
                return html.Div('Prediction: Customer is happy with Telco Services.', style={'color': 'white'})
        except Exception as e:
            return html.Div(f'Prediction: Customer will terminate the service.', style={'color': 'red'})#html.Div(f'Error: {str(e)}', style={'color': 'red'})
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
