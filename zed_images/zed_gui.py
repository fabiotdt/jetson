from typing import Any
import cv2
import numpy
import pyzed.sl as sl
from tkinter import *
from PIL import Image, ImageTk
import os
import csv
import datetime
import pandas as pd

class storing_data():
    def __init__(self):
        base_root = '/media/jetson/TDTF_sd/Data_measurments' # Linux
        #base_root =  'C:\\Users\\fabio\\Desktop\\Data_measurments' # Windows
        self.left_img = os.path.join(base_root, 'left_image')
        self.right_img = os.path.join(base_root, 'right_image')
        self.dataset = os.path.join(base_root, 'dataset')

class ZedVideoApp:
    def __init__(self, root):
        
        self.root = root
        
        # Get the screen width and height
        self.wsh = self.root.winfo_screenheight()
        self.wsw = self.root.winfo_screenwidth()

        # Create a ZED camera object        
        self.zedCamera = sl.Camera()
        # Creating initial parameters
        init_params = sl.InitParameters()
        init_params.camera_resolution = sl.RESOLUTION.HD720 # Image Resolution (HD2K, HD1080, HD720, SVGA, VGA)
        init_params.camera_fps = 30
        
        status = self.zedCamera.open(init_params)
        if status != sl.ERROR_CODE.SUCCESS:
            print(f"Error (status): Unable to Opne Zed camera")
            self.root.destroy()
            return

        self.res = sl.Resolution()
        self.res.width = self.zedCamera.get_camera_information().camera_configuration.resolution.width
        self.res.height = self.zedCamera.get_camera_information().camera_configuration.resolution.height
        
        # Create a video frame on the right
        self.video_frame = Frame(self.root, width=int(self.wsw/2))
        self.video_frame.grid(row=6, column=3, rowspan= 15, columnspan=3, padx=10, pady=20)
        self.video_label = Label(self.video_frame)
        self.video_label.pack()
        
        self.update_video_stream()
        
    def update_video_stream(self):

        self.zedCamera.grab()
        image_l = sl.Mat()
        self.zedCamera.retrieve_image(image_l, sl.VIEW.LEFT)

        prop = self.res.width/self.res.height

        new_w = int(self.wsw/4.5)
        new_h = int(new_w*prop)

        image_l_display = image_l.get_data()
        image_l_display = cv2.resize(image_l_display, (new_h, new_w))
        image_l_display = cv2.cvtColor(image_l_display, cv2.COLOR_BGR2RGB)

        photo = ImageTk.PhotoImage(image=Image.fromarray(image_l_display))
        self.video_label.config(image=photo)
        self.video_label.image = photo
        self.video_frame.update()

        self.root.after(5, self.update_video_stream)

    def submit_action(self, root, name):
        
        image_l = sl.Mat()
        image_r = sl.Mat()

        self.zedCamera.retrieve_image(image_l, sl.VIEW.LEFT)
        self.zedCamera.retrieve_image(image_r, sl.VIEW.RIGHT)

        # Save the images
        cv2.imwrite(os.path.join(root.left_img,name+'_L.jpg'), image_l.get_data())
        cv2.imwrite(os.path.join(root.right_img,name+'_R.jpg'), image_r.get_data())

        self.update_video_stream()
    
class FileCounterApp:
    def __init__(self, root):
        
        self.root = root
        
        self.root.title("File Counter App")
        self.folder_path = storing_data() 
        
        self.taget_count_var = StringVar()
        self.bocl_count_var = StringVar()
        self.viga_count_var = StringVar()        
        
        self.create_widgets()

    def create_widgets(self):
        # Create three labels to display file counts
        taget = Label(self.root, text="Tagete:", font = ('calibre', 10))
        taget.grid(row=20, column=0, padx=1, pady=5)#, sticky="e")
        
        viga = Label(self.root, text="Viole:",font = ('calibre', 10))
        viga.grid(row=20, column=1, padx=1, pady=5)#, sticky="e")
        
        bocl = Label(self.root, text="Bocca di Leone:",font = ('calibre', 10))
        bocl.grid(row=20, column=2, padx=1, pady=5)#, sticky="e")

        # Create three entry widgets to display file counts
        bocl_en = Entry(self.root, textvariable=self.taget_count_var, state="readonly",font = ('calibre', 10))
        bocl_en.grid(row=21, column=0, padx=1, pady=5)#, sticky="w")
        
        taget_en = Entry(self.root, textvariable=self.viga_count_var, state="readonly",font = ('calibre', 10))
        taget_en.grid(row=21, column=1, padx=1, pady=5)#, sticky="w")
        
        bocl_en = Entry(self.root, textvariable=self.bocl_count_var, state="readonly",font = ('calibre', 10))
        bocl_en.grid(row=21, column=2, padx=1, pady=5)#, sticky="w")

        # Update file counts initially
        self.update_file_counts()

    def update_file_counts(self):    

        if 'dataset.csv' in os.listdir(self.folder_path.dataset):
            df = pd.read_csv(os.path.join(self.folder_path.dataset, 'dataset.csv'))#['variety']
            variety = df['variety']
            count_taget = variety[variety == 'taget'].count()
            count_bocl = variety[variety == 'bocl'].count()
            count_viga = variety[variety == 'viga'].count()
        else:
            count_taget = 0
            count_bocl = 0
            count_viga = 0

        # Update the text variables for the entry widgets       
        self.taget_count_var.set(f"{count_taget}")
        self.bocl_count_var.set(f"{count_bocl}")
        self.viga_count_var.set(f"{count_viga}")

        self.root.after(1000, self.update_file_counts)

