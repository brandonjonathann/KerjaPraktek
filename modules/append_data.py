import pandas as pd

def append_data_to_database(file_path: str):
    """
    Append data from a CSV file to the corresponding 
    database folder based on 'nomor_kandang'.

    Args:
        file_path (str): The path to the CSV file containing the data.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        PermissionError: If there's a permission issue while accessing the file.
        Exception: For other unexpected errors.
    """
    
    try: 

        # Read data from the file.
        csv_dataframe = pd.read_csv(file_path, header = None)

        # Loop through every row of the dataframe.
        for row_index, row in csv_dataframe.iterrows():

            # Locate 'nomor_kandang' of each row.
            nomor_kandang = row[0]

            # Locate the database file for 'nomor_kandang'.
            database_path = f'database/R{nomor_kandang}'

            # Append data to the respective 'kandang'.
            with open(database_path, 'a') as database_file:
                row.to_csv(database_file, mode = 'a',index = False, header = False)

    except FileNotFoundError as e:
        print(f"Error: the file '{file_path}' was not found.")
    except PermissionError as e:
        print(f"Error: Permission denied while accessing '{file_path}'.")
    except Exception as e:
        print(f"Error: An error '{e}' occurred.")