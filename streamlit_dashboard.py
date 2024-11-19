import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title('Data Visualization App')

# Define file path and load data
file_path = "/content/DataProject.xlsx"

# Load the database
try:
    data = pd.read_excel(file_path, sheet_name="Table A1")
except Exception as e:
    st.error("Failed to load data. Please check the file path and sheet name.")
    st.stop()

# Custom CSS for styling
st.markdown("""
    <style>
        .navbar {
            display: flex;
            justify-content: center;
            gap: 1.5em;
            margin-top: 20px;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
        }
        .nav-item {
            padding: 10px 20px;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            background-color: rgba(255, 255, 255, 0.2);
            cursor: pointer;
        }
        .nav-item.active {
            background-color: #4a3fdb;
        }
        .nav-item:hover {
            background-color: rgba(255, 255, 255, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Navigation bar with simpler logic for page selection
page = st.sidebar.radio("Select Page", ["Overview", "Consumption Trends", "Energy Sources"])

# Display content based on the selected page
if page == "Overview":
    st.markdown("<h1 class='title'>Overview of Dataset</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>General overview and summary statistics</p>", unsafe_allow_html=True)
    st.write("This section provides a high-level overview of the dataset and its key variables.")

    # Display dataset preview
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Summary statistics
    st.write("### Summary Statistics")
    st.write(data.describe())

elif page == "Consumption Trends":
    st.markdown("<h1 class='title'>Consumption Trends</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Analyzing trends over different years</p>", unsafe_allow_html=True)

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
        ax.pie(data['% consume'].dropna(), labels=data['Description'], autopct='%1.1f%%', startangle=140,
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
    st.markdown("<h1 class='title'>Energy Sources</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Analysis of energy contribution by source</p>", unsafe_allow_html=True)

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
