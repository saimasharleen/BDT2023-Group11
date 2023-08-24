import subprocess
from data_analysis_spark import analyze_data
from data_cleaning import clean_data
from data_producer import produce_data
from preprocessing import preprocess_data
from restful_api import start_api_server
from restful_api import write_data


def main():
    # Call functions/methods from other script
    start_api_server()
    write_data()
    data = produce_data()
    cleaned_data = clean_data(data)
    preprocessed_data = preprocess_data(cleaned_data)
    analysis_result = analyze_data(preprocessed_data)
    

if __name__ == '__main__':
    # Run the data producer script
    subprocess.run(['python', 'data_producer.py'])

    # Run the data cleaning script
    subprocess.run(['python', 'data_cleaning.py'])

    # Run the preprocessing and analysis
    main()

    # Start a simple HTTP server for serving
    subprocess.run(["python", "-m", "http.server", "8000"])
