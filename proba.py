import tkinter as tk

def check_states():
    print("Option 1:", var1.get())
    print("Option 2:", var2.get())
    print("Option 3:", var3.get())

# Create the main window
root = tk.Tk()
root.title("Radio Buttons Example")

# Create three IntVar variables to hold the state of each radio button
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()

# Initialize the first variable to 1 (checked), and the others to 0 (unchecked)
var1.set(1)

# Create three radio buttons with different text and associate each one with a variable
radio1 = tk.Radiobutton(root, text="Option 1", variable=var1, value=1)
radio2 = tk.Radiobutton(root, text="Option 2", variable=var2, value=2)
radio3 = tk.Radiobutton(root, text="Option 3", variable=var3, value=3)

# Place the radio buttons in the window
radio1.pack()
radio2.pack()
radio3.pack()

# Create a button to check the state of the radio buttons
check_button = tk.Button(root, text="Check States", command=check_states)
check_button.pack()

# Start the Tkinter event loop
root.mainloop()

