from tkinter import*
from employees import connect_database
from tkinter import ttk # for combobox, treeview
from tkinter import messagebox 


#this fuction for the selecting record in treeview and the record details will be filled in left frame
def select_data(Event,treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox):
    index=treeview.selection()# this will give the record you are selecting in treeview with you mouse
    dict=treeview.item(index)
    content=dict['values']
    # up to above we got the all data of the record we selcted in treeview
    #need to insert the data in left frame 

    #deleting exsisting dta in entry fields
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    discount_spinbox.delete(0,END)
    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0,content[3])
    price_entry.insert(0,content[4])
    discount_spinbox.insert(0,content[5])
    quantity_entry.insert(0,content[7])
    status_combobox.set(content[8])







def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
            return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT *FROM product_data')
        #next step is to insert data in treeview
        records=cursor.fetchall()# store all data from table in records verable
        treeview.delete(*treeview.get_children())# delete all current data in treeview
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to{e}')
    finally:
        cursor.close()
        connection.close()



def fetch_supplier_category(category_combobox,supplier_combobox):
    category_options=[]
    supplier_options=[]
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    

    cursor.execute('USE inventory_system')
    cursor.execute('select name from category_data')
    names=cursor.fetchall()
    if len(names)>0:
        category_combobox.set('Select')
        for name in names:
            category_options.append(name[0])
        category_combobox.config(values=category_options)# it will show category options in cateogry_combobox foe choose options


    cursor.execute('select name from supplier_data')
    names=cursor.fetchall()
    if len(names)>0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_options.append(name[0])
        supplier_combobox.config(values=supplier_options)# it will show supplier options in cateogry_combobox foe choose options




def add_product(category,supplier,name,price,discount,quantity,status,treeview):
    if category=='Empty':  
        messagebox.showerror('Error','Category field is not Selected')
    elif supplier=='Empty':
        messagebox.showerror('Error','Supplier field is not Selected')

    elif category=='Select' or supplier=='Select'or name=='' or price=='' or quantity==''or status=='Select Status':
        messagebox.showerror('Error','All fields need to be filled')
    
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data(id int AUTO_INCREMENT PRIMARY KEY,category VARCHAR(100),supplier VARCHAR(100),name VARCHAR(100),price DECIMAL(10,2),quantity int,status VARCHAR(50))')
    
        #checking wheather the record is alrady existing or not
        cursor.execute('SELECT * from product_data WHERE category=%s AND supplier=%s And name=%s',(category,supplier,name))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error','Product already exists')
            return
        
        discounted_price=round(float(price)*(1-int(discount)/100),2)

        cursor.execute('INSERT INTO product_data (category,supplier,name,price,discount,discounted_price,quantity,status) values(%s,%s,%s,%s,%s,%s,%s,%s)',(category,supplier,name,price,discount,discounted_price,quantity,status))
        connection.commit()
        messagebox.showinfo('Succuss','Data is added Successfully')
        treeview_data(treeview)


def update_product(category,supplier,name,price,discount,quantity,status,treeview):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    
    if not index:# checking weather the user had selected row or not
        messagebox.showerror('Error','No row is selected')
        return
    id=content[0]
    
    cursor,connection=connect_database()
    if not cursor or not connection:
            return 
    try:
        #checking any updates are there are not

        cursor.execute("USE inventory_system")
        #for checking the left frame for any changes if it finds it will update or else just show thw message that there are no changes
        cursor.execute('SELECT * FROM product_data WHERE id=%s',(id,))#it will give the id 
        current_data=cursor.fetchone() 
        current_data=current_data[1:]# removed invoice column as we not taken invoice in new_data 
        #for removing decimal type as due it it was not matching to compare with new data
        current_data=list(current_data)
        current_data[3]=str(current_data[3])#converted into string
        current_data[4]=str(current_data[4])#converted into string
        current_data=tuple(current_data)# converting back into
        quantity=int(quantity)

        new_data=(category,supplier,name,price,discount,quantity,status)
        if current_data==new_data:
            messagebox.showinfo('Info','No data is updated')
            return
        discounted_price=round(float(price)*(1-int(discount)/100),2)
        cursor.execute('UPDATE product_data SET category=%s,supplier=%s,name=%s,price=%s,discount=%s,discounted_price=%s,quantity=%s,status=%s WHERE id=%s',(category,supplier,name,price,discount,discounted_price,quantity,status,id))
        connection.commit()
        messagebox.showinfo('Info','Data is updated')
        treeview_data(treeview) #this will show updated data in treeview 
    except Exception as e:
        messagebox.showerror('Error',f'Error due to{e}')
    finally:
        cursor.close()
        connection.close()



