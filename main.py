import pandas as pd
from sklearn.metrics import cohen_kappa_score
from krippendorff import alpha
import json


# Find Cohens Kappas
def calculate_kappas():
    # Get all the values
    values = pd.read_csv("triplets.csv")

    # Define the columns we want to look at
    # Change before each calculation if you're looking at different columns
    # NOTE I removed Hermes
    columns_of_interest = ["Emily", "Alessio", "ChatGPT 3.5", "ChatGPT 4 (Prompted with 1)", "ChatGPT 4 (Prompted with 2)"]

    # Get the values for each of those columns
    values_given_column = []
    for column in columns_of_interest:
        values_given_column.append(list(values[column]) )

    # For each combination of columns, get the Kappa score
    num_columns = len(columns_of_interest)
    Kappas = []
    for i in range(num_columns - 1):
        for j in range(i + 1, num_columns):
            # Make sure that the lists are the same length
            # This assumes that the filled in values are consistent and left aligned
            list_i = values_given_column[i]
            list_j = values_given_column[j]
            min_list_length = min(len(list_i), len(list_j))
            list_i = list_i[:min_list_length]
            list_j = list_j[:min_list_length]
            Kappas.append( (columns_of_interest[i], columns_of_interest[j], cohen_kappa_score(list_i, list_j) ) )

    # Sort it by the Kappas
    Kappas = sorted(Kappas, key=lambda x: x[2], reverse=True)

    # Save it as a json file
    with open("Kappas.json", 'w') as json_file:
        json.dump(Kappas, json_file)


# Find the alphas
def calculate_alphas():
    # Get all the values
    values = pd.read_csv("triplets.csv")

    # Define the columns we want to look at
    columns_of_interest = ["Emily", "Alessio", "ChatGPT 3.5", "ChatGPT 4 (Prompted with 1)", "ChatGPT 4 (Prompted with 2)"]

    # Select only columns of interest and transpose the dataframe
    values = values[columns_of_interest].T

    # Convert dataframe to a list of lists
    values_list = values.values.tolist()

    # Calculate Krippendorff's alpha
    alpha_value = alpha(values_list)

    # Save it as a json file
    with open("Alphas_no_human.json", 'w') as json_file:
        json.dump(alpha_value, json_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    calculate_kappas()
    calculate_alphas()

