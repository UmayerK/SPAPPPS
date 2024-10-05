import pandas as pd
import os

def clean_data(input_file, output_dir, keep_fraction):
    # Read the original CSV file
    df = pd.read_csv(input_file)
    
    # Calculate the step size based on the keep_fraction
    step = int(1 / keep_fraction)
    
    # Keep every nth line
    df_cleaned = df.iloc[::step].reset_index(drop=True)
    
    # Get the next available file number
    file_number = 1
    while os.path.exists(os.path.join(output_dir, f'cleaned file number {file_number}.csv')):
        file_number += 1
    
    # Generate filename for cleaned data
    cleaned_csv_file = os.path.join(output_dir, f'cleaned file number {file_number}.csv')
    
    # Save the cleaned data to a new CSV file
    df_cleaned.to_csv(cleaned_csv_file, index=False)
    
    print(f"Cleaned data saved to: {cleaned_csv_file}")
    
    return cleaned_csv_file

# Get the paths
backend_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(backend_dir, 'output')

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the input file path (you can modify this as needed)
input_file = './data/lunar/training/data/S12_GradeA/xa.s12.00.mhz.1970-01-19HR00_evid00002.csv'

# Clean the data
keep_fraction = 1/5  # Keep every 5th item (delete 4/5)

cleaned_csv_file = clean_data(input_file, output_dir, keep_fraction)

print(f"Cleaned data saved to: {cleaned_csv_file}")