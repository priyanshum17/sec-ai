from downloader import get_files
from visualisation import get_vis

def generate_vis(ticker, start_year, current_year):
    get_files(ticker=ticker, start_year=start_year, current_year=current_year)
    text_response = get_vis(ticker)
    return text_response