def description(win):
    
    """
    Create a text description of the interface.

    Args:
        win (Tk): The main window

    Returns:
        None
    """
    sc_w = win.winfo_screenwidth()
    txt = Text(win, height=10, width=int(sc_w/32), font = ('calibre', 20))
    txt.grid(row=0, column=0, rowspan = 4, columnspan=3, padx = 1, pady = 5)

    txt.insert(END,"This is an interface to manage the images and the measures of the flowers.\n\n")
    txt.insert(END,"The program is divided in 5 parts:\n")
    txt.insert(END,"0) flower picking (of course). \n")
    txt.insert(END,"1) select the flower's variety, this will be done by a chelist.\n")
    txt.insert(END,"2) measure the flower, this will be done by the operator thanks to a caliber.\n")
    txt.insert(END,"3) image acquisition, this will be done by the ZED camera.\n")
    txt.insert(END,"4) image and information saving, this will be done by the program.\n")

    txt.configure(state='disabled')

def sample_measure(win):
    
        """
        Create a sample image of the measure to take.
    
        Args:
            win (Tk): The main window
    
        Returns:
            None
        """
    
        img = PhotoImage( file="info_measurments.png")
        image_label = Label(win, image=img)
        image_label.image = img
        image_label.grid(row=1, column=3, rowspan = 4, columnspan=3, padx = 100, pady = 20)
    
def checklist_var(win):

    """
    Create a checklist to select the flower variety

    Args:
        win (Tk): The main window
    """

    flowers = {
    #'ager' : 'agerato',
    'bocl' : 'bocche_leone',
    #'bego' : 'begonie',
    #'marg' : 'margherite',
    #'cale' : 'calendule',
    #'borr' : 'borraggine',
    #'fior' : 'fiordaliso',
    #'dagr' : 'dalie_grandi',
    #'dapi' : 'dalie_picole',
    #'garo' : 'garofani',
    #'fucs' : 'fucsie',
    #'impa' : 'impatients',
    #'gera' : 'geranei',
    #'prim' : 'primule',
    #'rose' : 'rose',
    'taget' : 'tagete',
    #'vipo' : 'violette_piccole',
    'viga' : 'violette_grandi'
    }
    
    checkboxes = []
    selected_options = []  # List to store selected options

    def update_selected(option_key, var):
        if var.get() == 1:
            selected_options.append(option_key)
        else:
            selected_options.remove(option_key)
    
    for idx, key in enumerate(flowers.keys()):
        var = IntVar()
        var_button = Checkbutton(win, text= flowers[key], bd=4, variable=var, font=('calibre',20), command = lambda key=key, var=var: update_selected(key, var))
        var_button.grid(row=idx+6, column=0, columnspan=3, padx = 1, pady = 1)
        checkboxes.append(var)
    
    return checkboxes, selected_options

