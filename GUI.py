# import external libraries
from time import sleep
import vlc
import sys

import tkinter as Tk
from tkinter import PhotoImage, ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

# import standard libraries
import os

class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.position = 0
        self.items = len(os.listdir("pictures"))
        self.images = {}
        self.is_playing = False

        self.width_screen = self.parent.winfo_screenwidth()
        self.height_screen = self.parent.winfo_screenheight()

        self.load_images()
    
        self.videopanel = Tk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel)

        self.background_image = self.canvas.create_image(0, 0, image = None, 
                     anchor = "nw")

        self.update_image()

        self.videopanel.pack(fill=Tk.BOTH,expand=1)
        self.canvas.pack(fill=Tk.BOTH,expand=1)
        
        self.parent.bind('<Escape>', self.OnExit) # permite que se salga del programa pulsando escape
        self.parent.bind('<Right>', self.OnMove) 
        self.parent.bind('<Left>', self.OnMove)
        self.parent.bind('<Return>', self.OnOpen)  
        self.parent.bind('<<MediaFinish>>', self.OnOpen)  
        
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.mediaFinish)

        self.parent.update()
    
    def load_images(self):
        for index in range(0, self.items):
            filename = index + 1
            img = Image.open("pictures/" + str(filename) + ".png") 
            img = img.resize((self.width_screen, self.height_screen))
            self.images[index] = ImageTk.PhotoImage(img)
    
    def update_image(self):
        self.bg = self.images.get(self.position)
        self.canvas.itemconfig(self.background_image, image = self.bg)

    def OnExit(self, evt):
        """Closes the window.
        """
        self.parent.quit()
        self.parent.destroy()
        os._exit(1)

    def OnOpen(self, evt):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        sleep(2)
        self.player.set_hwnd(0)
        if self.is_playing:
            if self.player.is_playing():
                self.player.stop()
            else:
                print("VAMOS A REPRODUCRILO")
                self.Media = self.Instance.media_new("videos/" + str(self.position) + ".mp4")
                print("VAMOS A 1")
                self.player.set_media(self.Media)
                print("VAMOS A 2")
                self.player.play()
                print("VAMOS A 3")
                self.player.stop()
                print("VAMOS A 4")
            self.is_playing = False
        else:
            self.Media = self.Instance.media_new("videos/" + str(self.position) + ".mp4")
            self.player.set_media(self.Media)
            self.player.set_hwnd(self.GetHandle())
            self.player.play()
            self.is_playing = True
    
    def mediaFinish(self, evnt):
        self.parent.event_generate("<<MediaFinish>>")
    
    def OnMove(self, evt):
        if evt.keysym == "Right":
            self.position += 1
        else:
            self.position -= 1
        self.position %= self.items
        self.update_image()
            
    def GetHandle(self):
        return self.videopanel.winfo_id()

    def OnStop(self):
        """Stop the player.
        """
        self.player.stop()
        # reset the time slider
        self.timeslider.set(0)

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        tk.tkMessageBox.showerror(self, 'Error', errormessage)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"): #(1)
        Tk_get_root.root= Tk.Tk()  #initialization call is inside the function
        Tk_get_root.root.attributes('-fullscreen', 1) #fullscreen
        Tk_get_root.root.config(cursor="none")  # escondo cursor
    return Tk_get_root.root


if __name__ == "__main__":
    # Create a Tk.App(), which handles the windowing system event loop
    root = Tk_get_root()
    player = Player(root)
    # show the player window centred and run the application
    root.mainloop()
