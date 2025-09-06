from tkinter import*
from PIL import Image,ImageTk # library for background image
from employees import employee_form
from supplier import supplier_form
from category import category_form
from product import product_form
from employees import connect_database
from sales import sales_form
from tkinter import messagebox
import time
import os

def exit_app():
    """Shows a confirmation and then closes the entire application."""
    confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit the application?")
    if confirm:
        window.destroy()


def logout():
    """Closes the dashboard and re-opens the login screen."""
    confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
    if confirm:
        window.destroy()
        # Make sure your login file is named 'login.py' or update the filename below
        os.system("Login_page.py")



def update():

    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    # for employee count
    cursor.execute('SELECT *from employee_data')
    records=cursor.fetchall()
    total_employee_count.config(text=len(records))

    #for supplier count
    cursor.execute('SELECT *FROM supplier_data')
    records1=cursor.fetchall()
    total_supplier_count.config(text=len(records1))

    # for product count
    cursor.execute('SELECT *FROM product_data')
    records2=cursor.fetchall()
    total_product_count.config(text=len(records2))

    # for product count
    cursor.execute('SELECT *FROM category_data')
    records3=cursor.fetchall()
    total_categories_count.config(text=len(records3))

    current_time=time.strftime('%I:%M:%S %p') #%I 12 hours format %min %sec %p for am or pm
    current_date=time.strftime('%d/%m/%Y')#Y full year ,y form only last 2 digits
    #date_time=time.strftime('%I:%M:%S %p on %A,%B %d,%Y')
    subtitle_label.config(text=f'Welcome Admin \t\t {current_time}\t\t{current_date}')
    subtitle_label.after(1000,update)# 1sec =1000 ms




def tax_window():
    def save_tax():
        value=tax_count.get()
        cursor,connnection=connect_database()
        if not cursor or not connnection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT PRIMARY KEY,tax DECIMAL(5,2))')
        cursor.execute('SELECT id FROM tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table set tax=%s WHERE id=1',value)
        else:
            cursor.execute('INSERT INTO tax_table (id,tax)values(1,%s)',value)

        connnection.commit()
        messagebox.showinfo('Success',f'Tax is set to {value} and saved successfully',parent=tax_root)# parent will help to not dissaper



    tax_root=Toplevel()
    tax_root.title('Tax window')
    tax_root.geometry('300x200')
    tax_root.grab_set()# it will ristrict you to do anything other than closing and add tax in page in tax_window
    tax_percentage=Label(tax_root,text='Enter Tax Percentage',font=('Times new roman',12))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root,from_=0,to=100,font=('Times new roman',12))
    tax_count.pack(pady=10)
    delete_button=Button(tax_root,text='Save',font=('times new roman',12,'bold'),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=save_tax)
    delete_button.pack(pady=20)




# Main code of in dashboard
# for avoiding double click button bug
curret_form=None
def show_form(form_function):
    global curret_form
    if curret_form:
        curret_form.place_forget()
    curret_form=form_function(window)

window=Tk()
window.title("Dashboard")
# add in background image for dashboard
m1=Image.open(r"C:\Users\User1\OneDrive\Pictures\dashboard.png")
m2=ImageTk.PhotoImage(m1)
bg_label=Label(window,image=m2)
bg_label.place(x=0,y=0,relheight=1,relwidth=1)

# keeping window size from 0+0(top corner)
window.geometry('1270x668+0+0')
window.resizable(0,0)# not allowing to resize the window by keeping it as 0,0

bg_image_icon=PhotoImage(file='inventory-management.png')# loaded the icon 

# "compund = left" will decide that the icon should come at left or right to the text
title_label=Label(window,image=bg_image_icon,compound=LEFT,text="Inventory Management System",font=('times new roman',40,'bold'),bg='#010c48',fg='white',anchor='w',padx=20)
title_label.place(x=0,y=0,relwidth=1)# relwidth=1 will put the label in center of width and give complete line of label

subtitle_label=Label(window ,text='Welcome Admin \t\t Date: 31-07-25\t\t Time:12:30:40 pm',font=('times new roman',15),bg="#6C6D71",fg='white')
subtitle_label.place(x=0,y=70,relwidth=1)

#######################################################################################################

#Left frame
leftFrame=Frame(window)
leftFrame.place(x=0,y=100,width=200,height=570)

logoimage=PhotoImage(file='checklist.png')
image_logo=Label(leftFrame,image=logoimage)
image_logo.pack()

#load icons in left frame buttons
employee_icon=PhotoImage(file='man.png') 
supplier_icon=PhotoImage(file='tracking.png')
category_icon=PhotoImage(file='product-categories.png')
product_icon=PhotoImage(file='package.png')
sales_icon=PhotoImage(file='increasing.png')
tax_icon=PhotoImage(file='taxes.png')
exit_icon=PhotoImage(file='logout.png')

