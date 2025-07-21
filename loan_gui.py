import tkinter as tk
from tkinter import messagebox
import numpy as np
import pickle

# Load the trained model
try:
    with open('loan_model.pkl', 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    messagebox.showerror("Error", f"Model could not be loaded:\n{e}")
    raise

def predict_loan_status():
    try:
        gender = int(entry_gender.get())
        married = int(entry_married.get())
        dependents = int(entry_dependents.get())
        education = int(entry_education.get())
        self_employed = int(entry_self_employed.get())
        applicant_income = float(entry_applicant_income.get())
        coapplicant_income = float(entry_coapplicant_income.get())
        loan_amount = float(entry_loan_amount.get())
        loan_term = float(entry_loan_term.get())
        credit_history = float(entry_credit_history.get())
        load_status = int(entry_load_status.get())  # 1 for Y, 0 for N

        # Encode property area (dummy variables)
        property_area_input = entry_property_area.get().lower()
        property_area_semiurban = 0
        property_area_urban = 0

        if property_area_input == "semiurban":
            property_area_semiurban = 1
        elif property_area_input == "urban":
            property_area_urban = 1
        # For rural, both remain 0

        # Final input features (13 total)
        features = np.array([[gender, married, dependents, education, self_employed,
                              applicant_income, coapplicant_income, loan_amount,
                              loan_term, credit_history, load_status,
                              property_area_semiurban, property_area_urban]])

        prediction = model.predict(features)

        result = "Loan Approved ✅" if prediction[0] == 1 else "Loan Rejected ❌"
        messagebox.showinfo("Prediction Result", result)

    except Exception as e:
        messagebox.showerror("Invalid input or error occurred", str(e))

# Tkinter GUI
root = tk.Tk()
root.title("Loan Approval Predictor")

# Define Labels & Entries
labels = ["Gender (1=Male, 0=Female)", "Married (1/0)", "Dependents (0/1/2/3)",
          "Education (1=Graduate, 0=Not)", "Self Employed (1/0)",
          "Applicant Income", "Coapplicant Income", "Loan Amount",
          "Loan Term", "Credit History (1/0)", "Load Status (1=Y, 0=N)",
          "Property Area (Urban/Semiurban/Rural)"]

entries = []

for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

# Assign entries to variables
(entry_gender, entry_married, entry_dependents, entry_education, entry_self_employed,
 entry_applicant_income, entry_coapplicant_income, entry_loan_amount,
 entry_loan_term, entry_credit_history, entry_load_status,
 entry_property_area) = entries

# Predict Button
predict_button = tk.Button(root, text="Predict Loan Approval", command=predict_loan_status)
predict_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

root.mainloop()
