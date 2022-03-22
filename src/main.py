# main.py
#
# This module handes GUI interface for the program and runs it

from tabnanny import check
import tkinter
import tkinter.ttk
import pathlib
from turtle import bgcolor
import download
import fileUtilities

color = "grey30"
light_color = "grey40"


def createSettings(window: tkinter.Tk, tab: tkinter.ttk.Frame) -> None:
    path = fileUtilities.JsonFile("data.json").read()["download_folder_path"]

    # current download path labels
    header = tkinter.Label(tab, text="Output path:")
    header.config(bg=color, fg="white")
    header.grid(column=0, row=1, sticky="w")
    current_path = tkinter.Label(tab, text=path)
    current_path.config(bg=light_color, fg="white")
    current_path.grid(column=0, row=2, sticky="w")

    # auto clear url button
    def clear_url_clicked():
        data = fileUtilities.JsonFile("data.json").read()
        data["auto_clear_url"] = button_flag.get()
        fileUtilities.JsonFile("data.json").write(data)
    button_flag = tkinter.BooleanVar()
    button_flag.set(fileUtilities.JsonFile("data.json").read()["auto_clear_url"])
    checkbutton = tkinter.Checkbutton(tab, text="Auto clear url after input", command=clear_url_clicked, variable=button_flag, bg=light_color, fg="white", selectcolor=color)
    checkbutton.grid(column=0, row=0, sticky="w")


def createDownload(window: tkinter.Tk, tab: tkinter.ttk.Frame) -> None:
    # Box for url entry
    url_txt = tkinter.Entry(tab, width=15)
    url_txt.config(bg=light_color, fg="white")
    url_txt.place(relx=0.5, rely=0.5, relwidth=0.85, relheight=0.15, anchor=tkinter.CENTER)
    
    # Status label
    status = tkinter.Label(tab, text="Waiting...")
    status.config(bg=light_color, fg="white")
    status.place(relx=0.5, rely=0.35, relwidth=0.5, relheight=0.15, anchor=tkinter.CENTER)

    # Download button
    def download_clicked(event=False):
        data = fileUtilities.JsonFile("data.json")
        path = data.read()["download_folder_path"]
        auto_clear_url = data.read()["auto_clear_url"]
        try:
            temp_txt = url_txt.get()
            if (auto_clear_url):
                url_txt.delete(0, "end")
            name = download.video_download(temp_txt, path, ".webm")
            status.config(text=name, bg= "green")
        except download.VideoConnectionError:
            status.config(text="Could not connect", bg= "red2")
    
    download_button = tkinter.Button(tab, text="Download Video", width=15, command=download_clicked)
    download_button.config(bg=light_color, fg="white")
    download_button.place(relx=0.5, rely=0.65, relwidth=0.5, relheight=0.15, anchor=tkinter.CENTER)
    
    # keybind
    window.bind("<Return>", download_clicked)


def run():
    # get info
    outer = pathlib.Path(__file__).parent / "data.json"
    if not (outer.exists()):
        fileUtilities.JsonFile("data.json").write({"download_folder_path": str(pathlib.Path(__file__).parent.parent / "vid").replace('\\', "/"), "auto_clear_url": True})
    else:
        data = fileUtilities.JsonFile("data.json").read()
        data["download_folder_path"] = str(pathlib.Path(__file__).parent.parent / "vid").replace('\\', "/")
        fileUtilities.JsonFile("data.json").write(data)
    # Set up window
    window = tkinter.Tk()
    window.title("Video Download")
    window.geometry("300x200")
    window.config(bg=color)

    # set up tabs
    tabs = tkinter.ttk.Notebook(window)
    # tab colors
    tkinter.ttk.Style().configure("TNotebook", background=color, foreground=light_color)

    download_tab = tkinter.Frame(tabs, bg=color)
    settings_tab = tkinter.Frame(tabs, bg=color)
    tabs.add(download_tab, text="Download")
    tabs.add(settings_tab, text="Settings")
    tabs.pack(expand = 1, fill ="both")

    # populate tabs
    createDownload(window, download_tab)
    createSettings(window, settings_tab)

    # run
    window.mainloop()


if __name__ == "__main__":
    run()