from tkinter import*
from employees import connect_database
from tkinter import ttk # for combobox, treeview
from tkinter import messagebox 
 
def clear(id_entry,category_name_entry,description_text):
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)



def delete_category(treeview):
    index=treeview.selection()
    content=treeview.item(index)
    row=content['values']
    id=row[0]
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor,conncetion= connect_database()
    if not cursor or not conncetion:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM category_data WHERE id=%s',(id,))
        conncetion.commit()
        treeview_data(treeview)# for showing data after deletion
        messagebox.showinfo('Info','Record is deleted')
    except Exception as e:
        messagebox.showerror('Error',f'Error due to{e}')
    finally:
        cursor.close()
        conncetion.close()






 #for showing data in treeview
def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
            return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT *FROM category_data')
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


def add_category(id,name,description,treeview):
    if id=='' or name=='' or description=='':
        messagebox.showerror('Error','All fileds are required')
    else:
        cursor,connection=connect_database()# connecting database
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')

            #creating table if not exists
            cursor.execute('CREATE TABLE IF NOT EXISTS category_data (id int primary key,name varchar(100),description TEXT)')
            #checking wheather the id is already exists or not
            cursor.execute('SELECT *FROM category_data WHERE id=%s',id)
            if cursor.fetchone():
                    messagebox.showerror('Error','Id already exists')
                    return
            # query to insert data
            cursor.execute('INSERT INTO category_data VALUES(%s,%s,%s)',(id,name,description))
            connection.commit()
            messagebox.showinfo('Info','Data is inserted')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to{e}')
        finally:
            cursor.close()
            connection.close()




#------------------------main code--------------------------------------------------------------------------------

def category_form(window):
    global back_icon,logo # ifnot globalit won't be visibel in frame
    category_frame=Frame(window,width=1070,height=567,bg='white')
    category_frame.place(x=200,y=98)
    # heading leable 
    heading_label=Label(category_frame,text="Manage Category Details",font=("times new roman",16,'bold'),bg="#7A79E8",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    back_icon=PhotoImage(file='back_icon.png')
    back_button=Button(category_frame,bg='white',image=back_icon,bd=0,cursor='hand2',command=lambda:category_frame.place_forget())
    back_button.place(x=10,y=30)

    logo=PhotoImage(file='product_category.png')
    label=Label(category_frame,image=logo,bg='white')
    label.place(x=30,y=100)

    #---------------------------------------------------------------------------------------------------------
    details_frame=Frame(category_frame,bg='white')
    details_frame.place(x=500,y=60)

    id_label=Label(details_frame,text="Category Id",font=('times new roman',14,'bold'),bg='white')
    id_label.grid(row=0,column=0,padx=20,sticky='w')
    id_entry=Entry(details_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    id_entry.grid(row=0,column=1)

    category_name_label=Label(details_frame,text="Category Name",font=('times new roman',14,'bold'),bg='white')
    category_name_label.grid(row=1,column=0,padx=20,sticky='w')
    category_name_entry=Entry(details_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    category_name_entry.grid(row=1,column=1,pady=20)

    description_label=Label(details_frame,text="Description",font=('times new roman',14,'bold'),bg='white')
    description_label.grid(row=2,column=0,padx=20,sticky='nw')

    description_text=Text(details_frame,width=25,height=6,bd=2,bg='lightyellow')
    description_text.grid(row=2,column=1)

    #------------------button frame-----------------------------------------------------------------------
    button_frame=Frame(category_frame,bg='white')
    button_frame.place(x=580,y=280)

    add_button=Button(button_frame,text='Add',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:add_category(id_entry.get(),category_name_entry.get(),description_text.get(1.0,END).strip(),treeview))# we willuse .get() for insert data in sql    add_button.grid(row=0,column=0,padx=20)
    add_button.grid(row=0,column=0,padx=20)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:delete_category(treeview))
    delete_button.grid(row=0,column=1,padx=20)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:clear(id_entry,category_name_entry,description_text))
    clear_button.grid(row=0,column=2,padx=20)
    #------------------------------------------------------------------------------------------
    treeview_frame=Frame(category_frame)
    treeview_frame.place(x=530,y=340,height=200,width=500)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    #yscrollcommand=scrolly.set,xscrollcommand=scrollx.set for connect them to treeview

    treeview=ttk.Treeview(treeview_frame,column=('id','name','description'),show='headings',yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)# show will remove extra index in treeview

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)

    treeview.pack(fill=BOTH,expand=1)
    #-------------------------------------------------------------
     #adding headings in treeview
    treeview.heading('id',text='Category Id')
    treeview.heading('name',text='Category Name')
    treeview.heading('description',text='Description')

    #giving treeview column sizes

    treeview.column('id',width=80)
    treeview.column('name',width=140)
    treeview.column('description',width=300)

    treeview_data(treeview)

    return category_frame