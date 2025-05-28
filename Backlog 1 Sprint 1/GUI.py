import tkinter as tk
import vlc
import os

root = tk.Tk()
root.title("Raspberry pi Media Player")
root.geometry("600x400")

instance = vlc.Instance()
player = instance.media_player_new()

def play_video():
    print("Play button pressed")
    filename = '/home/pi/EGL-314/video.mp4'
    if os.path.exists(filename):
        media = instance.media_new(filename)
        player.set_media(media)
        player.play()
    else:
        print(f"Erro: {filename} does not exist.")

main = tk()
main.title("try")


def pause_video():
    player.pause

def stop_video():
    player.stop



play_button = tk.Button(root, text="Play", command=play_video, width=10)
play_button.pack(pady=10)

pause_button = tk.Button(root, text="Pause", command=pause_video, width=10)
pause_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_video, width=10)
stop_button.pack(pady=10)

root.mainloop
