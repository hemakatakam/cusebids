import dash
from dash import dcc, html, Input, Output, State
import pandas as pd

# Sample data
data = {
    'Item': ['Item A', 'Item B', 'Item C'],
    'Current Price': [100, 200, 150],
    'Highest Bidder': ['John', 'Alice', 'Bob']
}
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('Bidding App Dashboard'),
    
    # Display a table with bidding information
    html.Div([
        html.H2('Current Bids'),
        dcc.Graph(
            id='current-bids',
            figure={
                'data': [
                    {'x': df['Item'], 'y': df['Current Price'], 'type': 'bar', 'name': 'Current Price'},
                    {'x': df['Item'], 'y': [100, 150, 180], 'type': 'bar', 'name': 'Average Price'}
                ],
                'layout': {
                    'title': 'Bidding Summary'
                }
            }
        )
    ]),

    # Allow users to place new bids
    html.Div([
        html.H2('Place a Bid'),
        html.Label('Item:'),
        dcc.Dropdown(
            id='item-dropdown',
            options=[{'label': item, 'value': item} for item in df['Item']],
            value=df['Item'][0]
        ),
        html.Label('Your Name:'),
        dcc.Input(id='name-input', type='text', value=''),
        html.Label('Bid Amount:'),
        dcc.Input(id='bid-input', type='number', value=0),
        html.Button('Submit Bid', id='submit-bid-button', n_clicks=0),
        html.Div(id='bid-feedback')
    ])
])

# Define callback to process bid submission
@app.callback(
    Output('bid-feedback', 'children'),
    [Input('submit-bid-button', 'n_clicks')],
    [State('item-dropdown', 'value'),
     State('name-input', 'value'),
     State('bid-input', 'value')])
def process_bid(n_clicks, selected_item, name, bid_amount):
    if n_clicks > 0:
        if not name:
            return "Please enter your name."
        elif bid_amount <= 0:
            return "Bid amount must be greater than zero."
        else:
            # Update dataframe with new bid
            idx = df.index[df['Item'] == selected_item][0]
            if bid_amount > df.loc[idx, 'Current Price']:
                df.loc[idx, 'Current Price'] = bid_amount
                df.loc[idx, 'Highest Bidder'] = name
                return f"Bid submitted for {selected_item} by {name} with amount {bid_amount}."
            else:
                return "Your bid must be higher than the current highest bid."
    else:
        return ''

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
