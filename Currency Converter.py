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

        # Save to conversion history
        history_list.insert(0, f"{amount} {from_currency} = {result} {to_currency}")
    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))
    except requests.exceptions.RequestException as re:
        messagebox.showerror("Network Error", "Failed to connect to the API. Please check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

def swap_currencies():
    from_currency = combo_from.get()
    to_currency = combo_to.get()
    combo_from.set(to_currency)
    combo_to.set(from_currency)

def fetch_historical_rates():
    try:
        from_currency = combo_from.get()
        if not from_currency:
            raise ValueError("Please select a currency to fetch historical rates.")

        # Use a different API for historical rates (e.g., Open Exchange Rates)
        api_key = "YOUR_NEW_API_KEY"  # Replace with your new API key
        url = f"https://openexchangerates.org/api/historical/2023-01-01.json?app_id={api_key}&base={from_currency}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}.")

        data = response.json()
        # Display historical rates (simplified for demonstration)
        rates = data.get("rates", {})
        messagebox.showinfo("Historical Rates", f"Historical rates for {from_currency} on 2023-01-01: {rates}")
    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# Load Conversion History Function
def load_history():
    try:
        with open("conversion_history.txt", "r") as file:
            history_list.delete(0, tk.END)
            for line in file:
                history_list.insert(tk.END, line.strip())
        messagebox.showinfo("Success", "Conversion history loaded successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved history found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load history: {e}")

# Dark Mode Toggle Function
def toggle_dark_mode():
    if root["bg"] == "white":
        root.config(bg="black")
        for widget in root.winfo_children():
            widget.config(bg="black", fg="white")
    else:
        root.config(bg="white")
        for widget in root.winfo_children():
            widget.config(bg="white", fg="black")

# Save Favorite Pair Function
def save_favorite_pair():
    from_currency = combo_from.get()
    to_currency = combo_to.get()
    if from_currency and to_currency:
        favorite_pairs.insert(tk.END, f"{from_currency} -> {to_currency}")
    else:
        messagebox.showerror("Error", "Please select both currencies.")

# Load Favorite Pair Function
def load_favorite_pair(event):
    try:
        # Ensure an item is selected
        selected_index = favorite_pairs.curselection()
        if not selected_index:
            return  # No selection, exit the function

        selected_pair = favorite_pairs.get(selected_index)
        from_currency, to_currency = selected_pair.split(" -> ")
        combo_from.set(from_currency)
        combo_to.set(to_currency)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load favorite pair: {e}")

# Clear All Fields Function
def clear_all_fields():
    entry_amount.delete(0, tk.END)
    combo_from.set("USD")
    combo_to.set("EUR")
    label_result.config(text="")
    history_list.delete(0, tk.END)

# Currencies list (you can add more if you want)
currencies = ["USD", "EUR", "GBP", "JPY", "MAD", "CAD", "AUD", "CNY"]

# GUI Setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("500x600")
root.resizable(True, True)

# Title
tk.Label(root, text="Currency Converter", font=("Helvetica", 16, "bold")).pack(pady=10)

# Amount Entry
tk.Label(root, text="Amount:").pack()
entry_amount = ttk.Entry(root, font=("Arial", 12))
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

# Swap Button
tk.Button(root, text="Swap Currencies", command=swap_currencies, bg="#FFC107", fg="black", font=("Arial", 12)).pack(pady=5)

# Convert Button
tk.Button(root, text="Convert", command=convert_currency, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

# Result Label
label_result = tk.Label(root, text="", font=("Arial", 14, "bold"))
label_result.pack(pady=10)

# Conversion History
tk.Label(root, text="Conversion History:", font=("Arial", 12, "bold")).pack(pady=5)
history_list = tk.Listbox(root, height=5, font=("Arial", 10))
history_list.pack(pady=5, fill=tk.BOTH, expand=True)

# Historical Rates Button
tk.Button(root, text="Fetch Historical Rates", command=fetch_historical_rates, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=5)

# Add Load History Button
tk.Button(root, text="Load History", command=load_history, bg="#03A9F4", fg="white", font=("Arial", 12)).pack(pady=5)

# Add Dark Mode Toggle Button
tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, bg="#607D8B", fg="white", font=("Arial", 12)).pack(pady=5)

# Favorite Pairs List
tk.Label(root, text="Favorite Pairs:", font=("Arial", 12, "bold")).pack(pady=5)
favorite_pairs = tk.Listbox(root, height=5, font=("Arial", 10))
favorite_pairs.pack(pady=5, fill=tk.BOTH, expand=True)
favorite_pairs.bind("<<ListboxSelect>>", load_favorite_pair)

# Add Save Favorite Pair Button
tk.Button(root, text="Save Favorite Pair", command=save_favorite_pair, bg="#FF9800", fg="white", font=("Arial", 12)).pack(pady=5)

# Add Clear All Fields Button
tk.Button(root, text="Clear All Fields", command=clear_all_fields, bg="#FF5722", fg="white", font=("Arial", 12)).pack(pady=5)

# Start the GUI
root.mainloop()