def measure_var(win, calix_var, all_var, diameter_var):

    """
    Create the entry to insert the measure of the calix, the overall height and the diameter.

    Args:
        win (Tk): The main window
        calix_var (DoubleVar): The variable to store the calix measure
        all_var (DoubleVar): The variable to store the overall height measure
        diameter_var (DoubleVar): The variable to store the diameter measure

    Returns:
        None
    """
    # Create the entry to insert the measure of the calix
    calix_label = Label(win, text = 'Calix measure', font=('calibre',20, 'bold'))
    calix_label.grid(row=11,column=0, padx = 10, pady = 10)
    measure_calix = Entry(win, textvariable = calix_var, width=30, font=('calibre',20))
    measure_calix.grid(row=11,column=1, padx = 10, pady = 10)
    # Create the entry to insert the measure of the overall height
    all_label = Label(win, text = 'Overall height', font=('calibre',20, 'bold'))
    all_label.grid(row=12,column=0, padx = 10, pady = 10)
    measure_all = Entry(win, textvariable = all_var, width=30, font=('calibre',20))
    measure_all.grid(row=12,column=1, padx = 10, pady = 10)
    # Create the entry to insert the measure of the diameter
    diameter_label = Label(win, text = 'Diameter measure', font=('calibre',20, 'bold'))
    diameter_label.grid(row=13,column=0, padx = 10, pady = 10)
    measure_diameter = Entry(win, textvariable = diameter_var, width=30, font=('calibre',20))
    measure_diameter.grid(row=13,column=1, padx = 10, pady = 10)


def confirm_window(input, app):

    """
    Create a pop-up window to display confirmation messages before saving the data.

    Args: 
        input (list): The list containing all the input data:
            input[0] (DoubleVar): The variable to store the calix measure
            input[1] (DoubleVar): The variable to store the overall height measure
            input[2] (DoubleVar): The variable to store the diameter measure
            input[3] (list): The list containing the selected flower variety
            input[4] (list): The list containing the variables of the flower variety checkboxes
    Returns:
        None
    """

    confirm = Tk()
    confirm.title("Confirm submit!!")

    screen_width = confirm.winfo_screenwidth()
    screen_height = confirm.winfo_screenheight()

    confirm.geometry(f"{int(screen_width/2)}x{int(screen_height/2)}")

    def Close():
        # Close the confirm window
        confirm.destroy()

    # Create the grid layout
    confirm.grid_rowconfigure(0, weight=1)
    confirm.grid_rowconfigure(1, weight=1)
    confirm.grid_columnconfigure(0, weight=1)
    confirm.grid_columnconfigure(1, weight=1)

    # Create text to be displayed
    worning_label = Label(confirm, text = "Are you sure you want to submit?", font=('calibre',30, 'bold'))
    worning_label.grid(row = 0 , column = 0, columnspan = 2, sticky='nsew')
    # Create the button to confirm choiche the measures
    Y_btn = Button(confirm, text = 'YES', font=('calibre',20, 'bold'), command = lambda input=input: save_data(input, confirm, app))
    Y_btn.grid(row=1,column=0, columnspan=1, padx = 5, pady = 5, sticky='nsew')
    # Create button to go back
    N_btn = Button(confirm, text = 'NO', font=('calibre',20, 'bold'), command = Close)
    N_btn.grid(row=1,column=1, columnspan=1, padx = 5, pady = 5, sticky='nsew')

    confirm.mainloop()


def worning_window(warning_text):

    """
    Create a pop-up window to display warning messages.

    Args: 
        warning_text (str): The text to display in the window

    Returns:
        None
    """

    worning = Tk()
    worning.title("Worning!!")

    screen_width = worning.winfo_screenwidth()
    screen_height = worning.winfo_screenheight()

    worning.geometry(f"{int(screen_width/2)}x{int(screen_height/2)}")

    worning.grid_rowconfigure(0, weight=1)
    worning.grid_rowconfigure(1, weight=1)
    worning.grid_columnconfigure(0, weight=1)
    worning.grid_columnconfigure(1, weight=1)

    def Close():
        # Close the worning window
        worning.destroy()

    # Create worning label to prevent from submitting empty or incorrect data
    worning_label = Label(worning, text = warning_text, font=('calibre',30, 'bold'))
    worning_label.grid(row = 0 , column = 0, columnspan = 2, sticky='nsew')
    # Create button to close the worning window
    ok_btn = Button(worning, text = 'CLOSE', font=('calibre',20, 'bold'), command = Close)
    ok_btn.grid(row=1,column=0, columnspan=2, padx = 5, pady = 5, sticky='nsew')

    worning.mainloop()

