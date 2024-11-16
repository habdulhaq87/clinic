import streamlit as st
import pandas as pd
import os

# Define the path to your data file
DATA_PATH = os.path.join(os.path.dirname(__file__), "clinic.csv")

# Load the dataset
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        st.error(f"Data file not found at {DATA_PATH}. Please ensure the file exists.")
        st.stop()

# Styling the app
st.set_page_config(page_title="Dental Clinic Dataroom", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #343a40;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Streamlit app
def main():
    st.sidebar.title("Dental Clinic Dataroom")
    st.sidebar.image(
        "https://via.placeholder.com/150x150.png?text=Clinic+Logo", 
        use_column_width=True,
    )

    # Load data
    df = load_data()

    # Navigation options
    options = ["Home", "Patient Records", "Search Appointments", "Statistics"]
    choice = st.sidebar.radio("Select a page", options)

    if choice == "Home":
        st.write("## Welcome to the Dental Clinic Dataroom!")
        st.markdown(
            """
            This platform helps you manage patient data, track appointments, and visualize clinic statistics.
            - **View patient records**: See a detailed view of patient appointments and treatments.
            - **Search appointments**: Quickly find appointments by name or date.
            - **Statistics**: Get insights into clinic performance and trends.
            """
        )
        st.image("https://via.placeholder.com/600x300.png?text=Clinic+Dashboard", use_column_width=True)

    elif choice == "Patient Records":
        st.write("## Patient Records")
        st.dataframe(df.style.format({"Cost": "${:.2f}"}))

        # Add download button
        st.download_button(
            label="Download Data as CSV",
            data=df.to_csv(index=False),
            file_name="clinic_records.csv",
            mime="text/csv",
        )

    elif choice == "Search Appointments":
        st.write("## Search Appointments")

        # Search by Patient Name
        search_name = st.text_input("Search by Patient Name", placeholder="Enter patient name...")
        if search_name:
            filtered_data = df[df["Name"].str.contains(search_name, case=False, na=False)]
            if not filtered_data.empty:
                st.success(f"Found {len(filtered_data)} record(s) for '{search_name}'")
                st.dataframe(filtered_data.style.format({"Cost": "${:.2f}"}))
            else:
                st.warning(f"No records found for '{search_name}'")

        # Filter by Appointment Date
        search_date = st.date_input("Filter by Appointment Date")
        if search_date:
            filtered_date = df[df["Appointment Date"] == search_date.strftime("%Y-%m-%d")]
            if not filtered_date.empty:
                st.success(f"Found {len(filtered_date)} appointment(s) on {search_date}")
                st.dataframe(filtered_date.style.format({"Cost": "${:.2f}"}))
            else:
                st.warning(f"No appointments found on {search_date}")

    elif choice == "Statistics":
        st.write("## Clinic Statistics")

        # Total Patients
        total_patients = df["Patient ID"].nunique()
        st.metric(label="Total Patients", value=total_patients)

        # Total Revenue
        try:
            df["Cost"] = df["Cost"].str.replace("$", "").astype(float)
            total_revenue = df["Cost"].sum()
            st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
        except Exception as e:
            st.error("Error processing revenue data: " + str(e))

        # Payment Status Distribution
        st.write("### Payment Status Distribution")
        payment_status = df["Payment Status"].value_counts()
        st.bar_chart(payment_status)

        # Revenue by Procedure
        st.write("### Revenue by Procedure")
        revenue_by_procedure = df.groupby("Procedure")["Cost"].sum().sort_values(ascending=False)
        st.bar_chart(revenue_by_procedure)

if __name__ == "__main__":
    main()
