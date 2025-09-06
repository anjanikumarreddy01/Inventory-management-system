from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import os
import qrcode
from employees import connect_database
import subprocess # A more robust way to open files
import sys # Needed for cross-platform support

class BillingApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Employee Billing Dashboard")
        self.window.geometry('1270x668+0+0')
        self.window.resizable(0, 0)

        # ========== Main Title and Header ==========
        try:
            self.icon_title = PhotoImage(file="inventory-management.png")
            title_image = self.icon_title
        except TclError:
            print("Warning: Title icon 'inventory-management.png' not found. Running without icon.")
            title_image = None

        title = Label(self.window, text="Inventory Management System", image=title_image, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # --- FIX: Changed command to self.logout ---
        btn_logout = Button(self.window, text="Logout", font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2", command=self.logout)
        btn_logout.place(x=1100, y=10, height=50, width=150)

        self.lbl_clock = Label(self.window, text="Welcome Employee\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        
        # ... (rest of the __init__ method is the same)
        # ========== Variables ==========
        self.search_product_var = StringVar()
        self.customer_name_var = StringVar()
        self.customer_contact_var = StringVar()
        self.product_name_var = StringVar()
        self.product_price_var = StringVar()
        self.product_qty_var = IntVar()
        self.cart_list = []
        self.bill_no = "" # To store the current bill number for QR code generation
        self.tax_rate = 0.0 # To store the tax rate from the database

        # ===================================================================================
        # ==================== SECTION 1: ALL PRODUCTS (LEFT FRAME) =========================
        # ===================================================================================
        
        ProductFrame1 = Frame(self.window, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626", fg="white")
        pTitle.pack(side=TOP, fill=X)

        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white", fg="green")
        lbl_search.place(x=5, y=5)

        txt_search = Entry(ProductFrame2, textvariable=self.search_product_var, font=("times new roman", 15), bg="lightyellow")
        txt_search.place(x=5, y=45, width=250, height=22)

        btn_search = Button(ProductFrame2, text="Search", font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.search_product)
        btn_search.place(x=260, y=45, width=130, height=22)
        
        btn_show_all = Button(ProductFrame2, text="Show All", font=("goudy old style", 15), bg="#083531", fg="white", cursor="hand2", command=self.show_all_products)
        btn_show_all.place(x=260, y=10, width=130, height=22)

        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3, columns=("id", "name", "price", "discount", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("id", text="ID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("discount", text="Discount(%)")
        self.product_Table.heading("qty", text="Qty")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"] = "headings"

        self.product_Table.column("id", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=80)
        self.product_Table.column("discount", width=80)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=80)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_product_data)
        
        # ===================================================================================
        # ==================== SECTION 2: WORKSPACE (CENTER FRAME) ==========================
        # ===================================================================================

        CustomerFrame = Frame(self.window, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=450, height=70)

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15, "bold"), bg="lightgray")
        cTitle.pack(side=TOP, fill=X)

        lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.customer_name_var, font=("times new roman", 13), bg="lightyellow").place(x=60, y=35, width=140)

        lbl_contact = Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(x=220, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.customer_contact_var, font=("times new roman", 13), bg="lightyellow").place(x=320, y=35, width=120)

        # --- My Cart Frame ---
        cart_Frame = Frame(self.window, bd=3, relief=RIDGE)
        cart_Frame.place(x=420, y=190, width=450, height=360)
        
        self.cartTitle = Label(cart_Frame, text="My Cart | Total Products: [0]", font=("goudy old style", 15, "bold"), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly_cart = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx_cart = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=("id", "name", "price", "qty"),
                                      yscrollcommand=scrolly_cart.set, xscrollcommand=scrollx_cart.set)
        scrollx_cart.pack(side=BOTTOM, fill=X)
        scrolly_cart.pack(side=RIGHT, fill=Y)
        scrollx_cart.config(command=self.CartTable.xview)
        scrolly_cart.config(command=self.CartTable.yview)

        self.CartTable.heading("id", text="ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Qty")
        self.CartTable["show"] = "headings"

        self.CartTable.column("id", width=40)
        self.CartTable.column("name", width=190)
        self.CartTable.column("price", width=100)
        self.CartTable.column("qty", width=50)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_cart_data)

        # --- Cart Management Widgets ---
        Add_Cart_WidgetsFrame = Frame(self.window, bd=2, relief=RIDGE, bg="white")
        Add_Cart_WidgetsFrame.place(x=420, y=550, width=450, height=110)

        lbl_p_name = Label(Add_Cart_WidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(x=5, y=5)
        txt_p_name = Entry(Add_Cart_WidgetsFrame, textvariable=self.product_name_var, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=5, y=30, width=190, height=22)

        lbl_p_price = Label(Add_Cart_WidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(x=215, y=5)
        txt_p_price = Entry(Add_Cart_WidgetsFrame, textvariable=self.product_price_var, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=215, y=30, width=150, height=22)

        lbl_p_qty = Label(Add_Cart_WidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=5, y=60)
        txt_p_qty = Entry(Add_Cart_WidgetsFrame, textvariable=self.product_qty_var, font=("times new roman", 15), bg="lightyellow").place(x=85, y=60, width=110, height=22)

        self.lbl_inStock = Label(Add_Cart_WidgetsFrame, text="In Stock [0]", font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=330, y=30)

        btn_clear_cart_fields = Button(Add_Cart_WidgetsFrame, text="Clear", font=("times new roman", 13, "bold"), bg="lightgray", cursor="hand2", command=self.clear_cart_fields).place(x=215, y=60, width=60, height=25)
        btn_add_cart = Button(Add_Cart_WidgetsFrame, text="Add To Cart", font=("times new roman", 13, "bold"), bg="orange", cursor="hand2", command=self.add_update_cart).place(x=300, y=60, width=100, height=25)

        # ===================================================================================
        # ==================== SECTION 3: BILLING AREA (RIGHT FRAME) ========================
        # ===================================================================================
        
        billFrame = Frame(self.window, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=875, y=110, width=385, height=410)

        BTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#f44336", fg="white")
        BTitle.pack(side=TOP, fill=X)

        scrolly_bill = Scrollbar(billFrame, orient=VERTICAL)
        scrolly_bill.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly_bill.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly_bill.config(command=self.txt_bill_area.yview)

        billMenuFrame = Frame(self.window, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=875, y=520, width=385, height=140)

        self.lbl_bill_amount = Label(billMenuFrame, text='Bill Amt\n[0]', font=('goudy old style', 12, 'bold'), bg='#3f51b5', fg='white')
        self.lbl_bill_amount.place(x=2, y=5, width=120, height=50)

        self.lbl_discount = Label(billMenuFrame, text='Discount\n[0]', font=('goudy old style', 12, 'bold'), bg='#8bc34a', fg='white')
        self.lbl_discount.place(x=124, y=5, width=120, height=50)

        self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n[0]', font=('goudy old style', 12, 'bold'), bg='#607d8b', fg='white')
        self.lbl_net_pay.place(x=246, y=5, width=130, height=50)

        btn_generate = Button(billMenuFrame, text='Generate Bill', font=('goudy old style', 12, 'bold'), bg='#009688', fg='white', cursor='hand2', command=self.generate_bill)
        btn_generate.place(x=2, y=60, width=120, height=40)

        btn_print = Button(billMenuFrame, text='Print', font=('goudy old style', 12, 'bold'), bg='#4CAF50', fg='white', cursor='hand2', command=self.print_bill)
        btn_print.place(x=124, y=60, width=120, height=40)

        btn_clear_all = Button(billMenuFrame, text='Clear All', font=('goudy old style', 12, 'bold'), bg='gray', fg='white', cursor='hand2', command=self.clear_all)
        btn_clear_all.place(x=246, y=60, width=130, height=40)

        # ========== Initial Setup Calls ==========
        self.show_all_products()
        self.fetch_tax_rate()
        self.update_time()

    # ===================================================================================
    # ============================ ALL FUNCTIONS ========================================
    # ===================================================================================

    def print_bill(self):
        """Opens the bill file in the default text editor for printing."""
        if not self.bill_no:
            messagebox.showerror("Error", "Please generate a bill first.", parent=self.window)
            return

        file_path = f"bills/{self.bill_no}.txt"
        if os.path.exists(file_path):
            try:
                # --- FIX: Using a more robust method to open the file for printing ---
                if sys.platform == "win32":
                    # On Windows, 'notepad' is a reliable way to open a text file
                    subprocess.Popen(['notepad.exe', file_path])
                else:
                    # For macOS and Linux
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, file_path])
            except Exception as e:
                messagebox.showerror("Print Error", f"Failed to open bill file: {e}", parent=self.window)
        else:
            messagebox.showerror("Error", f"Bill file not found: {file_path}", parent=self.window)
      
    def fetch_tax_rate(self):
        """Fetches the tax rate from the database."""
        cur, con = connect_database()
        try:
            cur.execute("USE inventory_system")
            cur.execute("SELECT tax FROM tax_table WHERE id=1")
            tax_result = cur.fetchone()
            if tax_result:
                self.tax_rate = float(tax_result[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching tax rate: {str(ex)}", parent=self.window)
        finally:
            if con:
                con.close()

    def show_all_products(self):
        self.search_product_var.set("")
        cur, con = connect_database()
        try:
            cur.execute("USE inventory_system")
            cur.execute("SELECT id, name, price, discount, quantity, status FROM product_data WHERE status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.window)
        finally:
            if con:
                con.close()

    def search_product(self):
        cur, con = connect_database()
        try:
            if self.search_product_var.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.window)
            else:
                cur.execute("USE inventory_system")
                cur.execute("SELECT id, name, price, discount, quantity, status FROM product_data WHERE name LIKE %s AND status='Active'", ("%" + self.search_product_var.get() + "%",))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.window)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.window)
        finally:
            if con:
                con.close()
            
    def get_product_data(self, ev):
        f = self.product_Table.focus()
        content = (self.product_Table.item(f))
        row = content['values']
        self.product_name_var.set(row[1])
        self.product_price_var.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.product_qty_var.set(1)

    def get_cart_data(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        self.product_name_var.set(row[1])
        # Find the original price, not the cart total price
        for item in self.product_Table.get_children():
            if self.product_Table.item(item)['values'][0] == row[0]:
                self.product_price_var.set(self.product_Table.item(item)['values'][2])
                stock = self.product_Table.item(item)['values'][4]
                self.lbl_inStock.config(text=f"In Stock [{str(stock)}]")
                break
        self.product_qty_var.set(row[3])
        

    def add_update_cart(self):
        if self.product_name_var.get() == '':
            messagebox.showerror('Error', "Please select a product from the list", parent=self.window)
            return
        
        stock_text = self.lbl_inStock.cget("text")
        current_stock = int(stock_text.split('[')[-1].split(']')[0])

        if self.product_qty_var.get() > current_stock:
            messagebox.showerror('Error', "Not enough stock available", parent=self.window)
            return

        product_id = -1
        discount_percent = 0
        for item in self.product_Table.get_children():
            if self.product_Table.item(item)['values'][1] == self.product_name_var.get():
                product_id = self.product_Table.item(item)['values'][0]
                # --- FIX: Handle 'None' or empty discount values ---
                discount_val = self.product_Table.item(item)['values'][3]
                if discount_val:
                    try:
                        discount_percent = float(discount_val)
                    except (ValueError, TypeError):
                        discount_percent = 0 # Default to 0 if conversion fails
                else:
                    discount_percent = 0
                break
        
        price = float(self.product_price_var.get())
        qty = self.product_qty_var.get()
        
        price_before_discount = price * qty
        discount_amount = (price_before_discount * discount_percent) / 100
        final_price = price_before_discount - discount_amount

        item_in_cart = False
        for i, item in enumerate(self.cart_list):
            if item[0] == product_id:
                item_in_cart = True
                self.cart_list[i][3] = qty # Update quantity
                self.cart_list[i][2] = final_price # Update total price
                self.cart_list[i][4] = discount_amount # Update discount amount
                break
        
        if not item_in_cart:
            cart_data = [product_id, self.product_name_var.get(), final_price, qty, discount_amount]
            self.cart_list.append(cart_data)

        self.show_cart()
        self.bill_updates()

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                # Display only id, name, price, qty in cart table
                self.CartTable.insert('', END, values=(row[0], row[1], f"{row[2]:.2f}", row[3]))
            self.cartTitle.config(text=f"My Cart | Total Products: [{len(self.cart_list)}]")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.window)

    def bill_updates(self):
        bill_amount = 0
        total_discount = 0
        for row in self.cart_list:
            bill_amount += float(row[2]) + float(row[4]) # price + discount
            total_discount += float(row[4])
        
        tax_amount = (bill_amount * self.tax_rate) / 100
        net_pay = (bill_amount - total_discount) + tax_amount

        self.lbl_bill_amount.config(text=f'Bill Amt\n[{bill_amount:.2f}]')
        self.lbl_discount.config(text=f'Discount\n[{total_discount:.2f}]')
        self.lbl_net_pay.config(text=f'Net Pay\n[{net_pay:.2f}]')

    def generate_bill(self):
        if not self.cart_list:
            messagebox.showerror("Error", "Please add products to the cart first", parent=self.window)
            return
        if self.customer_name_var.get() == '' or self.customer_contact_var.get() == '':
            messagebox.showerror("Error", "Customer details are required", parent=self.window)
            return

        self.bill_top()
        for row in self.cart_list:
            name = row[1]
            qty = row[3]
            price = (float(row[2]) + float(row[4])) / int(row[3]) # Recalculate price per item before discount
            self.txt_bill_area.insert(END, f"\n {name:<15}\t\t{qty}\tRs.{price * qty:.2f}")
        self.bill_bottom()
        
        # QR Code Generation
        self.generate_qr_code()

        # Save the final bill with QR info
        bill_text_content = self.txt_bill_area.get('1.0', END)
        with open(f"bills/{self.bill_no}.txt", "w", encoding='utf-8') as fp:
            fp.write(bill_text_content)
        
        messagebox.showinfo("Saved", "Bill has been saved successfully!", parent=self.window)
        self.update_stock()

    def bill_top(self):
        self.bill_no = str(time.strftime("%Y%m%d%H%M%S"))
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert(END, "\t\tInventory Management System\n")
        self.txt_bill_area.insert(END, f"\n Bill Number: {self.bill_no}")
        self.txt_bill_area.insert(END, f"\n Customer Name: {self.customer_name_var.get()}")
        self.txt_bill_area.insert(END, f"\n Phone No. : {self.customer_contact_var.get()}")
        self.txt_bill_area.insert(END, f"\n Date: {str(time.strftime('%d/%m/%Y'))}")
        self.txt_bill_area.insert(END, "\n==================================================")
        self.txt_bill_area.insert(END, "\n Product\t\tQTY\tPrice")
        self.txt_bill_area.insert(END, "\n==================================================")

    def bill_bottom(self):
        bill_amount = 0
        total_discount = 0
        for row in self.cart_list:
            bill_amount += float(row[2]) + float(row[4])
            total_discount += float(row[4])
        
        tax_amount = (bill_amount * self.tax_rate) / 100
        net_pay = (bill_amount - total_discount) + tax_amount

        self.txt_bill_area.insert(END, "\n==================================================")
        self.txt_bill_area.insert(END, f"\n Bill Amount:\t\t\tRs.{bill_amount:.2f}")
        self.txt_bill_area.insert(END, f"\n Discount:\t\t\tRs.{total_discount:.2f}")
        self.txt_bill_area.insert(END, f"\n Tax ({self.tax_rate}%):\t\t\tRs.{tax_amount:.2f}")
        self.txt_bill_area.insert(END, f"\n Net Pay:\t\t\tRs.{net_pay:.2f}")
        self.txt_bill_area.insert(END, "\n==================================================")

    def generate_qr_code(self):
        """Generates a QR code and displays it on the bill."""
        if not self.bill_no:
            return

        bill_amount_text = self.lbl_bill_amount.cget('text').splitlines()[1].replace('[', '').replace(']', '')
        net_pay_text = self.lbl_net_pay.cget('text').splitlines()[1].replace('[', '').replace(']', '')

        bill_data = f"Bill No.: {self.bill_no}\nCustomer: {self.customer_name_var.get()}\nBill Amount: Rs.{bill_amount_text}\nNet Pay: Rs.{net_pay_text}"
        
        qr = qrcode.QRCode(version=1, box_size=4, border=1)
        qr.add_data(bill_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        
        qr_img_path = f"bills/{self.bill_no}_qr.png"
        img.save(qr_img_path)

        # Display on screen
        self.qr_photo = ImageTk.PhotoImage(file=qr_img_path)
        self.txt_bill_area.insert(END, '\n\n')
        self.txt_bill_area.image_create(END, image=self.qr_photo)
        self.txt_bill_area.insert(END, '\n      Scan for Details')
        
    def update_stock(self):
        cur, con = connect_database()
        try:
            cur.execute("USE inventory_system")
            for item in self.cart_list:
                product_id = item[0]
                sold_qty = item[3]
                cur.execute("UPDATE product_data SET quantity=(quantity-%s) WHERE id=%s", (sold_qty, product_id))
            con.commit()
            self.show_all_products()
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating stock: {str(ex)}", parent=self.window)
        finally:
            if con:
                con.close()

    def clear_all(self):
        self.customer_name_var.set('')
        self.customer_contact_var.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cart_list = []
        self.show_cart()
        self.bill_updates()
        self.clear_cart_fields()
        self.show_all_products()
        self.bill_no = "" # Reset bill number

    def clear_cart_fields(self):
        self.product_name_var.set('')
        self.product_price_var.set('')
        self.product_qty_var.set(0)
        self.lbl_inStock.config(text="In Stock [0]")

    def update_time(self):
        time_string = time.strftime("%I:%M:%S %p")
        date_string = time.strftime("%d/%m/%Y")
        self.lbl_clock.config(text=f"Welcome Employee\t\t Date: {date_string}\t\t Time: {time_string}")
        self.lbl_clock.after(1000, self.update_time)

    def logout(self):
        """Closes the dashboard and re-opens the login screen."""
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        if confirm:
            self.window.destroy()
            # --- FIX: Use correct filename and 'python' command ---
            os.system("python Login_page.py")


if __name__ == "__main__":
    root = Tk()
    app = BillingApp(root)
    if not os.path.exists("bills"):
        os.makedirs("bills")
    root.mainloop()