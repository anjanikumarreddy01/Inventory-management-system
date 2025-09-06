from tkinter import*
from tkinter import ttk # for combobox, treeview
from tkinter import messagebox 
from employees import connect_database

def clear(invoice_entry,name_entry,contact_entry,description_text):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)


def search_supplier(invoice,treeview):
    if invoice=='':
        messagebox.showerror('Error','Please enter the invoive number')
        
    else:
        cursor,conncetion= connect_database()
        if not cursor or not conncetion:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute('SELECT *from supplier_data WHERE invoice=%s',(invoice,))
            record=cursor.fetchone()
            if not record:
                messagebox.showerror('Error','No record matched')
                return
            treeview.delete(*treeview.get_children())#for deleting data in treeview  
            treeview.insert('',END,values=record)# inserting new data which we entered
        except Exception as e:
            messagebox.showerror('Error',f'Error due to{e}')
        finally:
            cursor.close()
            conncetion.close()
            
# for showing all records 
def show_all(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)
    

    

    


    
    


def delete_supplier(invoice,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor,conncetion= connect_database()
    if not cursor or not conncetion:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s',(invoice,))
        conncetion.commit()
        treeview_data(treeview)# for showing data after deletion
        messagebox.showinfo('Info','Record is deleted')
    except Exception as e:
        messagebox.showerror('Error',f'Error due to{e}')
    finally:
        cursor.close()
        conncetion.close()
    

def update_supplier(invoice,name,contact,description,treeview):
    index=treeview.selection()# checking is ther eany row is selected in treeview or not
    if not index:
        messagebox.ERROR("Error",'No row is selected ')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
            return
    try:

        cursor.execute("USE inventory_system")
        #for checking the left frame for any changes if it finds it will update or else just show thw message that there are no changes
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s',(invoice,))#it will give the id 
        current_data=cursor.fetchone() 
        current_data=current_data[1:]# removed invoice column as we not taken invoice in new_data 
        new_data=(name,contact,description)
        if current_data==new_data:
            messagebox.showinfo('Info','No data is updated')
            return
        cursor.execute('UPDATE supplier_data SET name=%s,contact=%s,description=%s WHERE invoice=%s',(name,contact,description,invoice))
        connection.commit()
        messagebox.showinfo('Info','Data is updated')
        treeview_data(treeview) #this will show updated data in treeview 
    except Exception as e:
        messagebox.showerror('Error',f'Error due to{e}')
    finally:
        cursor.close()
        connection.close()


def select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview):
    index=treeview.selection()# it will give index
    content=treeview.item(index) #it will give you the content dictionary
    actual_content=content['values']# this content dictionary have values key which has the actual content
    # now inserting the conent into left frame entry fields
    #deleting all entry fields
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)

    #inserting values in left farme of selected row in treeview
    invoice_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    description_text.insert(1.0,actual_content[3])


#for showing data in treeview
def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
            return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT *FROM supplier_data')
        #next step is to insert data in treeview
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to{e}')
    finally:
        cursor.close()
        connection.close()
    



def add_supplier(invoice,name,contact,description,treeview):
    if invoice=='' or name=='' or contact==''or description=='':# strip() for removing nullin text area
        messagebox.showerror("Error",'All fileds are requried')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')
            

            cursor.execute('CREATE TABLE IF NOT EXISTS supplier_data (invoice int primary key,name varchar(100),contact varchar(15),description TEXT)')

            cursor.execute('SELECT *FROM supplier_data WHERE invoice=%s',invoice)
            if cursor.fetchone():
                messagebox.showerror('Error','invoice No alrady exists')
                return

            cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s)',(invoice,name,contact,description))#form removing null vales at end
            connection.commit()
            messagebox.showinfo('Info','Data is inserted')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to{e}')
        finally:
            cursor.close()
            connection.close()

        


    










#main supplier form code--------------------------------------------------------------------------------------------------------------------------------------------------


def supplier_form(window):
    global back_icon
    supplier_frame=Frame(window,width=1070,height=567,bg='white')
    supplier_frame.place(x=200,y=98)
    # heading leable 
    heading_label=Label(supplier_frame,text="Manage Supplier Details",font=("times new roman",16,'bold'),bg="#7A79E8",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    back_icon=PhotoImage(file='back_icon.png')
    back_button=Button(supplier_frame,bg='white',image=back_icon,bd=0,cursor='hand2',command=lambda:supplier_frame.place_forget())
    back_button.place(x=10,y=30)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    left_frame=Frame(supplier_frame,bg='white')
    left_frame.place(x=10,y=100)

    invoice_label=Label(left_frame,text="Invoice No.",font=('times new roman',14,'bold'),bg='white')
    invoice_label.grid(row=0,column=0,padx=(20,40),sticky='w')
    invoice_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    invoice_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text="Supplier name",font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(20,40),pady=25,sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text="Supplier contact",font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=(20,40),sticky='w')
    contact_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    contact_entry.grid(row=2,column=1)

    description_label=Label(left_frame,text="Description",font=('times new roman',14,'bold'),bg='white')
    description_label.grid(row=3,column=0,padx=(20,40),pady=25,sticky='nw')
    description_text=Text(left_frame,width=25,height=6,bd=2,bg='lightyellow')
    description_text.grid(row=3,column=1,pady=25)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,column=0,columnspan=2,pady=20)

    add_button=Button(button_frame,text='Add',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:add_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))# in case of text area we need to pass indexing
    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(button_frame,text='Update',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:update_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    update_button.grid(row=0,column=1)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:clear(invoice_entry,name_entry,contact_entry,description_text))
    clear_button.grid(row=0,column=3)

    #--------------------------------------------------------------------------------------------------------------------------------------

    right_frame=Frame(supplier_frame,bg='white')
    right_frame.place(x=520,y=95,width=500,height=350)
    
    serach_frame=Frame(right_frame,bg='white')
    serach_frame.pack(pady=(0,20))

    num_label=Label(serach_frame,text="Invoice No.",font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,15),sticky='w')
    search_entry=Entry(serach_frame,font=('times new roman',14),bg='lightyellow',width=12)
    search_entry.grid(row=0,column=1,pady=10)

    search_button=Button(serach_frame,text='Search',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0,column=2,padx=15)

    show_button=Button(serach_frame,text='Show All',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:show_all(treeview,search_entry))
    show_button.grid(row=0,column=3)

    

    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)
    #yscrollcommand=scrolly.set,xscrollcommand=scrollx.set for connect them to treeview

    treeview=ttk.Treeview(right_frame,column=('invoice','name','contact','description'),show='headings',yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)# show will remove extra index in treeview

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)

    treeview.pack(fill=BOTH,expand=1)


    #adding headings in treeview
    treeview.heading('invoice',text='Invoice Id')
    treeview.heading('name',text='Supplier Name')
    treeview.heading('contact',text='Supplier Contact')
    treeview.heading('description',text='Description')

    #giving treeview column sizes

    treeview.column('invoice',width=80)
    treeview.column('name',width=160)
    treeview.column('contact',width=120)
    treeview.column('description',width=300)

    #this will always show the data in treeview after clicking supplier button

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview))

    return supplier_frame