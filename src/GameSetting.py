import Tkinter as tk

# root window
root = tk.Tk()

# getting system screen's height in pixels
system_height = str(root.winfo_screenheight())
height_value = 0

# getting system screen's width in pixels
system_width = str(root.winfo_screenwidth())
width_value = 0

playerName = ''

full_screen = False


def get_setting_info():
    return (full_screen ,int(width_value), int(height_value), str(playerName))

def close_setting_window():
    root.withdraw()
    
def reopen_setting_window():
    root.deiconify()

def run_setting():
    def change_setting():
        global width_value, height_value, full_screen, playerName
        
        if (current_full_screen_value.get()):
            width_value = system_width
            height_value = system_height
            full_screen = True
        else:
            width_value = get_current_width_value()
            height_value = get_current_height_value()
            full_screen = False
        
        playerName = name_var.get()
        
        root.quit()

    # This Window Opens at (300,300)
    root.geometry('700x400+300+300')
    root.resizable(False, False)
    root.title('Game Setting')


    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)



    # slider current value
    current_width_value = tk.IntVar()
    current_width_value.set(600)
    current_height_value = tk.IntVar()
    current_height_value.set(600)
    
    name_var=tk.StringVar()
    name_var.set('Anonymous')


    def get_current_width_value():
        return str(current_width_value.get())

    def get_current_height_value():
        return str(current_height_value.get())


    def width_slider_changed(event):
        current_width_value_label.configure(text='Width Value: ' + get_current_width_value())
        
    def height_slider_changed(event):
        current_height_value_label.configure(text='Height Value: ' + get_current_height_value())


    # label for the slider
    slider_width_label = tk.Label(
        root,
        text='Window Width:'
    )

    slider_width_label.grid(
        column=0,
        row=0,
        sticky='e',
        pady=20
    )

    slider_height_label = tk.Label(
        root,
        text='Window Height:'
    )

    slider_height_label.grid(
        column=0,
        row=2,
        sticky='e',
        pady=20
    )

    #  slider
    width_slider = tk.Scale(
        root,
        from_=600,
        to=system_width,
        orient='horizontal',  # vertical
        command=width_slider_changed,
        variable=current_width_value
    )

    width_slider.grid(
        column=1,
        row=0,
        sticky='we',
        padx=80
    )

    height_slider = tk.Scale(
        root,
        from_=600,
        to=system_height,
        orient='horizontal',  # vertical
        command=height_slider_changed,
        variable=current_height_value
    )

    height_slider.grid(
        column=1,
        row=2,
        sticky='we',
        padx=80
    )

    # current value label
    current_width_value_label = tk.Label(
        root,
        text='Width Value: ' + get_current_width_value()
    )

    current_width_value_label.grid(
        row=1,
        columnspan=2,
        sticky='n',
        ipadx=10,
        ipady=10
    )

    current_height_value_label = tk.Label(
        root,
        text='Height Value: ' + get_current_height_value()
    )

    current_height_value_label.grid(
        row=3,
        columnspan=2,
        sticky='n',
        ipadx=10,
        ipady=10
    )


    # checkbutton of full screen
    current_full_screen_value = tk.BooleanVar()

    # label for the checkbutton
    checkbutton_label = tk.Label(
        root,
        text='Full Screen:'
    )

    checkbutton_label.grid(
        column=0,
        row=4,
        sticky='e',
        pady=20
    )

    # checkbutton
    full_screen_checkbutton = tk.Checkbutton(
        root,
        variable = current_full_screen_value,
        onvalue = True,
        offvalue = False
    )

    full_screen_checkbutton.grid(
        column=1,
        row=4,
        sticky='we',
        padx=80
    )
    
    name_label = tk.Label(root, text = 'Player Name:')
    name_entry = tk.Entry(root,textvariable = name_var)
    
    name_label.grid(row=5,column=0, sticky='e', pady=20)
    name_entry.grid(row=5,column=1, pady=20)
    

    # button
    ok_button = tk.Button(
        root,
        text = "Create Game",
        command = change_setting
    )

    ok_button.grid(
        row=6,
        columnspan=3,
        sticky='ns'
    )

    root.mainloop()

# ********* Run as callback function in main ********* 
# import WindowsSizeSetting

# WindowsSizeSetting.run_setting()
# width, height = WindowsSizeSetting.get_setting_info()
# print("Changed screen size to: " + width + " x " + height)
# WindowsSizeSetting.close_setting_window()

if __name__ == '__main__':

    run_setting()