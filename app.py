import streamlit as st
import pandas as pd
import json
from github import Github

# GitHub Repository Configuration
GITHUB_TOKEN = st.secrets["github"]["token"]  # Use Streamlit secrets for the GitHub token
REPO_NAME = "habdulhaq87/clinic"
FILE_PATH = "clinic.json"  # Path to the JSON file in the repository
BRANCH_NAME = "main"

# Initialize GitHub API
try:
    github = Github(GITHUB_TOKEN)
    repo = github.get_repo(REPO_NAME)
except Exception as e:
    st.error(f"Error initializing GitHub API: {e}")
    st.stop()

# Load the dataset from GitHub
@st.cache_data
def load_data():
    try:
        # Fetch the JSON file content from GitHub
        file = repo.get_contents(FILE_PATH, ref=BRANCH_NAME)
        data = json.loads(file.decoded_content.decode())
        df = pd.DataFrame(data)

        # Ensure 'Cost' column is numeric and clean any formatting
        if "Cost" in df.columns:
            df["Cost"] = df["Cost"].replace('[\$,]', '', regex=True).astype(float)

        return df
    except Exception as e:
        st.error(f"Error fetching data from GitHub: {e}")
        st.stop()

# Append a new record to the GitHub JSON file
def append_to_github(new_record):
    try:
        # Fetch the existing file from GitHub
        file = repo.get_contents(FILE_PATH, ref=BRANCH_NAME)
        data = json.loads(file.decoded_content.decode())

        # Append the new record
        data.append(new_record.to_dict(orient="records")[0])

        # Update the file in GitHub
        repo.update_file(
            path=FILE_PATH,
            message="Update clinic.json via Streamlit",
            content=json.dumps(data, indent=4),
            sha=file.sha,
            branch=BRANCH_NAME,
        )
        st.success("Record has been successfully added to GitHub!")
    except Exception as e:
        st.error(f"Error writing data to GitHub: {e}")

# Main Streamlit app
def main():
    st.sidebar.title("Dental Clinic Dataroom")

    # Load data
    df = load_data()

    # Navigation options
    options = ["Dashboard", "View Records", "Add New Record", "Search Appointments", "Statistics"]
    choice = st.sidebar.radio("Select a page", options)

    if choice == "Dashboard":
        st.write("## Welcome to the Dental Clinic Dataroom!")
        st.markdown("Use the sidebar to navigate through the app.")

    elif choice == "View Records":
        st.write("## Patient Records")
        
        # Display the records in a table
        if df.empty:
            st.warning("No records found in the JSON file.")
        else:
            st.dataframe(df)

        # Add download button for the JSON file
        st.download_button(
            label="Download Records as JSON",
            data=json.dumps(df.to_dict(orient="records"), indent=4),
            file_name="clinic_records.json",
            mime="application/json",
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

            submitted = st.form_submit_button("Add Record")
            if submitted:
                # Create a new record as a DataFrame
                new_record = pd.DataFrame([{
                    "Patient ID": patient_id,
                    "Name": name,
                    "Contact": contact,
                    "Appointment Date": appointment_date.strftime("%Y-%m-%d"),
                    "Time": time.strftime("%H:%M:%S"),
                    "Dentist": dentist,
                    "Procedure": procedure,
                    "Tooth/Teeth": tooth_teeth,
                    "Cost": f"${cost:,.2f}",
                    "Payment Status": payment_status,
                }])

                # Append the new record directly to GitHub
                append_to_github(new_record)

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

if __name__ == "__main__":
    main()
