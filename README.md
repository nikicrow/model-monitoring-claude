How to Use

Install required packages:

Copy

```pip install dash dash-bootstrap-components plotly pandas numpy```

Run the application:

Copy

```python app.py```

Access the dashboard in your browser at http://127.0.0.1:8050/
To export as HTML, you can use a browser's "Save page as" feature or implement an export button with Dash's dcc.Download component.

The code is easily extendable - you can add new visualizations or metrics by creating additional callback functions and UI elements. The mock data generation can also be replaced with