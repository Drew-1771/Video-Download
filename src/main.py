# main.py
#
# This module handes GUI interface for the program and runs it
#
# See https://github.com/Drew-1771/Video-Download for information
# about this project.

import tkinter
import tkinter.ttk
from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
import pathlib
import download
import fileUtilities
import sys
import math

color = "grey30"
light_color = "grey40"
foreground = "white"

# List of tabs that currently exist
TABS = []


class StdoutRedirector(object):
    def __init__(self, window, progress_bar, text_widget):
        self.window = window
        self.progress_bar = progress_bar
        self.text_space = text_widget

    def write(self, string: str):
        if string.strip() == "\n":
            return
        if "[download]" in string and "Completed" in string:
            pass
        elif "[download]" in string and "Finished" in string:
            return
        elif "[download]" in string and "Destination:" not in string:
            substring = string.split(" ")
            for string in substring:
                if "%" in string:
                    self.progress_bar["value"] = math.floor(
                        float(string.replace("%", ""))
                    )
                    return
        self.text_space.insert("end", string)
        self.text_space.see("end")

    def flush(self):
        tkinter.Tk.update(self.window)


def color_tabs(light_color: str, foreground: str) -> None:
    for item in TABS:
        item.config(bg=light_color, fg=foreground)


def createSettings(tab: tkinter.ttk.Frame) -> None:
    # auto clear url button
    def clear_url_clicked():
        data = fileUtilities.JsonFile("data.json").read()
        data["auto_clear_url"] = button_flag.get()
        fileUtilities.JsonFile("data.json").write(data)

    button_flag = tkinter.BooleanVar()
    button_flag.set(fileUtilities.JsonFile("data.json").read()["auto_clear_url"])
    auto_clear_widget = tkinter.Checkbutton(
        tab,
        text="Auto clear url after input",
        command=clear_url_clicked,
        variable=button_flag,
        selectcolor=color,
    )
    auto_clear_widget.grid(column=0, row=0, sticky="w")
    TABS.append(auto_clear_widget)

    path = fileUtilities.JsonFile("data.json").read()["download_folder_path"]
    # current download path labels
    current_path_label_widget = tkinter.Label(tab, text="Default output path:")
    current_path_widget = tkinter.Label(tab, text=path)
    current_path_label_widget.grid(column=0, row=1, sticky="w")
    current_path_widget.grid(column=0, row=2, sticky="w")
    TABS.append(current_path_label_widget)
    TABS.append(current_path_widget)


def createImageConvert(tab: tkinter.ttk.Frame) -> None:
    def select_file():
        filename = filedialog.askopenfilename(
            title="Select image file (PNG, JPG, WEBP)",
            initialdir=f"{pathlib.Path(pathlib.Path.cwd() / 'vid')}",
        )
        if filename:
            try:
                # reset buttons
                file_entry_widget.config(text="Open File", bg=light_color)
                file_save_widget.config(text="Save File", bg=light_color)

                # load image
                img = ImageTk.PhotoImage(Image.open(filename))
                # get preview
                img_preview = ImageTk.PhotoImage(
                    Image.open(filename).resize(
                        (
                            img_widget_preview.winfo_width(),
                            img_widget_preview.winfo_height(),
                        )
                    )
                )
                # update image and preview
                img_widget.configure(image=img)
                img_widget_preview.configure(image=img_preview)
                img_widget.image = img
                img_widget_preview.image = img_preview

            except UnidentifiedImageError:
                file_entry_widget.config(text="Could not load", bg="red2")
                img_widget.configure(image=None)
                img_widget_preview.configure(image=None)
                img_widget.image = None
                img_widget_preview.image = None

    def convert_file():
        try:
            data = fileUtilities.JsonFile("data.json")
            path = data.read()["download_folder_path"]

            new_im = ImageTk.getimage(img_widget.image).convert("RGB")
            filename = filedialog.asksaveasfilename(
                title="Save image file as (PNG, JPG)",
                filetypes=[("jpg file", ".jpg"), ("png file", ".png")],
                defaultextension=".jpg",
                initialfile=str(download.generateRandomNumber(0, 999999999)) + ".jpg",
                initialdir=path,
            )
            if filename:
                new_im.save(filename)
                size = round(
                    pathlib.Path(filename).stat().st_size / 1024 / 1024,
                    2,
                )
                file_save_widget.config(text=f"{size}mb", bg="green")
        except AttributeError:
            file_save_widget.config(text="None loaded", bg="red2")

    # github url label
    github_label_widget = tkinter.Label(
        tab, text="https://github.com/Drew-1771/Video-Download"
    )
    github_label_widget.pack(side=tkinter.TOP, anchor=tkinter.NW)
    github_label_widget.config(bg=color, fg=foreground)

    # image label
    img_widget = tkinter.Label(tab)
    img_widget_preview = tkinter.Label(tab)
    img_widget_preview.place(
        relx=0.5,
        rely=0.5,
        relwidth=0.75,
        relheight=0.75,
        anchor=tkinter.CENTER,
    )
    img_widget_preview.config(bg="gray")

    # file entry
    file_entry_widget = tkinter.Button(
        tab, text="Open File", command=select_file, width=15, takefocus=False
    )
    file_entry_widget.place(
        relx=0.3, rely=0.9, relwidth=0.4, relheight=0.1, anchor=tkinter.CENTER
    )

    # file save
    file_save_widget = tkinter.Button(
        tab, text="Save File", command=convert_file, width=15, takefocus=False
    )
    file_save_widget.place(
        relx=0.7, rely=0.9, relwidth=0.4, relheight=0.1, anchor=tkinter.CENTER
    )

    TABS.append(file_entry_widget)
    TABS.append(file_save_widget)


