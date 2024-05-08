import streamlit as st
from main import generate_vis
import os
import shutil

"""
This Streamlit application serves as an SEC 10-K AI Analyser. It allows users to enter a ticker symbol 
of a company, and then displays an image that represents the analysis output of the SEC 10-K filings 
for that company. The application aims to provide a user-friendly interface for financial analysts 
and investors interested in understanding corporate fundamentals through automated analysis.
"""

# Set the title of the webpage
st.title('SEC 10-K AI Analyser')

# Input for ticker symbol
user_input_value = st.text_input("Enter TICKER SYMBOL:", help="Type the ticker symbol of the company and press Enter.")

# Add a slider for selecting year
start_year, end_year = st.slider("Select Year", 1995, 2023, (1995, 2023))


# Button to trigger the analysis
if st.button("Generate Analysis", key="generate_button",use_container_width=True):
    st.write("Analyzing...")
    progress_bar = st.progress(0)
    
    # Execute the generate_vis function
    text_response = generate_vis(user_input_value, start_year, end_year)
    
    # Update the placeholder with the final image upon completion
    st.image("vis.png", caption="Analysis complete!")
    st.text(text_response)
    
    st.button("Done", key="done_button",use_container_width=True)

# Check if the Done button is pressed after analysis
if 'done_button' in st.session_state and st.session_state.done_button:
    # Remove the data-META folder and vis.png file
    if os.path.exists(f"data-{user_input_value}"):
        shutil.rmtree(f"data-{user_input_value}")
    if os.path.exists("vis.png"):
        os.remove("vis.png")
    st.success("Cleanup successful!")
    st.session_state.done_button = False  # Reset the button state

    if st.button("Done", key="Done",use_container_width=True):
        print("Application done")