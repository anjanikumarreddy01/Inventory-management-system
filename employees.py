from tkinter import*
from tkinter import messagebox
from tkinter import ttk # for combobox, treeview 
from tkcalendar import DateEntry
import pymysql


def connect_database():
    try:    
        connection=pymysql.connect(host='localhost',user='root',passwd='1June@')
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error','Database is not connected try again')
        return None,None
    return cursor,connection

def create_database_table():
    cursor,connection=connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data(empid INT PRIMARY KEY, name VARCHAR(100),\
                   email VARCHAR(100),gender VARCHAR(50) ,dob VARCHAR(30),contact VARCHAR(30),employement_type VARCHAR(50),\
                   education varchar(50),work_shift VARCHAR(50),address VARCHAR(100),doj VARCHAR(30),salary VARCHAR(50),usertype VARCHAR(50),password VARCHAR(50))')

#to show data in top frame 
def treeview_data():
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_records=cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()



def select_data(event,empid_entry,name_entry,email_entry,\
                                        dob_date_entry,gender_combobox,contact_entry,employment_type_combobox,\
                                            education_combobox,work_shift_combobox,address_text,doj_date_entry,\
                                            salary_entry,user_type_combobox,password_entry):
    index=employee_treeview.selection()
    content=employee_treeview.item(index)
    row=content['values']
    clear_fileds(empid_entry,name_entry,email_entry,\
                                        dob_date_entry,gender_combobox,contact_entry,employment_type_combobox,\
                                            education_combobox,work_shift_combobox,address_text,doj_date_entry,\
                                            salary_entry,user_type_combobox,password_entry,False)

    empid_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0,row[5])
    employment_type_combobox.set(row[6])
    education_combobox.set(row[7])
    work_shift_combobox.set(row[8])
    address_text.insert(1.0,row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0,row[11])
    user_type_combobox.set(row[12])
    password_entry.insert(0,row[13])


