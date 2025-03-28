import streamlit as st
import hashlib

# Initialize an empty hospital ledger (a dictionary where keys are patient names)
hospital_ledger_advanced = {}

# Function to generate a hash for the visit record
def generate_hash(patient_name, treatment, cost, date_of_visit):
    # Combine all data to form a string for hashing
    visit_data = f"{patient_name}{treatment}{cost}{date_of_visit}"
    
    # Create a hash object using SHA-256
    return hashlib.sha256(visit_data.encode()).hexdigest()

# Function to add or update patient visits (optimized)
def add_patient_visit_advanced():
    # Get patient details from the user via Streamlit inputs
    patient_name = st.text_input("Enter the patient's name: ").lower()
    treatment = st.text_input("Enter the treatment received: ")
    cost = st.number_input("Enter the cost of the treatment: $", min_value=0.0)
    date_of_visit = st.date_input("Enter the date of visit: ")

    if st.button("Add Visit"):
        if patient_name and treatment and cost > 0 and date_of_visit:
            # Check if the patient already exists
            if patient_name in hospital_ledger_advanced:
                st.write(f"Updating visit record for {patient_name}.")
            else:
                st.write(f"Adding new visit record for {patient_name}.")

            # Generate a hash for this visit record
            visit_hash = generate_hash(patient_name, treatment, cost, str(date_of_visit))

            # Create a dictionary for the visit with the hash
            visit = {
                "treatment": treatment,
                "cost": cost,
                "date_of_visit": str(date_of_visit),
                "visit_hash": visit_hash  # Store the hash to verify data integrity
            }

            # Add the visit to the patient's list of visits (using a dictionary)
            if patient_name not in hospital_ledger_advanced:
                hospital_ledger_advanced[patient_name] = []

            hospital_ledger_advanced[patient_name].append(visit)

            # Display the confirmation message
            st.write(f"Visit added for {patient_name} on {date_of_visit} for treatment {treatment} costing ${cost}.")
            st.write(f"Visit hash: {visit_hash}")
        else:
            st.write("Please fill out all fields with valid information.")

# Function to search for patient visit records
def search_patient_visit():
    search_patient = st.text_input("Enter patient name to search for: ").lower()

    if st.button("Search"):
        if search_patient in hospital_ledger_advanced:
            st.write(f"Visit records for {search_patient}:")
            for visit in hospital_ledger_advanced[search_patient]:
                st.write(f"  Treatment: {visit['treatment']}, Cost: ${visit['cost']}, Date: {visit['date_of_visit']}, Hash: {visit['visit_hash']}")
        else:
            st.write(f"Patient {search_patient} not found in the ledger.")

# Streamlit app layout
st.title("Hospital Ledger System")
st.write("Manage patient visits and search visit records")

# Section to add patient visit
add_patient_visit_advanced()

# Section to search for a patient's visit record
search_patient_visit()
