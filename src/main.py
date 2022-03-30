# main.py
#
# This module handes GUI interface for the program and runs it
# 
# See https://github.com/Drew-1771/Python-Video-Download for information
# about this project.

import tkinter
import tkinter.ttk
import pathlib
import download
import fileUtilities

color = "grey30"
light_color = "grey40"
foreground = "white"


def color_tabs(list_to_color: list, light_color: str, foreground: str):
        for item in list_to_color:
            item.config(bg=light_color, fg=foreground)


def createSettings(window: tkinter.Tk, tab: tkinter.ttk.Frame) -> list:
    # returns this list to color the tabs later
    return_list = []

    # auto clear url button
    def clear_url_clicked():
        data = fileUtilities.JsonFile("data.json").read()
        data["auto_clear_url"] = button_flag.get()
        fileUtilities.JsonFile("data.json").write(data)
    button_flag = tkinter.BooleanVar()
    button_flag.set(fileUtilities.JsonFile("data.json").read()["auto_clear_url"])
    auto_clear_widget = tkinter.Checkbutton(tab, text="Auto clear url after input", command=clear_url_clicked, variable=button_flag, selectcolor=color)
    auto_clear_widget.grid(column=0, row=0, sticky="w")
    return_list.append(auto_clear_widget)

    path = fileUtilities.JsonFile("data.json").read()["download_folder_path"]
    # current download path labels
    current_path_label_widget = tkinter.Label(tab, text="Output path:")
    current_path_widget = tkinter.Label(tab, text=path)
    current_path_label_widget.grid(column=0, row=1, sticky="w")
    current_path_widget.grid(column=0, row=2, sticky="w")
    return_list.append(current_path_label_widget)
    return_list.append(current_path_widget)

    return return_list


def createDownload(window: tkinter.Tk, tab: tkinter.ttk.Frame) -> list:
    # returns this list to color the tabs later
    return_list = []

    # github url label
    github_label_widget = tkinter.Label(tab, text="https://github.com/Drew-1771/Python-Video-Download")
    github_label_widget.pack(side=tkinter.TOP, anchor=tkinter.NW)
    github_label_widget.config(bg=color, fg=foreground)

    # Status label
    status_label_widget = tkinter.Label(tab, text="Waiting...")
    status_label_widget.place(relx=0.5, rely=0.30, relwidth=0.5, relheight=0.15, anchor=tkinter.CENTER)
    return_list.append(status_label_widget)

    # url entry
    url_entry_widget = tkinter.Entry(tab, width=15)
    url_entry_widget.place(relx=0.5, rely=0.45, relwidth=0.85, relheight=0.15, anchor=tkinter.CENTER)
    return_list.append(url_entry_widget)

    # name label
    name_label_widget = tkinter.Label(tab, text="Name (optional):")
    name_label_widget.place(relx=0.125, rely=0.92, relwidth=0.25, relheight=0.15, anchor=tkinter.CENTER)
    return_list.append(name_label_widget)

    # name entry
    name_entry_widget = tkinter.Entry(tab, width=15)
    name_entry_widget.place(relx=0.455, rely=0.92, relwidth=0.4, relheight=0.15, anchor=tkinter.CENTER)
    return_list.append(name_entry_widget)

    # download button
    def download_clicked(event=False):
        data = fileUtilities.JsonFile("data.json")
        path = data.read()["download_folder_path"]
        auto_clear_url = data.read()["auto_clear_url"]
        try:
            temp_txt = url_entry_widget.get()
            if (auto_clear_url):
                url_entry_widget.delete(0, "end")
            if (name_entry_widget.get() == ""):
                name = str(download.generateRandomNumber(0, 999999999))
            else:
                name = name_entry_widget.get()
            name = download.video_download(temp_txt, path, name, ".mp4")
            status_label_widget.config(text=name, bg= "green")
            name_entry_widget.delete(0, "end")
        except download.VideoConnectionError:
            status_label_widget.config(text="Could not connect", bg= "red2")
    download_button_widget = tkinter.Button(tab, text="Download Video", width=15, command=download_clicked)
    download_button_widget.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.15, anchor=tkinter.CENTER)
    # keybind for download
    window.bind("<Return>", download_clicked)
    return_list.append(download_button_widget)

    return return_list


def run():
    # get info
    data_path = pathlib.Path(__file__).parent / "data.json"
    if (data_path.exists()):
        data = fileUtilities.JsonFile("data.json").read()
        data["download_folder_path"] = str(pathlib.Path(__file__).parent.parent / "vid").replace('\\', "/")
        fileUtilities.JsonFile("data.json").write(data)
    else:
        # create the data file
        fileUtilities.JsonFile("data.json").write({"download_folder_path": str(pathlib.Path(__file__).parent.parent / "vid").replace('\\', "/"), "auto_clear_url": True})

    # Set up window
    window = tkinter.Tk()
    window.title("Video Download v1.3")
    window.geometry("400x300")
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

    # populate and color tabs
    tabs_to_be_colored = createDownload(window, download_tab)
    tabs_to_be_colored = tabs_to_be_colored + createSettings(window, settings_tab)
    color_tabs(tabs_to_be_colored, light_color, foreground)

    # run
    window.mainloop()


if __name__ == "__main__":
    run()