def add_employee(empid,name,email,gender,dob,contact,employment_type,education,work_shift,address,doj,salary,user_type,password):
    if(empid=='' or name=='' or email==''or gender=='Select Gender' or contact=='' or employment_type=='Type' or education=='EducationType' or\
          work_shift=='Type Shift' or address=='\n' or salary=='' or user_type=='Select User Type' or password==''):
        messagebox.showerror('Error','All Fileds Are Required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        try:
            cursor.execute('SELECT empid from employee_data WHERE empid=%s',(empid))# shwoing error as person is alrady exist
            if cursor.fetchone():
                messagebox.showerror('Error','Id alrady exists')
                return
            address=address.strip()# it won't add \n in address end while inserting data
            cursor.execute('INSERT INTO employee_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(empid,name,email,gender,dob,contact,employment_type,education,work_shift,address,doj,salary,user_type,password))
            connection.commit()
            treeview_data()
            messagebox.showinfo('success','Data is inserted successfully')
        except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()



def clear_fileds(empid_entry,name_entry,email_entry,\
                dob_date_entry,gender_combobox,contact_entry,employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,\
               salary_entry,user_type_combobox,password_entry,check):
    
    
    empid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    from datetime import date
    dob_date_entry.set_date(date.today())
    gender_combobox.set('Select Gender')
    contact_entry.delete(0,END)
    employment_type_combobox.set('Type')
    education_combobox.set('EducationType')
    work_shift_combobox.set('Type Shift')
    address_text.delete(1.0,END)
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0,END)
    user_type_combobox.set('Select User Type')
    password_entry.delete(0,END)
    if check:
        employee_treeview.selection_remove(employee_treeview.selection())


def update_employee(empid, name, email, gender, dob, contact, employment_type,
                    education, work_shift, address, doj, salary, user_type, password):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
        return
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:

            cursor.execute('USE inventory_system')
            cursor.execute('SELECT * FROM employee_data WHERE empid=%s',(empid,))# for checking the changes to use update button
            current_data=cursor.fetchone()
            current_data=current_data[1:]
            address=address.strip()

            new_data=(name, email, gender, dob, contact, employment_type,
                            education, work_shift, address, doj, salary, user_type, password)
            
            if current_data== new_data:
                messagebox.showinfo('Information','No changes detected')
                return

            cursor.execute(
                '''
                UPDATE employee_data
                SET name=%s, email=%s, gender=%s, dob=%s, contact=%s,
                    employement_type=%s, education=%s, work_shift=%s, address=%s, doj=%s,
                    salary=%s, usertype=%s, password=%s
                WHERE empid=%s
                ''',
                (name, email, gender, dob, contact, employment_type, education,
                work_shift, address, doj, salary, user_type, password, empid)
            )

            connection.commit()
            treeview_data()
            messagebox.showinfo('Success', 'Data is updated successfully')
        except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()




def delete_employee(empid,):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
        return
    else:
        result=messagebox.askyesno('Conform','Do you really want to delete the record')# asking are you sure to delete the record 
        if result:    # if yes i will delete
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            
            try:
                cursor.execute('USE inventory_system')
                cursor.execute('DELETE FROM employee_data WHERE empid=%s',(empid,))
                connection.commit()
                treeview_data()
                messagebox.showinfo('Succuss','Record is deleted')
            except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()
            

    
def search_employee(search_option,value):
    if search_option=='Search by':
        messagebox.showerror('Error','No option is selected')
    elif value=='':
        messagebox.showerror('Error','Enter the value to search')
    else:
        print(search_option,value)
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute(f'SELECT * FROM employee_data WHERE {search_option} like %s',f'%{value}%')
        records=cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())# for delete all visiable data in treeview
        for record in records:
            employee_treeview.insert('',END,value=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def show_all(search_entry,search_combobox):
    treeview_data()# show all records in treeview 
    search_entry.delete(0,END)
    search_combobox.set('Search By')





































#----------------------------------------------------------------------------------------------------------------------------------------------
#main form

def employee_form(window):
    employee_frame=Frame(window,width=1070,height=567,bg='white')
    employee_frame.place(x=200,y=98)
    # heading leable 
    heading_label=Label(employee_frame,text="Manage Employee Details",font=("times new roman",16,'bold'),bg="#7A79E8",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    
    # lambda function will help to destroy the complete frame when you click the button 
    # top frame 
    top_frame=Frame(employee_frame,bg="white")
    top_frame.place(x=0,y=40,relwidth=1,height=235)
#-------------------------------------------------------------------------------------
    # In top frame again i will add "search frame" inside it 
    global back_icon,employee_treeview
    back_icon=PhotoImage(file='back_icon.png')
    back_button=Button(top_frame,bg='white',image=back_icon,bd=0,cursor='hand2',command=lambda:employee_frame.place_forget())
    back_button.place(x=10,y=0)

    search_frame=Frame(top_frame,bg='white')
    search_frame.pack()

    #combobox
    #justify will ne used to make everthing in frame to center as you types it will increase length left and right at same time
    search_combobox=ttk.Combobox(search_frame,values=('Empid','Name','Email','Gender','Contact','Employemnet Type','Work_Shift','User Type'),font=('times new roman',12),state='readonly',justify='center')# state will help stop typing in combobox
    search_combobox.grid(row=0,column=0,padx=20)
    search_combobox.set('Search By')

    #entry
    search_entry=Entry(search_frame,font=('times new roman',12),bg='lightyellow')
    search_entry.grid(row=0,column=1,padx=20)

    #search button
    search_button=Button(search_frame,text='SEARCH',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#7A79E8',command=lambda : search_employee(search_combobox.get(),search_entry.get()))
    search_button.grid(row=0,column=2,padx=20)


    #show all button
    showall_button=Button(search_frame,text='Show ALL',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:show_all(search_entry,search_combobox))
    showall_button.grid(row=0,column=3)

    # creating scroll bars for treeview
    horizontal_scrollbax=Scrollbar(top_frame,orient='horizontal')
    vertical_scrollbar=Scrollbar(top_frame,orient='vertical')


    # tree view 
    employee_treeview=ttk.Treeview(top_frame,columns=('empid','name','email','gender','dob','contact','employement_type','education','work_shift','address','doj','salary','usertype'),show='headings',
                                   yscrollcommand=vertical_scrollbar.set,xscrollcommand=horizontal_scrollbax.set)
    
    horizontal_scrollbax.pack(side='bottom',fill=X)
    vertical_scrollbar.pack(side='right',fill=Y,pady=(10,0))
    horizontal_scrollbax.config(command=employee_treeview.xview)# it will connect to scroll 
    vertical_scrollbar.config(command=employee_treeview.yview)


    employee_treeview.pack(pady=(10,0))

    employee_treeview.heading('empid',text='Empid')
    employee_treeview.heading('name',text='Name')
    employee_treeview.heading('email',text='Email')
    employee_treeview.heading('gender',text='Gender')
    employee_treeview.heading('contact',text='Contact')
    employee_treeview.heading('dob',text='Date of Birth')
    employee_treeview.heading('employement_type',text='Employemnet Type')
    employee_treeview.heading('education',text='Education')
    employee_treeview.heading('work_shift',text='Work_Shift')
    employee_treeview.heading('address',text='Address')
    employee_treeview.heading('doj',text='Date of Joining')
    employee_treeview.heading('salary',text='Salary')
    employee_treeview.heading('usertype',text='User Type')

    # giving width to colomns

    employee_treeview.column('empid',width=60)
    employee_treeview.column('name',width=130)
    employee_treeview.column('email',width=140)
    employee_treeview.column('gender',width=80)
    employee_treeview.column('contact',width=100)
    employee_treeview.column('dob',width=100)
    employee_treeview.column('employement_type',width=120)
    employee_treeview.column('education',width=120)
    employee_treeview.column('work_shift',width=100)  
    employee_treeview.column('address',width=200)
    employee_treeview.column('doj',width=100)
    employee_treeview.column('salary',width=140)
    employee_treeview.column('usertype',width=120) 

    treeview_data()
    

    #-------------------------------------------------------------------------------------------------

    #bottom frame
    bottom_frame=Frame(employee_frame,bg='white')
    bottom_frame.place(x=20,y=280,relwidth=1,height=268)

    empid_label=Label(bottom_frame,text="EmpId",font=('times new roman',12),bg='white')
    empid_label.grid(row=0,column=0,padx=20,pady=10,sticky='w')
    empid_entry=Entry(bottom_frame,font=('times new roman',12),bg='lightyellow')
    empid_entry.grid(row=0,column=1,padx=20,pady=10)

    name_label=Label(bottom_frame,text="Name",font=('times new roman',12),bg='white')
    name_label.grid(row=0,column=2,padx=20,pady=10,sticky='w')
    name_entry=Entry(bottom_frame,font=('times new roman',12),bg='lightyellow')
    name_entry.grid(row=0,column=3,padx=20,pady=10)

    email_label=Label(bottom_frame,text="Email",font=('times new roman',12),bg='white')
    email_label.grid(row=0,column=4,padx=20,pady=10,sticky='w')
    email_entry=Entry(bottom_frame,font=('times new roman',12),bg='lightyellow')
    email_entry.grid(row=0,column=5,padx=20,pady=10)


    gender_label=Label(bottom_frame,text="Gender",font=('times new roman',12),bg='white')
    gender_label.grid(row=1,column=0,padx=20,pady=10,sticky='w')

    gender_combobox=ttk.Combobox(bottom_frame,values=('Male','Female'),font=('times new roman',12),width=18,state='readonly')# state will help stop typing in combobox
    gender_combobox.grid(row=1,column=1,padx=10,pady=10)
    gender_combobox.set('Select Gender')


    Dob_label=Label(bottom_frame,text="Date Of Birth",font=('times new roman',12),bg='white')
    Dob_label.grid(row=1,column=2,padx=20,pady=10,sticky='w')
    dob_date_entry=DateEntry(bottom_frame,font=('times new roman',12),width=18,state='readonly',date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1,column=3,padx=20,pady=10)

    contact_label= Label(bottom_frame,text='Contact',font=('times new roman',12),bg='white')
    contact_label.grid(row=1,column=4,padx=20,pady=10,sticky='w')
    contact_entry=Entry(bottom_frame,font=('times new roman',12),bg='lightyellow')
    contact_entry.grid(row=1,column=5,padx=20,pady=10)

    employment_type_label=Label(bottom_frame,text="Employment Type",font=('times new roman',12),bg='white')
    employment_type_label.grid(row=2,column=0,padx=20,pady=10,sticky='w')
    employment_type_combobox=ttk.Combobox(bottom_frame,values=('Full Time','Part Time','Casual','Contract','Intern'),font=('times new roman',12),width=18,state='readonly')# state will help stop typing in combobox
    employment_type_combobox.grid(row=2,column=1,padx=20,pady=10)
    employment_type_combobox.set('Type')

    education_label=Label(bottom_frame,text="Education",font=('times new roman',12),bg='white')
    education_label.grid(row=2,column=2,padx=20,pady=10,sticky='w')
    education_combobox=ttk.Combobox(bottom_frame,values=('B.Tech','B.Com','M.Tech','M.Com','B.Sc','M.Sc',"BBA",'MBA','LLB','B.Arch','M.Arch'),font=('times new roman',12),width=18,state='readonly')# state will help stop typing in combobox
    education_combobox.grid(row=2,column=3,padx=20,pady=10)
    education_combobox.set('EducationType')

    work_shift_label=Label(bottom_frame,text="Work Shift",font=('times new roman',12),bg='white')
    work_shift_label.grid(row=2,column=4,padx=20,pady=10,sticky='w')
    work_shift_combobox=ttk.Combobox(bottom_frame,values=('Morning','Evening','Night'),font=('times new roman',12),width=18,state='readonly')# state will help stop typing in combobox
    work_shift_combobox.grid(row=2,column=5,padx=20,pady=10)
    work_shift_combobox.set('Type Shift')

    address_label=Label(bottom_frame,text="Address",font=('times new roman',12),bg='white')
    address_label.grid(row=3,column=0,padx=20,pady=10,sticky='w')
    address_text=Text(bottom_frame,width=20,height=3,font=('times new roman',12),bg='lightyellow',)
    address_text.grid(row=3,column=1,padx=20,pady=10,rowspan=2)

    Doj_label=Label(bottom_frame,text="Date Of Joining",font=('times new roman',12),bg='white')
    Doj_label.grid(row=3,column=2,padx=20,pady=10,sticky='w')
    doj_date_entry=DateEntry(bottom_frame,font=('times new roman',12),width=18,state='readonly',date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3,column=3,padx=20,pady=10)

    salary_label=Label(bottom_frame,text="Salary",font=('times new roman',12),bg='white')
    salary_label.grid(row=3,column=4,padx=20,pady=10,sticky='w')
    salary_entry=Entry(bottom_frame,font=('times new roman',12),bg='lightyellow')
    salary_entry.grid(row=3,column=5,padx=20,pady=10)

    user_type_label=Label(bottom_frame,text="User Type",font=('times new roman',12),bg='white')
    user_type_label.grid(row=4,column=2,padx=20,pady=10,sticky='w')
    user_type_combobox=ttk.Combobox(bottom_frame,values=('Admin','Employe'),font=('times new roman',12),width=18,state='readonly')# state will help stop typing in combobox
    user_type_combobox.grid(row=4,column=3,padx=20,pady=10)
    user_type_combobox.set('Select User Type')

    password_label=Label(bottom_frame,text="Password",font=('times new roman',12),bg='white')
    password_label.grid(row=4,column=4,padx=20,pady=10,sticky='w')
    password_entry=Entry(bottom_frame,font=('times new roman',12),bg='lightyellow')
    password_entry.grid(row=4,column=5,padx=20,pady=10)


    Button_frame=Frame(employee_frame,bg='white')
    Button_frame.place(x=200,y=520)

    add_button=Button(Button_frame,text='Add',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:add_employee(empid_entry.get(),\
                                    name_entry.get(),email_entry.get(),gender_combobox.get(),dob_date_entry.get(),contact_entry.get(),employment_type_combobox.get(),\
                                    education_combobox.get(),work_shift_combobox.get(),address_text.get(1.0,END),doj_date_entry.get(),salary_entry.get(),user_type_combobox.get(),password_entry.get()))
    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(Button_frame,text='Update',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:update_employee(empid_entry.get(),\
                                    name_entry.get(),email_entry.get(),gender_combobox.get(),dob_date_entry.get(),contact_entry.get(),employment_type_combobox.get(),\
                                    education_combobox.get(),work_shift_combobox.get(),address_text.get(1.0,END),doj_date_entry.get(),salary_entry.get(),user_type_combobox.get(),password_entry.get()))
    update_button.grid(row=0,column=1,padx=20)

    delete_button=Button(Button_frame,text='DELETE',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:delete_employee(empid_entry.get(),))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(Button_frame,text='Clear',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#7A79E8',command=lambda:clear_fileds(empid_entry,name_entry,email_entry,\
                                        dob_date_entry,gender_combobox,contact_entry,employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,\
                                            salary_entry,user_type_combobox,password_entry,True))
    clear_button.grid(row=0,column=3,padx=20)
    

    employee_treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,empid_entry,name_entry,email_entry,\
                                        dob_date_entry,gender_combobox,contact_entry,employment_type_combobox,\
                                            education_combobox,work_shift_combobox,address_text,doj_date_entry,\
                                            salary_entry,user_type_combobox,password_entry))# this is used to show data in bottom frame of employee who is selected in treeview
    
    create_database_table()

    return employee_frame