from flask import Flask, request, render_template
import pandas as pd
import pyarrow.parquet as pq
import requests

app = Flask(__name__)

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
    ser = request.form.get('ser')
    num = int(request.form.get('num'))
    row = find_row(ser, num, 'https://storage.googleapis.com/base_primera/prueba.parquet')

    if row is not None:
        col_to_label = {
            'porc_fa_p_19': 'FA',
            'porc_pn_p_19': 'PN',
            'porc_pc_p_19': 'PC',
            'porc_ca_p_19': 'CA',
            'porc_pi_p_19': 'PI',
            'porc_otros_p_19': 'OTROS'
        }
        results = {label: round(row.iloc[0][col] * 100, 2) for col, label in col_to_label.items()}
        return render_template('result.html', results=results)
    else:
        return "Data not found for the given series and number."

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT not set
    app.run(host='0.0.0.0', port=port, debug=False)