#adding buttons to left frame
# compound=LEFT is used to shift the logo to left of text
#anchor='w','e','n','s' this is used to pull complete text to that side of button
employee_button1=Button(leftFrame,image=employee_icon,compound=LEFT,text=" Employee",font=('times new roman',20,'bold'),anchor='w',command=lambda:show_form(employee_form))
supplier_button2=Button(leftFrame,image=supplier_icon,compound=LEFT,text=" Supplier",font=('times new roman',20,'bold'),anchor='w',command=lambda:show_form(supplier_form))
category_button3=Button(leftFrame,image=category_icon,compound=LEFT,text=" Category",font=('times new roman',20,'bold'),anchor='w',command=lambda:show_form(category_form))
product_button4=Button(leftFrame,image=product_icon,compound=LEFT,text=" Product",font=('times new roman',20,'bold'),anchor='w',command=lambda:show_form(product_form))
sales_button5=Button(leftFrame,image=sales_icon,compound=LEFT,text=" Sales",font=('times new roman',20,'bold'),anchor='w',command=lambda:show_form(sales_form))
tax_button6=Button(leftFrame,image=tax_icon,compound=LEFT,text=" Tax",font=('times new roman',20,'bold'),anchor='w',command=tax_window)
exit_button6=Button(leftFrame,image=exit_icon,compound=LEFT,text=" Exit",font=('times new roman',20,'bold'),anchor='w', command=exit_app) # <-- Added command

# displaying buttons in left frame
employee_button1.pack(fill=X)
supplier_button2.pack(fill=X)
category_button3.pack(fill=X)
product_button4.pack(fill=X)
sales_button5.pack(fill=X)
tax_button6.pack(fill=X)
exit_button6.pack(fill=X)
###################################################################################################

# 1 creating employee frame

total_employee_frame=Frame(window,bg="#7D8BBA")
total_employee_frame.place(x=400,y=125,width=280,height=170)

#adding label
total_employee_icon=PhotoImage(file='total_employee.png')
total_employee_icon_label=Label(total_employee_frame,image=total_employee_icon,bg='#7D8BBA')
total_employee_icon_label.pack(pady=15)

total_employee_label=Label(total_employee_frame,text='Total Employees',font=('times new roman',15),bg='#7D8BBA')
total_employee_label.pack()

total_employee_count=Label(total_employee_frame,text="0",font=('times new roman',30,'bold'),bg='#7D8BBA')
total_employee_count.pack()


# 2 creating suppliers frame 

total_supplier_frame=Frame(window,bg="#B3B3B3")
total_supplier_frame.place(x=800,y=125,width=280,height=170)

#adding icon
total_supplier_icon=PhotoImage(file='total_supplier_icon.png')
total_supplier_icon_label=Label(total_supplier_frame,image=total_supplier_icon,bg='#B3B3B3')
total_supplier_icon_label.pack(pady=15)
#adding labels
total_supplier_label=Label(total_supplier_frame,text='Total Suppliers',font=('times new roman',15),bg='#B3B3B3')
total_supplier_label.pack()
#label count
total_supplier_count=Label(total_supplier_frame,text="0",font=('times new roman',30,'bold'),bg='#B3B3B3')
total_supplier_count.pack()


# 3 creating categorirs frame 

total_categories_frame=Frame(window,bg="#778899")
total_categories_frame.place(x=400,y=310,width=280,height=170)

#adding icon
total_categories_icon=PhotoImage(file='total_categories_icon.png')
total_categories_icon_label=Label(total_categories_frame,image=total_categories_icon,bg='#778899')
total_categories_icon_label.pack(pady=15)
#adding labels
total_categories_label=Label(total_categories_frame,text='Total Categories',font=('times new roman',15),bg='#778899')
total_categories_label.pack()
#label count
total_categories_count=Label(total_categories_frame,text="0",font=('times new roman',30,'bold'),bg='#778899')
total_categories_count.pack()

# 4 creating product frame 

total_product_frame=Frame(window,bg="#D9D9D9")
total_product_frame.place(x=800,y=310,width=280,height=170)

#adding icon
total_product_icon=PhotoImage(file='total_product_icon.png')
total_product_icon_label=Label(total_product_frame,image=total_product_icon,bg="#D9D9D9")
total_product_icon_label.pack(pady=15)
#adding labels
total_product_label=Label(total_product_frame,text='Total Products',font=('times new roman',15),bg='#D9D9D9')
total_product_label.pack()
#label count
total_product_count=Label(total_product_frame,text="0",font=('times new roman',30,'bold'),bg='#D9D9D9')
total_product_count.pack()


# 5 creating sales frame 

total_sales_frame=Frame(window,bg="#219EBC")
total_sales_frame.place(x=600,y=495,width=280,height=170)

#adding icon
total_sales_icon=PhotoImage(file='total_sales_icon.png')
total_sales_icon_label=Label(total_sales_frame,image=total_sales_icon,bg="#219EBC")
total_sales_icon_label.pack(pady=15)
#adding labels
total_sales_label=Label(total_sales_frame,text='Total Sales',font=('times new roman',15),bg="#219EBC")
total_sales_label.pack()
#label count
total_sales_count=Label(total_sales_frame,text="0",font=('times new roman',30,'bold'),bg="#219EBC")
total_sales_count.pack()

# buttons at right side top 
logout_button=Button(window,text="Logout",font=('times new roman',20,'bold'),borderwidth=5,fg="#010c48", command=logout) # <-- Added command
#button display
logout_button.place(x=1150,y=7)

update()

window.mainloop()