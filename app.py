import streamlit as st
import pandas as pd

# Load the dataset
def load_data():
    return pd.read_csv('clinic.csv')

# Main Streamlit app
def main():
    st.title("Dental Clinic Dataroom")
    st.sidebar.title("Navigation")
    
    # Load data
    df = load_data()
    
    # Navigation options
    options = ["Home", "View Data", "Search Appointments", "Statistics"]
    choice = st.sidebar.selectbox("Select a page", options)
    
    if choice == "Home":
        st.write("### Welcome to the Dental Clinic Dataroom!")
        st.write("Use the sidebar to navigate through the app.")
        st.write("""
        **Features:**
        - View and explore patient data
        - Search for specific appointments
        - View simple statistics
        """)

    elif choice == "View Data":
        st.write("### Clinic Data")
        st.dataframe(df)

    elif choice == "Search Appointments":
        st.write("### Search Appointments")
        
        # Search by Patient Name
        search_name = st.text_input("Enter Patient Name to Search")
        if search_name:
            filtered_data = df[df["Name"].str.contains(search_name, case=False, na=False)]
            if not filtered_data.empty:
                st.dataframe(filtered_data)
            else:
                st.write("No results found.")
        
        # Filter by Date
        search_date = st.date_input("Select Appointment Date")
        if search_date:
            filtered_date = df[df["Appointment Date"] == search_date.strftime("%Y-%m-%d")]
            if not filtered_date.empty:
                st.dataframe(filtered_date)
            else:
                st.write("No appointments found on this date.")
    
    elif choice == "Statistics":
        st.write("### Statistics")
        
        # Total Patients
        total_patients = df["Patient ID"].nunique()
        st.metric(label="Total Patients", value=total_patients)
        
        # Total Revenue
        total_revenue = df["Cost"].str.replace("$", "").astype(float).sum()
        st.metric(label="Total Revenue", value=f"${total_revenue}")
        
        # Payment Status Summary
        st.write("#### Payment Status Distribution")
        payment_status = df["Payment Status"].value_counts()
        st.bar_chart(payment_status)

if __name__ == "__main__":
    main()
