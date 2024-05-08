# SEC 10-K AI Analyser

## Overview
This project uses natural language processing (NLP) to analyze SEC 10-K filings. It extracts significant entities and trends from these documents, presenting them visually in a word cloud. This allows users, especially financial analysts and investors, to quickly gather insights into corporate fundamentals through a streamlined web interface.

## Tech Stack

- **Python**: Chosen for its robust library ecosystem and support for data manipulation and NLP.
- **spaCy**: A powerful and efficient library for NLP in Python. We use it to process text and extract entities because of its speed and accuracy.
- **Streamlit**: Utilized for quickly building interactive web applications. It is user-friendly and allows for easy integration of Python code.
- **matplotlib**: A plotting library that we use to generate visual representations of data (word clouds in this case).
- **WordCloud**: This library is used to generate word clouds from text, a visual method to highlight key terms and trends.
- **JSON**: Facilitates data storage and transfer between functions and APIs.
- **Together AI**: Provides a powerful language model to extract relevant words from texts, enhancing our text analysis capabilities.


## How the SEC 10-K AI Analyser Works

The **SEC 10-K AI Analyser** operates by initially gathering and reading SEC 10-K filings from a specified time period for a given company ticker. This process involves dynamically downloading and storing files for later use.

### Text Processing and Entity Extraction

Once the necessary documents are acquired, the main computational work begins. The system uses **spaCy**, a Natural Language Processing (NLP) library, to efficiently process the text data. spaCy is particularly adept at identifying and extracting specific types of entities such as `PERSON`, `EVENT`, `PRODUCT`, and `LAW` from the texts. This step is critical as it helps pinpoint relevant information within the vast amounts of data contained in the 10-K filings, making the data manageable and meaningful.

### Keyword Extraction and Visualization

After the entity extraction, the system utilizes a client-server architecture to interact with an AI model hosted by the **Together AI API**. This model's task is to identify and extract the top 100 most relevant keywords from the compiled list of entities. These keywords are specifically chosen to reflect unique aspects and significant elements relating to the company's operations and its industry context.

### Visualization and User Interaction

Once the important words are identified, they are visualized using a **WordCloud**. This visualization creates a graphic representation of the data, where the size of each word indicates its frequency or importance. Such visualization aids users in quickly discerning key themes and significant points of interest from the company's filings.

The word cloud is then displayed through a user-friendly **Streamlit** web interface. This interface allows users to specify the ticker and time frame for the analysis. Designed to be interactive, the system provides users with both visual and textual insights into the analyzed data, enhancing the decision-making process for financial analysts and investors.


## Installation

To set up this project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd <project-folder>
pip install -r requirements.txt
