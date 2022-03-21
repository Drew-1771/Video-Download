# inteface.py
#
# This module handes GUI interface for the program

import tkinter
import tkinter.ttk
from turtle import down
import download

def run():
    # Set up window
    window = tkinter.Tk()
    window.title("Video Download")
    window.geometry("300x200")
    window.config(bg="gray10")

    # Select which website
    choice = tkinter.ttk.Combobox(window)
    choice.place(relx=0.17, rely=0.5, relwidth=0.275, relheight=0.15, anchor=tkinter.CENTER)
    choice['values'] = ("Youtube", "Twitter")
    choice.current(0) # default at youtube

    # Box for url entry
    url_txt = tkinter.Entry(window, width=15)
    url_txt.place(relx=0.55, rely=0.5, relwidth=0.5, relheight=0.15, anchor=tkinter.CENTER)

    # Download button
    def download_clicked():
        try:
            if(choice.get() == "Youtube"):
                name = download.youtube_download(url_txt.get(), "src/vid")
            else:
                name = download.twitter_download(url_txt.get(), "src/vid")
            status.config(text=name, bg= "green")
        except download.VideoConnectionError:
            status.config(text="Could not connect", bg= "red2")
    
    download_button = tkinter.Button(window, text="Download Video", width=15, command=download_clicked)
    download_button.place(relx=0.55, rely=0.625, relwidth=0.5, relheight=0.15, anchor=tkinter.CENTER)
    
    # Status label
    status = tkinter.Label(window, text="Waiting...")
    status.config(bg = "gray51", fg="white")
    status.place(relx=0.55, rely=0.375, relwidth=0.5, relheight=0.1, anchor=tkinter.CENTER)

    # run
    window.mainloop()


if __name__ == "__main__":
    run()