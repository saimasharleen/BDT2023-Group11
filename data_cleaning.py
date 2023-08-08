import pandas as pd

def clean_data(data):
    # Step 1: Handling Duplicates (if any)
    data.drop_duplicates(inplace=True)

    # Step 2: Data Type Conversion (if needed)
    data['FromNodeId'] = data['FromNodeId'].astype(int)
    data['ToNodeId'] = data['ToNodeId'].astype(int)

    # Step 3: Dealing with Missing Values (if any)
    # If there are missing values, you can choose to drop them or fill them with appropriate values
    # For this example, let's assume there are no missing values

    # Step 4: Return the cleaned data
    return data
