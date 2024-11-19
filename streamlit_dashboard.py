import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title('Data Visualization App')

# Define file path and load data
file_path = "DataProject.csv"

# Load the database
try:
    data = pd.read_csv(file_path)
except Exception as e:
    st.error("Failed to load data. Please check the file path.")
    st.stop()

# Display the data
st.write(data)

# Custom CSS for styling
st.markdown("""
    
""", unsafe_allow_html=True)

# Navigation bar with simpler logic for page selection
page = st.sidebar.radio("Select Page", ["Overview", "Consumption Trends", "Energy Sources"])

# Display content based on the selected page
if page == "Overview":
    st.markdown("Overview of Dataset", unsafe_allow_html=True)
    st.markdown("General overview and summary statistics", unsafe_allow_html=True)
    st.write("This section provides a high-level overview of the dataset and its key variables.")

    # Display dataset preview
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Summary statistics
    st.write("### Summary Statistics")
    st.write(data.describe())

elif page == "Consumption Trends":
    st.markdown("Consumption Trends", unsafe_allow_html=True)
    st.markdown("Analyzing trends over different years", unsafe_allow_html=True)

    # Layout for charts in two columns
    col1, col2 = st.columns(2)

    # First chart - Bar chart of Energy Contribution (1992)
    with col1:
        st.markdown("#### Energy Contribution by Beverage Type (1992)")
        fig, ax = plt.subplots()
        data.plot(kind='bar', x='Description', y='Per capita 1992', ax=ax, color='#1f77b4')
        ax.set_ylabel("Energy (kJ/day)")
        ax.set_xlabel("Beverage Type")
        st.pyplot(fig)

    # Second chart - Pie chart of % Consumption in 1992
    with col2:
        st.markdown("#### Percentage Consumption by Beverage Type (1992)")
        fig, ax = plt.subplots()

        # Ensure '% consume' column is numeric
        data['% consume'] = pd.to_numeric(data['% consume'], errors='coerce')

        # Drop NaN values
        data = data.dropna(subset=['% consume', 'Description'])

        # Check if data is empty after dropping NaN values
        if data.empty:
            st.error("No valid data available for the pie chart.")
        else:
            ax.pie(data['% consume'], labels=data['Description'], autopct='%1.1f%%', startangle=140,
                   colors=['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896'])
            st.pyplot(fig)

    # Third chart - Line chart comparing Per capita over years
    st.markdown("#### Consumption Trends Over Years")
    fig, ax = plt.subplots()
    data.plot(kind='line', x='Description',
              y=['Per capita 1992', 'Per capita 1997', 'Per capita 2008-2009', 'Per capita 2008-2009 (2)'], ax=ax)
    ax.set_ylabel("Per Capita Consumption")
    ax.set_xlabel("Beverage Type")
    st.pyplot(fig)

elif page == "Energy Sources":
    st.markdown("Energy Sources", unsafe_allow_html=True)
    st.markdown("Analysis of energy contribution by source", unsafe_allow_html=True)

    # Layout for charts in two columns
    col1, col2 = st.columns(2)

    # Fourth chart - Bar chart for Per Consumer in different years
    with col1:
        st.markdown("#### Per Consumer Consumption in Different Years")
        fig, ax = plt.subplots()
        data[['Description', 'Per consumer', 'Per consumer2', 'Per consumer3']].set_index('Description').plot(kind='bar', ax=ax)
        ax.set_ylabel("Per Consumer Consumption")
        ax.set_xlabel("Beverage Type")
        st.pyplot(fig)

    # Example chart for Energy Sources page (Total Energy)
    with col2:
        st.markdown("### Total Energy from Sources (Example Chart)")
        fig, ax = plt.subplots()
        if "Per capita 1992" in data.columns:
            ax.bar(data["Description"], data["Per capita 1992"], color='#1f77b4')
            ax.set_ylabel("Total Energy (kJ/day)")
            ax.set_xlabel("Description")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.error("Column 'Per capita 1992' not found in the dataset. Please check the column name.")