def createDownload(window: tkinter.Tk, tab: tkinter.ttk.Frame) -> None:
    # github url label
    github_label_widget = tkinter.Label(
        tab,
        text="https://github.com/Drew-1771/Video-Download",
    )
    github_label_widget.pack(side=tkinter.TOP, anchor=tkinter.NW)
    github_label_widget.config(bg=color, fg=foreground)

    # url entry
    url_entry_widget = tkinter.Entry(tab, width=15)
    url_entry_widget.place(
        relx=0.5, rely=0.45, relwidth=0.85, relheight=0.15, anchor=tkinter.CENTER
    )
    TABS.append(url_entry_widget)

    # progress bar (jumping thru hoops simulator)
    style = tkinter.ttk.Style()
    style.theme_use("clam")
    style.configure("1.Horizontal.TProgressbar", troughcolor=color, background="green")
    progress_bar = tkinter.ttk.Progressbar(
        tab,
        style="1.Horizontal.TProgressbar",
        orient=tkinter.HORIZONTAL,
        length=160,
        mode="determinate",
    )
    progress_bar.place(
        relx=0.5, rely=0.9, relwidth=0.85, relheight=0.05, anchor=tkinter.CENTER
    )

    # console output
    std_box = tkinter.Text(
        tab,
        wrap="word",
        height=30,
        width=30,
        fg="snow",
        bg="gray20",
        font=("Arial", 9),
    )
    std_box.place(
        relx=0.5, rely=0.7, relwidth=0.85, relheight=0.35, anchor=tkinter.CENTER
    )
    sys.stdout = StdoutRedirector(tab, progress_bar, std_box)

    # download button
    def download_clicked(event=False) -> None:
        # reset button
        download_button_widget.config(text="Download Video", bg=light_color)
        # reset progress bar
        progress_bar["value"] = 0
        # reset text bot
        std_box.delete(1.0, tkinter.END)

        data = fileUtilities.JsonFile("data.json")
        path = data.read()["download_folder_path"]
        filename = filedialog.asksaveasfilename(
            title="Save video",
            filetypes=[("mp4 file", ".mp4")],
            defaultextension=".mp4",
            initialfile=str(download.generateRandomNumber(0, 999999999)),
            initialdir=path,
        )
        if filename:
            # update status
            download_button_widget.config(text="Trying...", bg=light_color)
            tkinter.Tk.update(window)

            auto_clear_url = data.read()["auto_clear_url"]
            try:
                temp_txt = url_entry_widget.get()
                if auto_clear_url:
                    url_entry_widget.delete(0, "end")

                filename = pathlib.Path(filename)
                # get file
                if filename.suffixes:
                    first = filename.suffixes[0]
                    filename = filename.parent / filename.name.split(first)[0]
                file = download.video_download(temp_txt, str(filename))
                # display size
                size = round(
                    pathlib.Path(file).stat().st_size / 1024 / 1024,
                    2,
                )
                download_button_widget.config(
                    text=filename.stem + f" @ {size}mb", bg="green"
                )
                # touch to update
                pathlib.Path(file).touch(exist_ok=True)
                # print finish confirm
                print(f"[download] Completed @ {size}mb")
            except download.VideoConnectionError:
                download_button_widget.config(text="Could not connect", bg="red2")
                # reset progress bar
                progress_bar["value"] = 0

    download_button_widget = tkinter.Button(
        tab, text="Download Video", width=15, command=download_clicked
    )
    download_button_widget.place(
        relx=0.5, rely=0.30, relwidth=0.5, relheight=0.15, anchor=tkinter.CENTER
    )
    TABS.append(download_button_widget)

    def paste_url(event=False) -> None:
        # create hidden window
        root = tkinter.Tk()
        root.withdraw()
        url_entry_widget.delete(0, tkinter.END)
        url_entry_widget.insert(0, root.clipboard_get())

    # keybinds for download
    # pressing enter will download whatever is in the url slot
    window.bind("<Return>", download_clicked)
    # pressing right click will paste whatever is in the clipboard to the url slot
    window.bind("<Button-3>", paste_url)


def run() -> None:
    # get info
    data_path = pathlib.Path(__file__).parent / "data.json"
    if data_path.exists():
        data = fileUtilities.JsonFile("data.json").read()
        data["download_folder_path"] = str(
            pathlib.Path(__file__).parent.parent / "vid"
        ).replace("\\", "/")
        fileUtilities.JsonFile("data.json").write(data)
    else:
        # create the data file
        fileUtilities.JsonFile("data.json").write(
            {
                "download_folder_path": str(
                    pathlib.Path(__file__).parent.parent / "vid"
                ).replace("\\", "/"),
                "auto_clear_url": True,
            }
        )

    # Set up window
    window = tkinter.Tk()
    window.title("Video Download v1.5")
    window.geometry("400x300")
    window.config(bg=color)

    # set up tabs
    tabs = tkinter.ttk.Notebook(window)
    # tab colors
    tkinter.ttk.Style().configure("TNotebook", background=color, foreground=light_color)

    download_tab = tkinter.Frame(tabs, bg=color)
    convert_image_tab = tkinter.Frame(tabs, bg=color)
    settings_tab = tkinter.Frame(tabs, bg=color)
    tabs.add(download_tab, text="Download")
    tabs.add(convert_image_tab, text="Convert Images")
    tabs.add(settings_tab, text="Settings")
    tabs.pack(expand=1, fill="both")

    # populate and color tabs
    createDownload(window, download_tab)
    createImageConvert(convert_image_tab)
    createSettings(settings_tab)
    color_tabs(light_color, foreground)

    # run
    window.mainloop()


if __name__ == "__main__":
    run()
