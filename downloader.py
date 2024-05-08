import re
import os
import glob
import json
import shutil
import warnings
import threading
import sec_parser as sp
from bs4 import BeautifulSoup
from sec_edgar_downloader import Downloader

dl = Downloader("VIP Georgia Institute of Technology", "pmehta305@gatech.edu")

def download_10k(ticker, start_year=1995, current_year=2023):
    try:
        dl.get("10-K", ticker, after=f"{start_year}-01-01", before=f"{current_year}-12-31",download_details=True)
    except Exception as e:
        print(f"Failed to download 10-K. Exception: {e}")

def download_10k_threaded(ticker, start_year=1995, current_year=2023):
    threads = []

    def download_year(year):
        try:
            dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31", download_details=True)
        except Exception as e:
            print(f"Failed to download 10-K for {ticker} in {year}. Exception: {e}")

    for year in range(start_year, current_year + 1):
        thread = threading.Thread(target=download_year, args=(year,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def get_file_paths(ticker):
    html_files = []
    directory = f"sec-edgar-filings/{ticker}/10-K/"
    html_files = glob.glob(os.path.join(directory, "*", "primary-document.html"))
    non_html_files = glob.glob(os.path.join(directory, "*", "primary-document"))
    all_files = html_files + non_html_files
    return all_files

def remove_html_tags(input_file_path):
    # Read the HTML file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text from the HTML
    text = soup.get_text()

    # Create a new filename for the cleaned HTML file
    filename, extension = os.path.splitext(os.path.basename(input_file_path))
    year = int(input_file_path[input_file_path.index("10-K/") + 16: input_file_path.index("10-K/") + 18])
    if (int(year) < 25 ):
        year += 2000
    else:
        year += 1900
    cleaned_filename = filename +"-" + str(year) +"_cleaned.txt"

    # Write the cleaned text to a new file
    output_file_path = os.path.join(os.path.dirname(input_file_path), cleaned_filename)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    # print(f"Cleaned HTML saved to: {output_file_path}")

def cleaned_data_files(ticker, root_dir="."):
    # Create a new folder named "data"
    data_folder_path = os.path.join(root_dir, f"data-{ticker}")
    os.makedirs(data_folder_path, exist_ok=True)

    # Keep track of copied files
    copied_files = set()

    # Traverse through the directory tree
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Check if the file ends with "_cleaned.txt"
            if file.endswith("_cleaned.txt"):
                # Get the full path of the cleaned file
                cleaned_file_path = os.path.join(root, file)

                # Check if the file has already been copied
                if cleaned_file_path not in copied_files:
                    # Construct the destination path
                    destination_file_path = os.path.join(data_folder_path, file)
                    
                    # Check if the destination file exists and is not the same as the source file
                    if not os.path.exists(destination_file_path) or not os.path.samefile(cleaned_file_path, destination_file_path):
                        # Copy the cleaned file to the "data" folder
                        shutil.copy(cleaned_file_path, data_folder_path)
                        # Add the file to the set of copied files
                        copied_files.add(cleaned_file_path)

    print("Cleaned files copied to 'data' folder.")

def delete_sec_edgar_folder(root_dir="."):

    sec_edgar_filing_folder = os.path.join(root_dir, "sec-edgar-filings")

    # Check if the folder exists
    if os.path.exists(sec_edgar_filing_folder):
        # Delete the folder and all its contents
        shutil.rmtree(sec_edgar_filing_folder)
        print("sec-edgar-filings folder and its contents have been deleted.")
    else:
        print("sec-edgar-filings folder does not exist.")

def parse_10k(html_path):

    parser = sp.Edgar10QParser()
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Invalid section type for")
            elements = parser.parse(html_content)
    tree = sp.TreeBuilder().build(elements)
    print(elements)
    # print(tree.render())

    return tree

def get_cik_number_from_file(ticker):
    # Open the JSON file
    with open('assets/company_tickers.json', 'r') as file:
        data = json.load(file)

    # Searching for the ticker in the JSON data
    for _, company_info in data.items():
        if company_info['ticker'] == ticker:
            return company_info['cik_str']

    # If the ticker is not found, return None
    return None

def get_all_paths(directory):

    file_paths = []  
    for root, dirs, files in os.walk(directory):
        for file in files:

            filepath = os.path.join(root, file)
            file_paths.append(filepath)
    
    return file_paths

def get_files(ticker, start_year= 1995, current_year=2023):

    download_10k_threaded(ticker, start_year,current_year=current_year)
    html_paths = get_file_paths(ticker)
    for path in html_paths:
        remove_html_tags(path)

    cleaned_data_files(ticker)
    delete_sec_edgar_folder()