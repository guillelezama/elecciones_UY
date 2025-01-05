# Repository: Uruguay Elections Longitudinal Analysis

This repository contains a notebook that analyzes changes in voting behavior over time by leveraging Uruguay's stable voter identification system. Specifically, it focuses on the evolution of the vote share for the Frente Amplio (FA) in each precinct from 2004 to 2024.

## Structure

- **`data/`**  
  This folder contains all the required data files, including information on voter IDs, precinct codes (*Serie*), and department-level data (*departamentos*). Ensure that you have the correct data files here before running the notebook.

- **`notebook.ipynb`**  
  The primary Jupyter Notebook, where you can call the `create_graph` function to generate visualizations. By inputting a precinct’s *Serie* and the corresponding *departamento*, the notebook will show how FA’s vote share evolved over time and highlight how new voters (those with ID numbers higher than the maximum from the previous election) voted.

## Usage
create_graph(serie, departamento)

- serie: The electoral code for the city or neighborhood.
- departamento: The department where the city or neighborhood is located.

This function displays how the same voters’ choices have changed (since voter IDs remain constant across elections) and highlights how new voters (with newly assigned IDs) have influenced overall vote trends.

## Contributing
If you have any suggestions or improvements, feel free to submit a pull request or open an issue. Contributions are always welcome!
