import tkinter as tk
import os
import vlc
import time
from PIL import ImageTk, Image



directorio = 'pictures'
contenido = os.listdir(directorio)
images = []

for fichero in contenido:                
    if os.path.isfile(os.path.join(directorio, fichero)) and fichero.endswith('.jpg'):   # solo si es archivo y con extension jpg lo añade
        images.append(fichero)

t = len(images)   
n = 0
#print(t)
#print(images)



root = tk.Tk()
root.attributes('-fullscreen', 1) #fullscreen
root.config(cursor="none")  # escondo cursor

# obtiene el tamaño actual de la pantalla:
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()


# reescalo las imagenes para llenar pantalla completa
photos = []
for x in images:
    img = Image.open("pictures/" + str(x)) 
    img = img.resize((int(scr_width), int(scr_height)))  # redimensiona la foto al tamaño de la pantalla 
    photos.append(ImageTk.PhotoImage(img))     # en cada iteracion se añade una imagen ya redimensionada a la lista "photos"
    #print("escalando imagen"+ str(x))  

   
displayCanvas = tk.Label(root)
displayCanvas.pack(expand=1, fill=tk.BOTH)
displayCanvas.config(image=photos[n])  # primera imagen en pantalla 

def right(event):
    global n
    global t

    if n < t:
        n += 1
    if n == t:
        n = 0
    print(n)
    displayCanvas.config(image=photos[n])   #se actualiza la imagen

    
def left(event):
    global n
    global t
    n = abs(n)                                 # siempre positivo, nunca negativo ;)
    if n <= t and n != 0:
        n -= 1
    else:
        n = t
                               
    displayCanvas.config(image=photos[n])
    


def reproducir(event):
    
    media_player = vlc.MediaPlayer()
    media_player.set_fullscreen(True)
    media = vlc.Media(str(n+1)+".mp4")
    media_player.set_media(media)
    media_player.play()
    time.sleep(1.5)
    duration = media_player.get_length() / 1000
    #print(duration)
    time.sleep(duration+1.5)
    media_player.stop()




root.bind('<Escape>', lambda e: root.destroy()) # permite que se salga del programa pulsando escape
root.bind('<Right>', right) 
root.bind('<Left>', left)
root.bind('<Return>', reproducir)  
    
root.focus_force() # mantiene en primer plano la pantalla
root.mainloop()
