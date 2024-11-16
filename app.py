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
                "Cost": cost,
                "Payment Status": payment_status
            }])

            # Concatenate the new record with the existing DataFrame
            df = pd.concat([df, new_record], ignore_index=True)

            # Save updated DataFrame back to CSV
            save_data(df)

            # Display success message
            st.success(f"Record for {name} added successfully!")
