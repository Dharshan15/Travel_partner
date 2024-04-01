import streamlit as st
import openai
import pandas as pd
import requests
import numpy as np

# Set up OpenAI API credentials
openai.api_key = "key"

# Set up OpenCage Geocoding API credentials
opencage_api_key = "key"

# Function to generate a travel plan using OpenAI
def generate_travel_plan(location, duration, budget, enjoyment_type, num_travelers):
    prompt = f"I want to travel to {location} for {duration} days with a budget of {budget} and enjoy {enjoyment_type}. We are {num_travelers} people. Please suggest an itinerary."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )
    plan = response.choices[0].text.strip()

    return plan

# Function to parse the travel plan and extract date, time, and activity
def parse_travel_plan(plan):
    # Split the plan by lines and extract date, time, and activity
    lines = plan.strip().split("\n")
    itinerary = []
    for line in lines:
        line_parts = line.split(" - ")
        if len(line_parts) == 2:
            date_time = line_parts[0].strip()
            activity = line_parts[1].strip()
            itinerary.append({"Date/Time": date_time, "Activity": activity})

    return itinerary

# Function to get the location of a place using OpenCage Geocoding API
def get_place_location(place_name):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={opencage_api_key}"
    response = requests.get(url).json()

    if response["total_results"] > 0:
        result = response["results"][0]
        location = result["formatted"]
    else:
        location = None

    return location

# Main page content
def main_page():
    st.title("Travel Planner AI")
    st.write("Enter your travel details below:")

    # User input form
    location = st.text_input("Enter the travel destination:")
    duration = st.number_input("Enter the duration of the trip (in days):", min_value=1, step=1)
    budget = st.number_input("Enter your travel budget:", min_value=0, step=1)
    enjoyment_type = st.text_input("Enter the type of enjoyment during the trip:")
    num_travelers = st.number_input("Enter the number of people traveling:", min_value=1, step=1)

    # Generate travel plan when user clicks the button
    if st.button("Generate Travel Plan"):
        if location and duration and budget and enjoyment_type and num_travelers:
            plan = generate_travel_plan(location, duration, budget, enjoyment_type, num_travelers)
            st.subheader("Travel Plan:")
            st.markdown(plan)

            # Parse the travel plan
            itinerary = parse_travel_plan(plan)

            # Create a DataFrame with the parsed data
            df = pd.DataFrame(itinerary)

            # Display the travel itinerary as a table
            st.subheader("Travel Itinerary:")
            st.table(df)

            # Validation based on enjoyment type
            if enjoyment_type.lower() in plan.lower():
                st.success("Enjoyment type validated!")
            else:
                st.warning("The generated plan may not align with the specified enjoyment type.")
        else:
            st.warning("Please enter the travel destination, duration, budget, enjoyment type, and number of travelers.")

# Daily Planner page content
def daily_planner():
    st.title("Daily Planner")
    st.write("Enter your daily activities below:")

    # User input form
    duration = st.session_state.duration
    daily_activities = []
    for day in range(1, duration + 1):
        activity = st.text_input(f"Day {day}:", key=f"activity_{day}")
        daily_activities.append(activity)

    # Display the daily activities as a table
    st.subheader("Daily Activities:")
    daily_df = pd.DataFrame({"Day": range(1, duration + 1), "Activity": daily_activities})
    st.table(daily_df)

# Location page content
def location_page():
    st.title("Place Location Finder")
    st.write("Enter the name of a place to find its location.")

    place_name = st.text_input("Enter the name of the place:")

    if st.button("Find Location"):
        if place_name:
            # Call the location API to get the location of the specified place
            location = get_place_location(place_name)

            # Display the location if found, or show a message if not found
            st.subheader("Location:")
            if location:
                st.write(location)
            else:
                st.warning("Location not found.")
        else:
            st.warning("Please enter the name of a place.")

# Streamlit web app
def main():
    st.set_page_config(page_title="Travel Planner AI")

    # Add page selection sidebar
    page = st.sidebar.selectbox("Page", ["Main", "Daily Planner", "Place Location Finder"])

    # Render selected page
    if page == "Main":
        main_page()
    elif page == "Daily Planner":
        daily_planner()
    elif page == "Place Location Finder":
        location_page()

if __name__ == "__main__":
    main()