def submit(variety, calix_var, all_var, diameter_var, checkboxes, app):

    """
    This function will check if all the data are correct and will call the confirm_window function.

    Args:
        variety (list): The list containing the selected flower variety
        calix_var (DoubleVar): The variable to store the calix measure
        all_var (DoubleVar): The variable to store the overall height measure
        diameter_var (DoubleVar): The variable to store the diameter measure
        checkboxes (list): The list containing the variables of the flower variety checkboxes

    Returns:
        None
    """

    calix = calix_var.get()
    overall = all_var.get()
    diameter = diameter_var.get()

    # Check if all the measurment data have been inserted
    if calix == 0.0 or overall == 0.0 or diameter == 0.0: # or calix == "" or overall == "" or diameter == "": 
        worning_window("Please fill ALL measurment fields")
        return
    
    # Check if the flower variety has been selected
    if variety == []:
        worning_window("Please select a flower variety")
        return
    
    print('Checking variety ', variety)
    # Check if only one flower variety has been selected
    if len(variety) > 1:
        worning_window("Please select ONLY ONE flower variety")
        return
    
    #confirm_window(calix, overall, diameter, variety)
    input = [calix_var, all_var, diameter_var, variety, checkboxes]
    confirm_window(input, app) 

def save_data(input, confirm, app):

    """
    This function will save the image, a csv containing data collection inforation and a csv containing measurment information.
    """
    confirm.destroy()

    root = storing_data()
       
    if 'dataset.csv' not in os.listdir(root.dataset):
        with open(os.path.join(root.dataset, 'dataset.csv'), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["filename","timestamp", "left_image", "right_image", "calix_height", "oveall_height", "diameter", "variety", "index"])
        f.close()
    
    with open(os.path.join(root.dataset, 'dataset.csv'), 'r', encoding='UTF8') as f:
        final_line = f.readlines()[-1]
        previous = final_line.split(',')[-1]
        f.close()
        print('previous: ', previous)
        if previous == 'index\n':
            i = 0
        else:
            i = int(previous) + 1
    
    name = input[3][0] + '_' + str(i)
    
    ct = datetime.datetime.now()
    timestamp = ct.timestamp()
    app.submit_action(root, name)
    # Save the data

    print("Saving data...")
    print('name: ', name)  
    print('calix: ', input[0].get())
    print('overall: ', input[1].get())
    print('diameter: ', input[2].get())
    print('variety: ', input[3])

    with open(os.path.join(root.dataset, 'dataset.csv'), 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([name,
                        timestamp,
                        str(os.path.join(root.left_img,name+'_L.jpg')),
                        str(os.path.join(root.right_img,name+'_R.jpg')),
                        input[0].get(),   
                        input[1].get(),
                        input[2].get(),
                        input[3][0],
                        i])
        f.close()
    
    print('Data saved!')
    # Setting all the value back to the original one
    for var in input[4]:
        var.set(0)
    input[0].set(0.0)
    input[1].set(0.0)
    input[2].set(0.0)
    input[3].clear()

def main():
    
    # Create an instance of the canvas
    win = Tk()
    win.title("Flower Image and Measurement Manager")

    # Define the geometry of the window
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    win.geometry(f"{screen_width}x{screen_height}")

    win['padx'] = 20
    win['pady'] = 20
    
    # Create the variables of the measures
    calix_var = DoubleVar()
    all_var = DoubleVar()
    diameter_var = DoubleVar()
        
    # Create a initial text description
    description(win)

    # Create a label to display the instructions
    inst_name = Label(win, text="Choose the flower variety", font=('calibre',20, 'bold'))
    inst_name.grid(row=5, column=0, columnspan=3, padx = 1, pady = 1)

    # Create a ckelist to select the flower variety
    checkboxes, result =  checklist_var(win)
    
    # Create a label to display the measure instructions
    inst_measure = Label(win, text="Insert the collected measurments", font=('calibre',20, 'bold'))
    inst_measure.grid(row=9, column=0, columnspan=3, padx = 1, pady = 1)

    # Create the variables of the measures
    measure_var(win, calix_var, all_var, diameter_var)
    
    app = ZedVideoApp(win)
    FileCounterApp(win)  

    # Create the button to submit everything
    sub_btn = Button(win, text = 'Submit', command = lambda variety=result: submit(variety, calix_var, all_var, diameter_var, checkboxes, app), font=('calibre',20, 'bold'))
    sub_btn.grid(row=15,column=0, columnspan=3, padx = 1, pady = 20)
    
    # Create a label and image to display the measure instructions
    samp_measure = Label(win, text="Sample of measurment to take", font=('calibre',20, 'bold'))
    samp_measure.grid(row=0, column=3, columnspan=3, padx = 1, pady = 1)

    # Insert the sample image of the measure to take
    sample_measure(win)
    
    # Create the label and canvas to display the image from the ZED camera
    zed_image = Label(win, text="ZED camera LEFT image", font=('calibre',20, 'bold'))
    zed_image.grid(row=5, column=3, columnspan=3, padx = 1, pady = 10)

    win.mainloop()

if __name__ == '__main__':
    main()