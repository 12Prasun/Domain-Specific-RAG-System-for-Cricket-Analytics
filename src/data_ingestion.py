import os
import urllib.request
import zipfile

def download_and_extract_cricsheet_data(url: str, extract_to: str):
    """
    Downloads a zip file from Cricsheet and extracts it to the specified directory.
    """
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
        
    zip_path = os.path.join(extract_to, "data.zip")
    
    print(f"Downloading data from {url}...")
    urllib.request.urlretrieve(url, zip_path)
    
    print(f"Extracting data to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        
    print("Cleaning up...")
    os.remove(zip_path)
    print("Data ingestion complete.")

if __name__ == "__main__":
    # Example: downloading T20s JSON data
    # You can change this URL to other datasets provided by cricsheet
    CRICSHEET_URL = "https://cricsheet.org/downloads/t20s_json.zip"
    RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
    
    download_and_extract_cricsheet_data(CRICSHEET_URL, RAW_DATA_DIR)
