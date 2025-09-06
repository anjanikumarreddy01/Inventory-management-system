from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

def sales_form(window):
    global back_icon, logo  # if not global it won't be visible in frame
    sales_frame = Frame(window, width=1070, height=567, bg='white')
    sales_frame.place(x=200, y=98)

    heading_label = Label(sales_frame, text="View Customer Bills", font=("arial", 16, 'bold'), bg="#7A7AEC", fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # --- Gracefully handle missing image ---
    try:
        back_icon = PhotoImage(file='back_icon.png')
        back_button = Button(sales_frame, bg='white', image=back_icon, bd=0, cursor='hand2', command=lambda: sales_frame.place_forget())
        back_button.place(x=10, y=30)
    except TclError:
        print("Warning: 'back_icon.png' not found.")
        back_button = Button(sales_frame, text="< Back", bd=0, cursor='hand2', command=lambda: sales_frame.place_forget())
        back_button.place(x=10, y=30)


    # ===================================================================================
    # ============================ HELPER FUNCTIONS =====================================
    # ===================================================================================

    def show_bills():
        """Reads the 'bills' directory and populates the listbox with bill filenames."""
        search_entry.delete(0, END)
        L_treeview.delete(*L_treeview.get_children())
        
        if not os.path.exists("bills"):
            messagebox.showerror("Error", "Bills directory not found.", parent=sales_frame)
            return

        # Read only .txt files from the bills directory
        bill_files = [f for f in os.listdir('bills/') if f.endswith('.txt')]
        bill_files.sort() # Sort the files for consistent order

        for file in bill_files:
            L_treeview.insert('', END, values=[file])

    def get_bill_data(event):
        """Displays the content of the selected bill file in the Text area."""
        selected_item = L_treeview.focus()
        if not selected_item:
            return
            
        content = L_treeview.item(selected_item)
        file_name = content['values'][0]
        
        bill_area.config(state=NORMAL) # Enable writing to the text area
        bill_area.delete('1.0', END)
        
        # Display text content from the selected file
        try:
            with open(f'bills/{file_name}', 'r', encoding='utf-8') as fp:
                bill_area.insert(END, fp.read())
        except Exception as e:
            messagebox.showerror("Error", f"Could not read bill file: {e}", parent=sales_frame)
        
        bill_area.config(state=DISABLED) # Make text area read-only again

    def search_bill():
        """Searches for a specific bill by invoice number."""
        search_term = search_entry.get()
        if search_term == "":
            messagebox.showerror("Error", "Invoice number is required.", parent=sales_frame)
            return

        L_treeview.delete(*L_treeview.get_children())
        found = False
        # Using os.listdir() is fine for this number of files
        all_bills = [f for f in os.listdir('bills/') if f.endswith('.txt')]
        for file in all_bills:
            if search_term in file:
                L_treeview.insert('', END, values=[file])
                found = True
        
        if not found:
            messagebox.showinfo("Not Found", "No bill found with that invoice number.", parent=sales_frame)
            show_bills() # Show all bills again if nothing was found

    def clear_search():
        """Clears the search and shows all bills."""
        search_entry.delete(0, END)
        show_bills()
        # --- FIX: Clear the bill display area as well ---
        bill_area.config(state=NORMAL)
        bill_area.delete('1.0', END)
        bill_area.config(state=DISABLED)


    # ===================================================================================
    # ============================ ORIGINAL UI LAYOUT ===================================
    # ===================================================================================

    left_frame = Frame(sales_frame, bg='white', relief=RIDGE)
    left_frame.place(x=20, y=60, width=600, height=500)

    search_frame = Frame(left_frame, bg='white')
    search_frame.pack(pady=(40, 40))

    num_label = Label(search_frame, text="Invoice No.", font=('times new roman', 14, 'bold'), bg='white')
    num_label.grid(row=0, column=0, padx=(0, 15), sticky='w')
    search_entry = Entry(search_frame, font=('times new roman', 14), bg='lightyellow', width=12)
    search_entry.grid(row=0, column=1, pady=10)

    search_button = Button(search_frame, text='Search', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#7A79E8', command=search_bill)
    search_button.grid(row=0, column=2, padx=15)

    clear_button = Button(search_frame, text='Clear', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#7A79E8', command=clear_search)
    clear_button.grid(row=0, column=3)

    # ---------------------- left treeview and right text area -------------------------------------------------------------------

    left_treeview_frame = Frame(left_frame, bd=2, relief=RIDGE)
    left_treeview_frame.place(x=10, y=110, width=230, height=330)
    
    lscrolly = Scrollbar(left_treeview_frame, orient=VERTICAL)
    
    L_treeview = ttk.Treeview(left_treeview_frame, columns=("Invoice"), show='headings', yscrollcommand=lscrolly.set)
    L_treeview.heading("Invoice", text="Invoice No.")
    L_treeview.column("Invoice", width=210)

    lscrolly.pack(side=RIGHT, fill=Y)
    lscrolly.config(command=L_treeview.yview)
    
    L_treeview.pack(fill=BOTH, expand=1)
    L_treeview.bind("<ButtonRelease-1>", get_bill_data)

    # ---------------------------------------------------------------
    right_display_top = Frame(left_frame, relief=RIDGE)
    right_display_top.place(x=270, y=110, width=325, height=30)

    heading_label_right = Label(right_display_top, text="Customer Bill Area", font=("arial", 14, 'bold'), bg="#7A79E8", fg='white')
    heading_label_right.place(x=0, y=0, relwidth=1)
    
    right_display_frame = Frame(left_frame, bd=2, relief=RIDGE)
    right_display_frame.place(x=270, y=140, width=325, height=300)

    # --- ESSENTIAL CHANGE: Using a Text widget instead of Treeview to show bill content ---
    rscrolly = Scrollbar(right_display_frame, orient=VERTICAL)
    bill_area = Text(right_display_frame, yscrollcommand=rscrolly.set, font=("arial", 10))
    rscrolly.pack(side=RIGHT, fill=Y)
    rscrolly.config(command=bill_area.yview)
    bill_area.pack(fill=BOTH, expand=1)
    bill_area.config(state=DISABLED) # Make it read-only initially

    # --------------------- right hand side image --------------------------------------------------
    try:
        logo = PhotoImage(file='money.png')
        label = Label(sales_frame, image=logo, bg='white')
        label.place(x=690, y=200)
    except TclError:
        print("Warning: 'money.png' not found.")

    # ========== Initial Call to load bills ==========
    show_bills()
    
    return sales_frame
