# Elections Result Data Viewer

This Flask application allows users to query and view the results of their precint in the 2019 Uruguayan Elections, based on an id number.

It queries rows from a Parquet file hosted online based on user input. It provides a simple web interface where users can enter a series (`ser`) and a number (`num`) to search for corresponding data in the Parquet file.

## Features

- Web form to accept user input for series and number.
- Downloads and reads Parquet file in chunks to find the specific row.
- Displays results on a web page if the row is found.

## Dependencies

- Flask
- pandas
- pyarrow
- requests

This application requires Python 3.6+.

## Usage

To run the application:

1. Activate the virtual environment if it's not already activated.
2. Start the Flask app.
3. Open your web browser and navigate to `http://127.0.0.1:5000/`.

Enter a series and number in the form and submit to view the data. If the data for the given series and number is found, the application will display the results.

## Development

This application is set up for development with Flask's debug mode turned off. For development purposes, you can set `debug=True` in `app.run()` within `app.py`. However, ensure that debug mode is turned off in production environments for security reasons.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

