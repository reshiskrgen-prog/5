# import tkinter for widgets, messagebox to 
# give user messages, ttk for treeview for tables,
# and matplotlib for graphs
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")  # use the TkAgg backend
# creates a GUI application for calculating energy
#  usage and cost based on selected appliances
#  and their usage hours.
# Appliance data
appliances = ["TV", "Fridge", "Washing Machine", "Computer", "Fan", "AC", "Food Processor", "Microwave", "WiFi"]
wattage = {
    "TV": 100, "Fridge": 150, "Washing Machine": 500, "Computer": 200, "Fan": 75,
    "AC": 1500, "Food Processor": 300, "Microwave": 1200, "WiFi": 20
}
cost_per_kwh = 0.13
cost = ""
results_textbox = ""
# Main window
root = tk.Tk()
root.title("💡 Energy Usage & Solar Savings Calculator")
root.geometry("1000x800")
root.configure(bg="#f0f9ff")
 
# Title
title = tk.Label(root, text="Grade 5-6 Energy Calculator", font=("Helvetica", 18, "bold"), bg="#f0f9ff", fg="#1d3557")
title.place(x=300, y=10)
 
# Frame for appliance inputs
input_frame = tk.LabelFrame(root, text="📋 Appliance Selection & Usage (hrs/day)", font=("Arial", 12, "bold"), bg="#e3f2fd", padx=10, pady=10)
input_frame.place(x=30, y=60, width=450, height=450)
 
selected_vars = {}
entries = {}
 
for i, app in enumerate(appliances):
    var = tk.IntVar()
    chk = tk.Checkbutton(input_frame, text=app, variable=var, bg="#e3f2fd", font=("Arial", 10))
    chk.place(x=10, y=10 + i * 40)
 
    ent = tk.Entry(input_frame, width=6, font=("Arial", 10))
    ent.place(x=200, y=10 + i * 40)
    ent.insert(0, "0")
 
    selected_vars[app] = var
    entries[app] = ent
 
# Calculate button
btn = tk.Button(root, text="🔍 Calculate", command=lambda: calculate(), bg="#00796b", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
btn.place(x=550, y=60)
 
# Treeview for appliance data
tree_frame = tk.LabelFrame(root, text="📊 Appliance-wise Energy & Cost", font=("Arial", 12, "bold"), bg="#f0f9ff")
tree_frame.place(x=500, y=110, width=460, height=250)
 
tree = ttk.Treeview(tree_frame, columns=("Appliance", "Usage", "Energy", "Cost"), show="headings", height=9)
tree.heading("Appliance", text="Appliance")
tree.heading("Usage", text="Usage (hrs/day)")
tree.heading("Energy", text="Energy (kWh/day)")
tree.heading("Cost", text="Cost ($/day)")
 
tree.column("Appliance", width=100)
tree.column("Usage", width=100)
tree.column("Energy", width=120)
tree.column("Cost", width=100)
tree.place(x=0, y=0, width=445, height=220)
 
# Scrollbar for treeview (optional if needed)
tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scroll.set)
tree_scroll.place(x=445, y=0, height=220)
 
# Summary frame
result_frame = tk.LabelFrame(root, text="📈 Summary & Suggestions", font=("italics", 12, "bold"), bg="#205d87")
result_frame.place(x=30, y=530, width=930, height=230)
 
# Scrollable text area
text_frame = tk.Frame(result_frame, bg="white")
text_frame.place(x=10, y=10, width=900, height=190)
 
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side='right', fill='y')
 
output_text = tk.Text(text_frame, font=("Arial", 11), yscrollcommand=scrollbar.set, wrap='word')
output_text.pack(side='left', fill='both', expand=True)
result_textbox = tk.Text(text_frame, font=("Arial"))
scrollbar.config(command=output_text.yview)

