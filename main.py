from downloader import get_files
from visualisation import get_vis

def generate_vis(ticker, start_year, current_year):
    """
    Orchestrates the process of downloading files related to a specific ticker and 
    generating a visualization based on the content of these files.

    Args:
        ticker (str): The ticker symbol of the company for which to generate visual content.
        start_year (int): The starting year of the period for which the files are to be downloaded.
        current_year (int): The ending year of the period for which the files are to be downloaded.

    Returns:
        str: The textual response associated with the generated visualization.

    Description:
    This function integrates two major components: file downloading and visualization generation. 
    It first calls 'get_files' to handle the downloading of SEC filings or similar documents for the specified
    ticker within the given year range. Once the files are successfully downloaded and processed,
    it invokes 'get_vis' to create visual representations (e.g., word clouds) of the data contained in these files.

    Workflow:
    1. Invoke the 'get_files' function from the 'downloader' module. This function is responsible for fetching and
       processing the necessary files from a specified data source, such as the SEC EDGAR database, based on the 
       ticker symbol and the year range provided.
    2. Upon successful retrieval and processing of files, call the 'get_vis' function from the 'visualisation' module.
       This function generates a visual output, typically a word cloud, that represents key themes or concepts 
       extracted from the text of the downloaded files. This visual output is complemented by a textual response 
       that provides insights or summaries related to the visualized data.
    3. Return the textual response from the visualization process to the caller, which can be used for reporting 
       or further analysis.

    Usage:
    This function can be used in financial analysis, compliance monitoring, or market research to visually 
    and textually represent the thematic content of corporate filings over a specified period, offering 
    insights into trends, focuses, or shifts in business strategy or regulatory response.
    """
    # Download files for the specified ticker and year range.
    get_files(ticker=ticker, start_year=start_year, current_year=current_year)

    # Generate and retrieve the visual representation and textual analysis for the downloaded files.
    text_response = get_vis(ticker)
    return text_response
