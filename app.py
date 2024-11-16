import streamlit as st
import pandas as pd
import os

# Define the path to your data file
DATA_PATH = os.path.join(os.path.dirname(__file__), "clinic.csv")

# Load the dataset
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        # Load and clean the data
        df = pd.read_csv(DATA_PATH)
        df["Cost"] = df["Cost"].str.replace("$", "").astype(float)  # Convert cost to float
        return df
    else:
        st.error(f"Data file not found at {DATA_PATH}. Please ensure the file exists.")
        st.stop()

# Save the updated dataset
def save_data(df):
    df.to_csv(DATA_PATH, index=False)
    st.success("Data has been successfully saved!")

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
        use_container_width=True
    )

    # Load data
    df = load_data()

    # Navigation options
    options = ["Dashboard", "View Records", "Add New Record", "Search Appointments", "Statistics"]
    choice = st.sidebar.radio("Select a page", options)

    if choice == "Dashboard":
        st.write("## Welcome to the Dental Clinic Dataroom!")
        st.markdown(
            """
            Use the sidebar to navigate through the app. Features include:
            - Viewing and searching patient records.
            - Adding new patient appointments.
            - Viewing clinic statistics.
            """
        )
        st.image("https://via.placeholder.com/600x300.png?text=Clinic+Dashboard", use_container_width=True)

    elif choice == "View Records":
        st.write("## Patient Records")
        st.dataframe(df)

        # Add download button
        st.download_button(
            label="Download Data as CSV",
            data=df.to_csv(index=False),
            file_name="clinic_records.csv",
            mime="text/csv",
        )

    elif choice == "Add New Record":
        st.write("## Add New Appointment Record")

        with st.form("add_record_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID", placeholder="E.g., P005")
                name = st.text_input("Patient Name", placeholder="E.g., John Doe")
                contact = st.text_input("Contact Number", placeholder="E.g., 123-456-7890")
                appointment_date = st.date_input("Appointment Date")
                time = st.time_input("Appointment Time")
            with col2:
                dentist = st.text_input("Dentist", placeholder="E.g., Dr. Smith")
                procedure = st.text_input("Procedure", placeholder="E.g., Cleaning")
                tooth_teeth = st.text_input("Tooth/Teeth Treated", placeholder="E.g., Upper Left Molar")
                cost = st.number_input("Cost ($)", min_value=0.0, step=0.1)
                payment_status = st.selectbox("Payment Status", ["Paid", "Unpaid", "Partial"])

            # Submit button
            submitted = st.form_submit_button("Add Record")
            if submitted:
                # Append new record to the DataFrame
                new_record = {
                    "Patient ID": patient_id,
                    "Name": name,
                    "Contact": contact,
                    "Appointment Date": appointment_date.strftime("%Y-%m-%d"),
                    "Time": time.strftime("%H:%M:%S"),
                    "Dentist": dentist,
                    "Procedure": procedure,
                    "Tooth/Teeth": tooth_teeth,
                    "Cost": cost,
                    "Payment Status": payment_status
                }
                df = df.append(new_record, ignore_index=True)
                save_data(df)
                st.success(f"Record for {name} added successfully!")

    elif choice == "Search Appointments":
        st.write("## Search Appointments")

        # Search by Patient Name
        search_name = st.text_input("Search by Patient Name", placeholder="Enter patient name...")
        if search_name:
            filtered_data = df[df["Name"].str.contains(search_name, case=False, na=False)]
            if not filtered_data.empty:
                st.success(f"Found {len(filtered_data)} record(s) for '{search_name}'")
                st.dataframe(filtered_data)
            else:
                st.warning(f"No records found for '{search_name}'")

        # Filter by Appointment Date
        search_date = st.date_input("Filter by Appointment Date")
        if search_date:
            filtered_date = df[df["Appointment Date"] == search_date.strftime("%Y-%m-%d")]
            if not filtered_date.empty:
                st.success(f"Found {len(filtered_date)} appointment(s) on {search_date}")
                st.dataframe(filtered_date)
            else:
                st.warning(f"No appointments found on {search_date}")

    elif choice == "Statistics":
        st.write("## Clinic Statistics")

        # Total Patients
        total_patients = df["Patient ID"].nunique()
        st.metric(label="Total Patients", value=total_patients)

        # Total Revenue
        total_revenue = df["Cost"].sum()
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")

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