result_textbox = tk.Text(text_frame, font=("Arial", 11), yscrollcommand=scrollbar.set, wrap='word')
result_textbox.pack(side='left', fill='both', expand=True)
scrollbar.config(command=result_textbox.yview)
def calculate():
    tree.delete(*tree.get_children())
    output_text.delete("1.0", tk.END) # Clear previous table content
 
    total_energy = 0
    total_cost = 0
 
    output_text.insert(tk.END, "Energy and Cost Summary:\n\n")
 
    for appliance in appliances:
        if selected_vars[appliance].get() == 1:
            try:
                usage_hours = float(entries[appliance].get())
                # Get usage for the current appliance
 
                energy_consumed = round((wattage[appliance] * usage_hours) / 1000, 2)
                # Calculate energy consumed (in kWh)
 
                cost = round(energy_consumed * cost_per_kwh, 2)
                # Calculate cost (USD)
 
                total_energy += energy_consumed  # Add to total energy
                total_cost += cost  # Add to total cost
 
                # Insert into treeview
                tree.insert("", "end", values=(appliance, f"{usage_hours[app]} hrs", f"{energy_consumed[app]} kWh", f"${cost[app]:.2f}"))
 
                # Summary for the appliance
                output_text.insert(tk.END, f"🔌 {appliance}: Used for {usage_hours[app]} hrs → {energy_consumed[app]} kWh → Cost: ${cost[app]:.2f}\n")
 
 
            except ValueError:
                output_text.insert(tk.END, f"{appliance}: Invalid input.\n")
 
    # Insert total energy and cost
    output_text.insert(tk.END, f"\nTotal Energy: {total_energy:.2f} kWh\n")
    output_text.insert(tk.END, f"Total Cost: ${total_cost:.2f}")
def calculate():
    tree.delete(*tree.get_children()) # delete selected previous rows
    results_textbox.delete("1.0", tk.END) # delete previous inputs
    selected_appliances = [app for app in appliances if selected_vars[app].get() == 1] # loops through previously created list(S), checks which are checkboxed, puts checkboxes in a list
    if not selected_appliances: # if they are not selected / nothing is selected
        messagebox.showwarning("No appliance selcted", "Please select at least one appliance.") # gives user a warning
        return # send to user
    try: # if there is selected_appliances
        usage_hours = {app: float(entries[app].get()) for app in selected_appliances} # gets entry boxes' inputs, converts the text / string into a float (so that calculations will work) for every appliance in the list we created selected_appliances (this is a dictionary)
        energy_consumed = {app: round((wattage[app]).get()) for app in selected_appliances} # (another dictionary) looping through appliances and keeping one variable at a time into the dictionary
        cost = {app: round(energy_consumed[app] * cost_per_kwh, 2) for app in selected_appliances} # calculates cost based on consumed energy X cost per energy to figure out how much it would cost you 
        
        daily = round(sum(energy_consumed.values()), 2) # how much we use per day
        monthly = round(daily * 30, 2) # how much we use per month
        yearly = round(daily * 365, 2) # how much we use per year

        suggested_panels = round(daily / 1.5) # how many panels they should get
        solar_energy = round(suggested_panels * 1.5, 2) # the energy we get

        saved_kwh = min(daily, solar_energy) # the energy we save
        saved_money = round(saved_kwh * cost_per_kwh, 2) # the money we save
        
        panel_cost = 250 # cost of a panel
        install_cost = 500 # cost to install
        total_cost = panel_cost * suggested_panels + install_cost # cost to buy and install values
        break_even = round(total_cost / saved_money, 1) is saved_money > 0 else "-" # if we reach break-even which is when your savings = your debt, these are the calculations to figure out when savings = payment ( we also round it to one decimal point)

        for app in selected_appliances:
            tree.insert("", "end", values=(app, usage_hours[app], energy_consumed[app], f"${cost[app]:.2f}")) #report
        result_text = f""" # full report:

        📌 Daily Energy Usage: {daily} kWh

        🔋 Solar Energy Generated (Suggested Panels = {suggested_panels}): {solar_energy} kWh

        ____________________________________________________________________________________
 
        ✅ Savings if Solar is Used:

        - Daily Savings: {saved_kwh} kWh | ${saved_money}

        - Monthly Savings: {round(saved_kwh * 30, 2)} kWh | ${round(saved_money * 30, 2)}

        - Yearly Savings: {round(saved_kwh * 365, 2)} kWh | ${round(saved_money * 365, 2)}

        ____________________________________________________________________________________

        💰 Break-even Time: {break_even} days

        💸 Total Solar Setup Cost: ${total_cost}

        """

        results_textbox.insert(tk.END, result_text) # if forgot to put input 
 
    except ValueError:

        messagebox.showerror("Invalid Input", "Please enter valid numbers for all usage fields.")
    
root.mainloop()