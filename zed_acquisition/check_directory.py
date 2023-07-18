import os
import time
import tkinter as tk

class storing_data():
    def __init__(self, base_root):
        #self.base_root = '/media/jetson/Volume/Data'
        
        self.left_img = os.path.join(base_root, 'left_image')
        self.right_img = os.path.join(base_root, 'right_image')
        self.depth_img = os.path.join(base_root, 'depth')
        self.point_cloud = os.path.join(base_root, 'point_cloud')
        self.recap_root = os.path.join(base_root, 'recap')

    def __len__(self, path):        
        return len(os.listdir(path))
    
    def __split__(self, path):
        return path.split('/')[-1]

def main():
    base_root = '/media/jetson/Volume/Data'
    root = storing_data(base_root)

    print( "{}  --> {} files".format(root.__split__(root.left_img), root.__len__(root.left_img)), end="\r")
    print( "{}  --> {} files".format(root.__split__(root.right_img), root.__len__(root.right_img)), end="\r")
    
    print( "{}  --> {} files".format(root.__split__(root.depth_img), root.__len__(root.depth_img)), end="\r")
    print( "{}  --> {} files".format(root.__split__(root.point_cloud), root.__len__(root.point_cloud)), end="\r")

    print( "{}  --> {} files".format(root.__split__(root.recap_root), root.__len__(root.recap_root)), end="\r")
    

    time.sleep(5)

if __name__ == "__main__":
    main()
