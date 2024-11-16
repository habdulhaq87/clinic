import streamlit as st
import pandas as pd
import os

# Define the path to your data file
DATA_PATH = os.path.join(os.path.dirname(__file__), "clinic.csv")

# Load the dataset
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df["Cost"] = df["Cost"].str.replace("$", "").astype(float)  # Convert cost to float
        return df
    else:
        st.error(f"Data file not found at {DATA_PATH}. Please ensure the file exists.")
        st.stop()

# Append a new record to the CSV file
def append_to_csv(new_record):
    try:
        st.write("Debug: Attempting to append record to CSV...")
        st.write(f"CSV File Path: {DATA_PATH}")
        new_record.to_csv(DATA_PATH, mode='a', header=False, index=False)
        st.success("Record has been successfully added to the CSV file!")
    except Exception as e:
        st.error(f"An error occurred while writing to the CSV file: {e}")

# Main Streamlit app
def main():
    st.sidebar.title("Dental Clinic Dataroom")

    # Load data
    df = load_data()

    # Navigation options
    options = ["Add New Record"]
    choice = st.sidebar.radio("Select a page", options)

    if choice == "Add New Record":
        st.write("## Add New Appointment Record")

        with st.form("add_record_form", clear_on_submit=True):
            patient_id = st.text_input("Patient ID", placeholder="E.g., P005")
            name = st.text_input("Patient Name", placeholder="E.g., John Doe")
            contact = st.text_input("Contact Number", placeholder="E.g., 123-456-7890")
            appointment_date = st.date_input("Appointment Date")
            time = st.time_input("Appointment Time")
            dentist = st.text_input("Dentist", placeholder="E.g., Dr. Smith")
            procedure = st.text_input("Procedure", placeholder="E.g., Cleaning")
            tooth_teeth = st.text_input("Tooth/Teeth Treated", placeholder="E.g., Upper Left Molar")
            cost = st.number_input("Cost ($)", min_value=0.0, step=0.1)
            payment_status = st.selectbox("Payment Status", ["Paid", "Unpaid", "Partial"])

            # Submit button
            submitted = st.form_submit_button("Add Record")
            if submitted:
                new_record = pd.DataFrame([{
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
                }])

                # Append the new record directly to the CSV
                append_to_csv(new_record)

if __name__ == "__main__":
    main()
