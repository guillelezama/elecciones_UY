# Repository: Yamandú Orsi Age-Based Voting Comparison

This repository provides an analysis of voting patterns for Yamandú Orsi across various age groups in Uruguay. The main objective is to compare Orsi’s vote share among *new voters* (those who did not vote in the previous election) against different older voter cohorts. 

## Structure

- **`ages_voting.ipynb`**  
  The primary Jupyter Notebook containing all the code and visualization logic. It generates three scatter plots comparing the vote of new voters versus:
  1. Vote share among people older than 43 years in Canelones and Montevideo.
  2. Vote share among people older than 58 years in all departments *except* Montevideo.
  3. Vote share among the oldest individuals in each *serie* (precinct code).

- **`data/`**  
  Folder containing all the necessary datasets for the analysis (e.g., voter demographics, election results).

- **`output/`**  
  Folder where the images (graphs) produced by the notebook are saved.

## Key Findings

- New voters (those who did not participate in the previous election) consistently supported Yamandú Orsi at higher rates compared to older age groups.
- This trend holds true for both Canelones and Montevideo (comparing with voters over 43), as well as for the rest of the departments (comparing with voters over 58).
- Even within individual *series* (precinct codes), the oldest voters tended to support Orsi less than their younger counterparts.

## Contributing
Contributions are welcome! If you notice issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Data
credenciales2004.csv is not available in the repository as it is too large. If you want to use it, send me an email.