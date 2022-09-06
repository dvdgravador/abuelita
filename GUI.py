# import external libraries
import vlc

import tkinter as Tk
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

        self.width_screen = self.parent.winfo_screenwidth()
        self.height_screen = self.parent.winfo_screenheight()

        self.load_images()

        self.videopanel = Tk.Frame(self.parent)
        self.videocanvas = Tk.Canvas(self.videopanel)

        self.imagepanel = Tk.Frame(self.parent)
        self.imagecanvas = Tk.Canvas(self.imagepanel)

        self.background_image = self.imagecanvas.create_image(0, 0, image=None,
                                                              anchor="nw")

        self.update_image()

        self.imagepanel.pack(fill=Tk.BOTH, expand=1)
        self.imagecanvas.pack(fill=Tk.BOTH, expand=1)
        self.videocanvas.pack(fill=Tk.BOTH, expand=1)

        self.parent.bind('<Escape>', self.OnExit)
        self.parent.bind('<Right>', self.OnMove)
        self.parent.bind('<Left>', self.OnMove)
        self.parent.bind('<Return>', self.OnOpen)

        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.events = self.player.event_manager()
        self.events.event_attach(
            vlc.EventType.MediaPlayerEndReached, self.OnVideoFinished)
        self.player.set_hwnd(self.videocanvas.winfo_id())

        self.parent.update()

    def load_images(self):
        for index in range(0, self.items):
            filename = index + 1
            img = Image.open("pictures/" + str(filename) + ".png")
            img = img.resize((self.width_screen, self.height_screen))
            self.images[index] = ImageTk.PhotoImage(img)

    def update_image(self):
        self.bg = self.images.get(self.position)
        self.imagecanvas.itemconfig(self.background_image, image=self.bg)

    def OnExit(self, evt):
        """Closes the window.
        """
        self.parent.quit()
        self.parent.destroy()
        os._exit(1)

    def OnOpen(self, evt):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        if self.player.is_playing():
            self.player.stop()
            self.videopanel.pack_forget()
            self.imagepanel.pack(fill=Tk.BOTH, expand=1)
        else:
            self.imagepanel.pack_forget()
            self.videopanel.pack(fill=Tk.BOTH, expand=1)
            self.Media = self.Instance.media_new(
                "videos/" + str(self.position) + ".mp4")
            self.player.set_media(self.Media)
            self.player.play()

    def OnVideoFinished(self, evt):
        self.videopanel.pack_forget()
        self.imagepanel.pack(fill=Tk.BOTH, expand=1)

    def OnMove(self, evt):
        if evt.keysym == "Right":
            self.position += 1
        else:
            self.position -= 1
        self.position %= self.items
        self.update_image()


def Tk_get_root():
    if not hasattr(Tk_get_root, "root"):
        Tk_get_root.root = Tk.Tk()
        Tk_get_root.root.attributes('-fullscreen', 1)
        Tk_get_root.root.config(cursor="none")
    return Tk_get_root.root


if __name__ == "__main__":
    root = Tk_get_root()
    player = Player(root)
    root.mainloop()
