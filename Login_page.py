from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os # To run another python file

# It's good practice to have the database connection function in a separate utility file,
# but since your project already has it in employees.py, we will import it from there.
from employees import connect_database


class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.title("Login")
        # Set the window size to match your main dashboard
        self.window.geometry('1270x668+0+0')
        self.window.resizable(0, 0)

        # ========================================================================
        # ====================  BACKGROUND & HEADER ==============================
        # ========================================================================
        
        # Main blue header
        self.header_frame = Frame(self.window, bg="#0078D7")
        self.header_frame.place(x=0, y=0, relwidth=1, height=100)
        
        title_label = Label(self.header_frame, text="Inventory Management System", font=('arial', 30, 'bold'), bg="#0078D7", fg='white')
        title_label.pack(pady=20)

        # Main content frame
        self.content_frame = Frame(self.window, bg="white")
        self.content_frame.place(x=0, y=100, relwidth=1, relheight=1)

        # ========================================================================
        # ==================== LEFT SIDE ANIMATED IMAGES =========================
        # ========================================================================

        self.left_frame = Frame(self.content_frame, bg="white")
        self.left_frame.place(x=50, y=50, width=600, height=450)

        # --- IMAGE SETUP ---
        # INSTRUCTIONS:
        # 1. Create a folder named 'images' in the same directory as this script.
        # 2. Place your 3-4 PNG images inside this 'images' folder.
        # 3. Make sure the images are 254x254 pixels for the best look.
        # 4. Update the self.image_files list below with the names of your image files.
        self.image_files = [
            'image_1.png',
            'image_2.png',
            'image_3.png'
        ]
        
        # Check if the image files exist, otherwise use placeholders
        for i, path in enumerate(self.image_files):
            if not os.path.exists(path):
                print(f"Warning: Image file not found at '{path}'. A placeholder will be used.")
                # Create a placeholder if the image is missing
                placeholder_img = Image.new('RGB', (254, 254), color = 'grey')
                placeholder_img.save(path) # Save the placeholder so it can be loaded
        
        self.current_image_index = 0
        self.photo_images = [ImageTk.PhotoImage(Image.open(img).resize((400, 400), Image.LANCZOS)) for img in self.image_files]
        
        self.image_label = Label(self.left_frame, bg="white")
        self.image_label.pack(pady=20)

        self.animate_images() # Start the animation

        # ========================================================================
        # ==================== RIGHT SIDE LOGIN FORM =============================
        # ========================================================================

        self.right_frame = Frame(self.content_frame, bg="#F0F0F0", bd=2, relief=RIDGE)
        self.right_frame.place(x=750, y=30, width=450, height=480)

        # --- PROFILE ICON ---
        # INSTRUCTIONS: Place your profile icon here. Recommended size: 124x124 pixels.
        try:
            profile_img_path = 'profile.png'
            if not os.path.exists(profile_img_path):
                 # Create a placeholder if the image is missing
                placeholder_img = Image.new('RGB', (124, 124), color = 'darkgrey')
                placeholder_img.save(profile_img_path)
            
            self.profile_icon = ImageTk.PhotoImage(Image.open(profile_img_path).resize((124, 124), Image.LANCZOS))
            profile_label = Label(self.right_frame, image=self.profile_icon, bg="#F0F0F0")
            profile_label.pack(pady=20)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load profile icon: {e}", parent=self.window)


        # --- Employee ID ---
        id_label = Label(self.right_frame, text="Employee Id", font=('arial', 14), bg="#F0F0F0")
        id_label.pack(padx=50, anchor='w')
        
        self.id_entry = Entry(self.right_frame, font=('arial', 14), bg='white')
        self.id_entry.pack(padx=50, pady=(5, 20), fill='x')

        # --- Password ---
        password_label = Label(self.right_frame, text="Password", font=('arial', 14), bg="#F0F0F0")
        password_label.pack(padx=50, anchor='w')
        
        self.password_entry = Entry(self.right_frame, font=('arial', 14), bg='white', show='*')
        self.password_entry.pack(padx=50, pady=5, fill='x')

       
        # --- Forgot Password ---
        forgot_password_link = Label(self.right_frame, text="Forgot Password?", font=('arial', 11, 'underline'), bg="#F0F0F0", fg="blue", cursor="hand2")
        forgot_password_link.pack(padx=50, pady=(0, 20), anchor='e')
        # Bind the click event to the new function
        forgot_password_link.bind("<Button-1>", self.forgot_password_action)

        
        # --- Login Button ---
        login_button = Button(self.right_frame, text="Login", font=('arial', 16, 'bold'), bg="#0078D7", fg="white", cursor="hand2", command=self.login_check)
        login_button.pack(padx=50, pady=20, fill='x', ipady=5)


    # You can delete this entire function

    def animate_images(self):
        """Cycles through the images every 2 seconds."""
        self.image_label.config(image=self.photo_images[self.current_image_index])
        self.current_image_index = (self.current_image_index + 1) % len(self.photo_images)
        self.window.after(2000, self.animate_images) # Call this function again after 2000ms (2 seconds)

    def forgot_password_action(self, event):
        """Shows a funny message when the 'Forgot Password' link is clicked."""
        messagebox.showinfo("Ni batuku ayipoyindi le", "Niku chekkuthadu le eroju. admin ki call chey inka.", parent=self.window)


    def login_check(self):
        """Validates user credentials against the database."""
        emp_id = self.id_entry.get()
        password = self.password_entry.get()

        if emp_id == "" or password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.window)
            return

        cursor, connection = connect_database()
        if not cursor or not connection:
            # The connect_database function already shows an error message
            return
        
        try:
            cursor.execute('USE inventory_system')
            # Query to find a user with matching empid and password
            cursor.execute('SELECT usertype FROM employee_data WHERE empid=%s AND password=%s', (emp_id, password))
            user_record = cursor.fetchone()

            if user_record:
                user_type = user_record[0]
                if user_type == 'Admin':
                    messagebox.showinfo("Success", "Welcome Admin!", parent=self.window)
                    self.window.destroy() # Close the login window
                    # Run the main dashboard script
                    os.system("python inventory_management_system.py") 
                elif user_type == 'Employe': # Note: Your table uses 'Employe', not 'Employee'
                    messagebox.showinfo("Success", "Welcome Employee!", parent=self.window)
                    # Here you would launch the employee-specific billing dashboard
                    # For now, we'll just close the login window
                    self.window.destroy()
                    os.system("python billing.py")
                else:
                    messagebox.showerror("Error", "Unknown user type.", parent=self.window)
            else:
                messagebox.showerror("Error", "Invalid Employee ID or Password", parent=self.window)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=self.window)
        finally:
            if connection.open:
                cursor.close()
                connection.close()


if __name__ == "__main__":
    root = Tk()
    app = LoginPage(root)
    root.mainloop()