def delete_product(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox,treeview):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    id=content[0] # for finding id
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    ans=messagebox.askyesno('Confirm','Do you really want to delete?')
    if ans:
        cursor,conncetion= connect_database()
        if not cursor or not conncetion:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute('DELETE FROM product_data WHERE id=%s',(id,))
            conncetion.commit()
            treeview_data(treeview)# for showing data after deletion
            messagebox.showinfo('Info','Record is deleted')
            clear(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox,treeview)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to{e}')
        finally:
            cursor.close()
            conncetion.close()


def clear(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox,treeview):
    treeview.selection_remove(treeview.selection())# it willhelp to unselect the record in treview box
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    status_combobox.set('Select Status')
    discount_spinbox.delete(0,END)
    discount_spinbox.insert(0,0)




def search_product(search_combobox,search_entry,treeview):
    if search_combobox.get()=='Search By':
        messagebox.showwarning('Warning','Please select an option')
    elif search_entry.get()=='':
        messagebox.showwarning('Warning','Please enter the value to search')
    else:
        cursor,conncetion= connect_database()
        if not cursor or not conncetion:
            return
        cursor.execute('USE inventory_system')
        cursor.execute(f"SELECT * FROM product_data WHERE {search_combobox.get()} LIKE %s",(f"%{search_entry.get()}%",))# for searchinfg for sindile alphabet
        records=cursor.fetchall()
        if len(records)==0:
            messagebox.showerror('Error','No records found')
            return

        treeview.delete(*treeview.get_children())# delete all current data in treeview
        for record in records:
            treeview.insert('',END,values=record)
        

def show_all(treeview,search_entry,search_combobox):
    treeview_data(treeview)
    search_combobox.set("Select By")
    search_entry.delete(0,END)
    




