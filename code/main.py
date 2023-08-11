import subprocess
from preprocessing import main as preprocessing_main

# Run the data producer script
subprocess.run(['python', 'data_producer.py'])

# Run the data cleaning script
subprocess.run(['python', 'data_cleaning.py'])
if __name__ == '__main__':
    preprocessing_main()
subprocess.run(["python", "-m", "http.server"])