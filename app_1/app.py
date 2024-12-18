from flask import Flask, request, render_template
import pandas as pd
import pyarrow.parquet as pq
import requests
import plotly.graph_objects as go
import numpy as np
import os

app = Flask(__name__)

query_counter = 0

# Function to download and find the specific row based on 'ser' and 'num' in the Parquet file
def find_row(ser, num, url):
    # Download the file
    r = requests.get(url)
    if r.status_code == 200:
        with open('temp_file.parquet', 'wb') as f:
            f.write(r.content)
        
        # Read the file in chunks
        parquet_file = pq.ParquetFile('temp_file.parquet')
        for batch in parquet_file.iter_batches(batch_size=10000):
            df = batch.to_pandas()
            row = df[(df['serie'] == ser.upper()) & (df['number'] == num)]
            if not row.empty:
                return row
        return None
    else:
        raise Exception("Failed to download the file")

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    global query_counter
    ser = request.form.get('ser')
    num = int(request.form.get('num'))
    row = find_row(ser, num, 'https://storage.googleapis.com/base_primera/prueba.parquet')

    if row is not None:
        circ_votos = row  
        query_counter += 1  # Increment the counter here

        # Setting up the party columns
        cols_fa = [i for i in circ_votos.columns if i.startswith('porc_fa_p')]
        cols_pn = [i for i in circ_votos.columns if i.startswith('porc_pn_p')]
        cols_pc = [i for i in circ_votos.columns if i.startswith('porc_pc_p')]
        cols_pi = [i for i in circ_votos.columns if i.startswith('porc_pi_p')]
        cols_ca = [i for i in circ_votos.columns if i.startswith('porc_ca_p')]
        party = cols_fa + cols_pn + cols_pc + cols_pi + cols_ca

        lines = {'porc_fa_p': [], 'porc_pn_p': [], 'porc_pc_p': [], 'porc_pi_p': [], 'porc_ca_p': []}
        filtered_df = circ_votos[party]  
        
        # Populating lines
        for col in filtered_df.columns:
            parts = col.split('_')
            par = parts[1]
            type = parts[2]  # Extract 'p' or 'e'
            year_suffix = int(parts[3]) + 2000

            if len(parts) == 5:  # Handling '_b' suffix
                year = year_suffix + 0.2  # Shift the year slightly to the right for '_b' columns
            else:
                year = year_suffix

            # Append the data point to the respective list
            average_value = filtered_df[col].mean()
            lines['porc_' + par + '_' + type].append((year, average_value))
        
        # Plot figure
        fig = go.Figure()

        # Including all special cases and color specifications
        party_names, special_cases, color_map = setup_graph_details()

        for line_type, data_points in lines.items():
            hover_texts = []
            years, values = zip(*sorted(data_points)) if data_points else ([], [])
            for year, value in zip(years, values):
                formatted_value = np.round(value * 100, 2)
                if str(year) in special_cases and line_type in special_cases[str(year)]:
                    hover_text = f"{special_cases[str(year)][line_type]} ({year}): {formatted_value}%"
                else:
                    hover_text = f"{party_names[line_type]} ({year}): {formatted_value}%"
                hover_texts.append(hover_text)
            
            if line_type == 'porc_fa_p':
                # Handling multi-color for Frente Amplio with specific sizes for each color
                fig.add_trace(go.Scatter(x=years, y=values, mode='markers', marker=dict(color=color_map[line_type][0], size=20), hoverinfo='text', text=hover_texts, showlegend=False))
                fig.add_trace(go.Scatter(x=years, y=values, mode='markers', marker=dict(color=color_map[line_type][1], size=15), hoverinfo='skip', showlegend=False))
                fig.add_trace(go.Scatter(x=years, y=values, mode='markers', marker=dict(color=color_map[line_type][2], size=5), hoverinfo='skip', showlegend=False))

            else:
                fig.add_trace(go.Scatter(x=years, y=values, mode='markers', marker=dict(color=color_map[line_type], size=20), hoverinfo='text', text=hover_texts, name=party_names[line_type], showlegend=False))

        fig.update_layout(title=f"Voto en el circuito de la serie {ser} {num}", xaxis_title='Año', yaxis_title='Porcentaje sobre voto a partidos')

        graph_html = fig.to_html(full_html=False)
        return render_template('result_with_graph.html', graph_html=graph_html, query_count=query_counter)
    else:
        return "Data not found for the given series and number."

def setup_graph_details():
    party_names = {
        'porc_fa_p': 'Frente Amplio',
        'porc_pn_p': 'Partido Nacional',
        'porc_pc_p': 'Partido Colorado',
        'porc_pi_p': 'Partido Independiente',
        'porc_ca_p': 'Cabildo Abierto'
    }

    special_cases = {
        '2022': {
            'porc_fa_p': 'SI Derogar LUC',
            'porc_pn_p': 'NO Derogar LUC'
        }
    }

    color_map = {
        'porc_fa_p': ['red', 'blue', 'white'],  # This series will use a combination of red, blue, and white
        'porc_pn_p': 'blue',
        'porc_pc_p': 'red',
        'porc_pi_p': 'purple',
        'porc_ca_p': 'green'
    }
    return party_names, special_cases, color_map

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