#-------------------main code----------------------------------------------------------------------------------------------------
def product_form(window):
    global back_icon,logo # ifnot globalit won't be visibel in frame
    product_frame=Frame(window,width=1070,height=567,bg='white')
    product_frame.place(x=200,y=98)

    back_icon=PhotoImage(file='back_icon.png')
    back_button=Button(product_frame,bg='white',image=back_icon,bd=0,cursor='hand2',command=lambda:product_frame.place_forget())
    back_button.place(x=10,y=0)

    #----------------------------------------------------------------------------------------------

    left_frame=Frame(product_frame,bg='white',bd=2,relief=RIDGE)
    left_frame.place(x=30,y=40)

    heading_label=Label(left_frame,text="Manage Product Details",font=("times new roman",16,'bold'),bg="#7A79E8",fg='white')
    heading_label.grid(row=0,column=0,columnspan=2,sticky='we')# due to sticky=we it fill completly "west and east"

    category_label=Label(left_frame,text="Category",font=('times new roman',14,'bold'),bg='white')
    category_label.grid(row=1,column=0,padx=20,pady=30,sticky='w')
    category_combobox=ttk.Combobox(left_frame,font=('times new roman',14,'bold'),width=18,state='readonly')
    category_combobox.grid(row=1,column=1)
    category_combobox.set('Empty')


    supplier_label=Label(left_frame,text="Supplier",font=('times new roman',14,'bold'),bg='white')
    supplier_label.grid(row=2,column=0,padx=20,sticky='w')
    supplier_combobox=ttk.Combobox(left_frame,font=('times new roman',14,'bold'),width=18,state='readonly')
    supplier_combobox.grid(row=2,column=1)
    supplier_combobox.set('Empty')

    name_label=Label(left_frame,text="Product Name",font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=3,column=0,padx=20,pady=30,sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=3,column=1,pady=30)

    price_label=Label(left_frame,text="Price",font=('times new roman',14,'bold'),bg='white')
    price_label.grid(row=4,column=0,padx=20,sticky='w')
    price_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    price_entry.grid(row=4,column=1)

    discount_label=Label(left_frame,text="Discount(%)",font=('times new roman',14,'bold'),bg='white')
    discount_label.grid(row=5,column=0,padx=20,sticky='w',pady=(30,0))
    discount_spinbox=Spinbox(left_frame,from_=0,to=100,font=('times new roman',14,'bold'),width=19)
    discount_spinbox.grid(row=5,column=1,pady=(30,0))

    quantity_label=Label(left_frame,text="Quantity",font=('times new roman',14,'bold'),bg='white')
    quantity_label.grid(row=6,column=0,padx=20,pady=30,sticky='w')
    quantity_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    quantity_entry.grid(row=6,column=1,pady=30)

    status_label=Label(left_frame,text="Status",font=('times new roman',14,'bold'),bg='white')
    status_label.grid(row=7,column=0,padx=20,sticky='w')
    status_combobox=ttk.Combobox(left_frame,values=('Active','Inactive'),font=('times new roman',14,'bold'),width=18,state='readonly')
    status_combobox.grid(row=7,column=1)
    status_combobox.set('Select Status')

    #-----------button frame------------------------------------------------------------
    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=8,columnspan=2,pady=(30,10))

    add_button=Button(button_frame,text='Add',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:add_product(category_combobox.get(),
                                                    supplier_combobox.get(),name_entry.get(),price_entry.get(),discount_spinbox.get(),quantity_entry.get(),status_combobox.get(),treeview))
    add_button.grid(row=0,column=0,padx=10)

    update_button=Button(button_frame,text='Update',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:update_product(category_combobox.get(),
                                                    supplier_combobox.get(),name_entry.get(),price_entry.get(),discount_spinbox.get(),quantity_entry.get(),status_combobox.get(),treeview))
    update_button.grid(row=0,column=1,padx=10)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:delete_product(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox,treeview))
    delete_button.grid(row=0,column=2,padx=10)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:clear(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox,treeview))
    clear_button.grid(row=0,column=3,padx=10)


    #----------------------search frame----------------------------------------------------------------------------------

    search_frame=LabelFrame(product_frame,text='Search product',font=('times new roman',14),bg='white')# labelframe is diff from frame
    search_frame.place(x=480,y=40)
    search_combobox=ttk.Combobox(search_frame,values=('Category','Supplier','Name','Status'),font=('times new roman',14),width=16,state='readonly')
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set('Search By')

    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='lightyellow',width=16)
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:search_product(search_combobox,search_entry,treeview))
    search_button.grid(row=0,column=2,padx=(10,0),pady=10)

    showall_button=Button(search_frame,text='Showall',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:show_all(treeview,search_entry,search_combobox))
    showall_button.grid(row=0,column=3,padx=10)

    #------------------------treeview frame-------------------------------------------------------------------------------------------
    treeview_frame=Frame(product_frame,bg='white')
    treeview_frame.place(x=480,y=125,width=570,height=430)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    #yscrollcommand=scrolly.set,xscrollcommand=scrollx.set for connect them to treeview

    treeview=ttk.Treeview(treeview_frame,column=('id','category','supplier','name','price','discount','discounted_price','quantity','status'),show='headings',yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)# show will remove extra index in treeview

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)

    treeview.pack(fill=BOTH,expand=1)

     #adding headings in treeview

    treeview.heading('id',text='Id')
    treeview.heading('category',text='Category')
    treeview.heading('supplier',text='Supplier')
    treeview.heading('name',text='Product Name')
    treeview.heading('price',text='Price')
    treeview.heading('discount',text='Discount')
    treeview.heading('discounted_price',text='Discounted Price')
    treeview.heading('quantity',text='Quantity')
    treeview.heading('status',text='Status')

    #giving treeview column sizes
    treeview.column('id',width=80)
    # treeview.column('category',width=80)
    #treeview.column('supplier',width=100)
    #treeview.column('name',width=100)
    # treeview.column('price',width=80)
    # treeview.column('quantity',width=80)
    # treeview.column('status',width=80)
    fetch_supplier_category(category_combobox,supplier_combobox)
    treeview_data(treeview)

    #binding select data fuction with treeview 
    treeview.bind('<ButtonRelease-1>',lambda Event:select_data(Event,treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox))
    
    return product_frame







    