# library_gui.py
# Acknowledgement : original logic by kasiaka oghenetega emmanuel
# a gui cool version of the library search system using tkinter
import tkinter as tk
from tkinter import ttk,messagebox
import library_functions as lib

try:
    subjects = lib.load_subjects()
    locations = lib.load_locations()
except FileNotFoundError as e:
    messagebox.showerror('missing file', str(e))
    raise SystemExit(str(e))
root = tk.Tk()
root.title("📚library search system")
root.geometry('600x600')
root.config(bg = "#1f53a2")
style = ttk.Style()
style.configure('TLabel', background="#b8c2d7", foreground = '#1f2937', font=('segoe UI', 10))
style.configure("TButton", background=( '#e0f0ff'))
style.map('TButton', background=[('active', '#e0f0ff')])
title_label = tk.Label(root,text='📚library search system',font = ("segoe UI", 16, "bold"))
title_label.pack(pady=20)

# frame for inputs and dropdowns
input_frame = ttk.LabelFrame(root,text='search options',padding =(15,10))
input_frame.pack(fill ='x', padx=20, pady = (10,10))

# to search said input term
ttk.Label(input_frame, text=' enter search term:').grid(row=0,column=0, sticky ='w')
entry = ttk.Entry (input_frame, width =40)
entry.grid(row =0, column =1, padx =10, pady=5)

# dropdown for the kind of search
ttk.Label(input_frame, text=' search by:').grid(row=1, column =0, sticky ='w')
search_type = ttk.Combobox(input_frame, values =['subject', 'Classmark','location'], state=' readonly', width = 37)
search_type.current(0)
search_type.grid(row=1, column =1, padx =10, pady=5)

# fuction that actually performs the search
def perform_search():
    term = entry.get().strip()
    kind = search_type.get()

    if not term:
        messagebox.showwarning("Input Error", "Please enter a search term.")
        return
    
   # if kind == 'subject':
    #    results =lib.search_subject(term, subjects, locations)
    #elif kind == " Classmark":
     #   results = lib.search_classmark(term, subjects, locations)
    #else:
    #    results = lib.search_location(term, subjects,locations)



    if kind == "subject":
        results = lib.search_subject(term, subjects, locations)
    elif kind == "Classmark":
        results = lib.search_classmark(term, subjects, locations)
    else:
        results = lib.search_location(term, subjects, locations)
      # I was testing something here earlier
      # print(locations)
  

    result_box.config(state='normal')
    result_box.delete("1.0", tk.END)
    if results:
        for r in results:
            result_box.insert(tk.END, "• " + r + "\n")
    else:
        result_box.insert(tk.END, "No matches found.\n")
    result_box.config(state='disabled')
# this is the clear function 
def clear_all():
    entry.delete(0, tk.END)
    result_box.config(state='normal')
    result_box.delete("1.0", tk.END)
    result_box.config(state='disabled')
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)
ttk.Button(btn_frame, text="🔍 Search", command=perform_search).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="🧹 Clear", command=clear_all).grid(row=0, column=1, padx=8)
ttk.Button(btn_frame, text="❌ Exit", command=root.destroy).grid(row=0, column=2, padx=8)

# Results area where the results will be displayed
result_frame = ttk.LabelFrame(root, text="Results", padding=(10, 10))
result_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))

# Scrollbar and  Textbox
scrollbar = ttk.Scrollbar(result_frame)
scrollbar.pack(side='right', fill='y')
result_box = tk.Text(result_frame,
                     wrap='word',
                     height=12,
                     state='disabled',
                     yscrollcommand=scrollbar.set,
                     bg="white",
                     fg="#1f2937",
                     font=("Consolas", 11))
result_box.pack(fill='both', expand=True)
scrollbar.config(command=result_box.yview)

# Footer
footer = tk.Label(root,
                  text="Developed by kasiaka oghenetega Emmanuel",
                  bg="#f7f9fc",
                  fg="#64748b",
                  font=("Segoe UI", 9))
footer.pack(side='bottom', pady=6)

root.mainloop()
