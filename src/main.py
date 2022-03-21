# main.py
#
# This module handes GUI interface for the program and runs it

import tkinter
import tkinter.ttk
import pathlib
import download
import fileUtilities

color = "grey30"
light_color = "grey40"
auto_clear_url = True # global for now until i add it in settings


def createDownload(window: tkinter.Tk, tab: tkinter.ttk.Frame, path: str) -> None:
    '''
    Creates the download tab with all its buttons
    '''
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
        fileUtilities.JsonFile("data.json").write({"download_folder_path": str(pathlib.Path(__file__).parent.parent / "vid").replace('\\', "/")})
    data = fileUtilities.JsonFile("data.json").read()
    path = data["download_folder_path"]
    print(path)

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
    createDownload(window, download_tab, path)
    #createSettings(window, settings_tab)

    # run
    window.mainloop()


if __name__ == "__main__":
    run()