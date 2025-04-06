import tkinter as tk
from tkinter import ttk, messagebox
import requests

def convert_currency():
    try:
        # Validate amount input
        amount = entry_amount.get()
        if not amount or not amount.replace('.', '', 1).isdigit():
            raise ValueError("Invalid amount entered.")
        amount = float(amount)

        # Validate selected currencies
        from_currency = combo_from.get()
        to_currency = combo_to.get()
        if not from_currency or not to_currency:
            raise ValueError("Please select both currencies.")

        # API Request
        api_key = "7dc9395e00960b6a28dcda51"
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}.")
        
        data = response.json()

        # Check if the response contains the expected data
        if "conversion_rates" not in data or to_currency not in data["conversion_rates"]:
            raise Exception("API response does not contain the conversion rate for the selected currency.")

        # Calculate and display result
        conversion_rate = data["conversion_rates"][to_currency]
        result = round(amount * conversion_rate, 2)
        label_result.config(text=f"{amount} {from_currency} = {result} {to_currency}")
    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))
    except requests.exceptions.RequestException as re:
        messagebox.showerror("Network Error", "Failed to connect to the API. Please check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# Currencies list (you can add more if you want)
currencies = ["USD", "EUR", "GBP", "JPY", "MAD", "CAD", "AUD", "CNY"]

# GUI Setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x300")
root.resizable(False, False)

# Title
tk.Label(root, text="Currency Converter", font=("Helvetica", 16, "bold")).pack(pady=10)

# Amount Entry
tk.Label(root, text="Amount:").pack()
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack(pady=5)

# From Currency
tk.Label(root, text="From:").pack()
combo_from = ttk.Combobox(root, values=currencies, state="readonly")
combo_from.set("USD")
combo_from.pack(pady=5)

# To Currency
tk.Label(root, text="To:").pack()
combo_to = ttk.Combobox(root, values=currencies, state="readonly")
combo_to.set("EUR")
combo_to.pack(pady=5)

# Convert Button
tk.Button(root, text="Convert", command=convert_currency, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

# Result Label
label_result = tk.Label(root, text="", font=("Arial", 14, "bold"))
label_result.pack(pady=10)

# Start the GUI
root.mainloop()
