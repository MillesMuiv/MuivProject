import customtkinter
from Search import *
from YTData import *
from OAUTHRequests import *
from OAuth import *
import time
from YD import Downloader
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

LOGGED_IN = 0


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("AppTitle")
        self.geometry(f"{1200}x{720}")
        self.generated_frame = 0

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="AyyLmao",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.search_button_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Search",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.search_button_frame_event)
        self.search_button_frame.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create Search frame
        self.search_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.search_frame.grid_columnconfigure(3, weight=0)

        self.entry = customtkinter.CTkEntry(self.search_frame, placeholder_text="Type Channel Name or Video Title",
                                            width=400)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(master=self.search_frame, label_text="Search Results",
                                                                 width=800)
        self.scrollable_frame_buttons = []

        self.search_button = customtkinter.CTkButton(self.search_frame, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text='Search',
                                                     width=80, command=self.search_button_event)

        # create Authorize frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.log_in_button = customtkinter.CTkButton(self.second_frame, text="LOG IN",
                                                     command=self.login, width=1000, height=600)
        self.log_in_button.grid(sticky="nsew")

        # create Account frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create Search Result frame
        self.search_result_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.thumbnail = customtkinter.CTkLabel(self.search_result_frame, text="")

        # select default frame
        self.select_frame_by_name("search")

        # configurations
        #def on_change():
         #   global SearchEntry
         #   SearchEntry = self.entry.get()
         #   print(SearchEntry)

        self.appearance_mode_menu.set("Dark")
        self.search_button_frame.configure(text='Search')
        self.frame_2_button.configure(text='Authorize')

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.search_button_frame.configure(fg_color=("gray75", "gray25") if name == "search" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "Authorize" else "transparent")

        # show selected frame
        if name == "search":
            self.search_frame.grid(row=0, column=1)
            self.entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=20, sticky="ew")
            self.scrollable_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.search_button.grid(row=0, column=3, padx=(10, 5), pady=20, sticky="ne")
        else:
            self.search_frame.grid_forget()
        if name == "Authorize":
            self.second_frame.grid(row=0, column=1)
        else:
            self.second_frame.grid_forget()
        if name == "search_result":
            self.search_result_frame.grid(row=0, column=1)
        else:
            self.search_result_frame.grid_forget()

    def search_button_frame_event(self):
        self.select_frame_by_name("search")

    def frame_2_button_event(self):
        self.select_frame_by_name("Authorize")

    def search_result_button_event(self, video_id):
        self.select_frame_by_name("search_result")
        search_details = get_video_details(youtube, video_id)
        time.sleep(2)
        video_stats = search_details[0]
        video_details = search_details[1]
        channel_id = video_details[0]['Channel_Id']
        channel_stats = get_channel_stats(youtube, channel_id)
        avg_views = int(channel_stats[0]['Views']) / int(channel_stats[0]['Total_videos'])
        views = int(video_stats[0]['Views'])
        print(avg_views)
        print(views)
        #chan_thumb = channel_stats[0]['Thumbnail']
        #print(chan_thumb)
        if self.generated_frame == 1:
            self.thumbnail.grid_forget()
            self.video_title.grid_forget()
        vid_im = thumbnail(video_id)
        self.thumbnail_img = customtkinter.CTkImage(vid_im, size=(480, 360))
        self.thumbnail = customtkinter.CTkLabel(self.search_result_frame, text="", image=self.thumbnail_img)
        self.thumbnail.grid(row=1, column=1, padx=10, pady=(0, 5))
        self.video_title = customtkinter.CTkLabel(self.search_result_frame, text=f"Channel: {video_stats[0]['Title']}",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.video_title.grid(row=0, column=1, padx=10, pady=(5, 0))
        #chan_im = thumbnail(chan_thumb)
        #self.channel_thumbnail_img = customtkinter.CTkImage(chan_im, size=(88, 88))
        #self.channel_thumbnail = customtkinter.CTkLabel(self.search_result_frame, text="", image=self.channel_thumbnail_img)
        #self.channel_thumbnail.grid(row=0, column=2)
        self.channel_title = customtkinter.CTkLabel(self.search_result_frame, text=f"{video_details[0]['Channel_Title']}",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"), justify=customtkinter.LEFT)
        self.channel_title.grid(row=0, column=2, pady=20)
        self.channel_subs = customtkinter.CTkLabel(self.search_result_frame, text=f"Subs:{channel_stats[0]['Subscribers']}",
                                                   text_color=("gray10", "gray90"))
        self.channel_subs.grid(row=0, column=4, pady=5, sticky="w")
        self.sub_button = customtkinter.CTkButton(self.search_result_frame, text="Subscribe",
                                                  command=lambda: subscribe_button_event(self.youtube, channel_id),
                                                  fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                                  hover_color=("gray50", "gray50"), border_color="red",
                                                  border_width=1)
        self.sub_button.grid(row=0, column=3, padx=(10, 0), pady=10, sticky="w")
        self.like_button = customtkinter.CTkButton(self.search_result_frame, image=None,
                                                   text=f"Likes: {video_stats[0]['Likes']}",
                                                   command=lambda: like_button_event(self.youtube, video_id),
                                                   fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                                   hover_color=("gray50", "gray50"), border_color="red",
                                                      border_width=1)
        self.like_button.grid(row=1, column=2, pady=10)
        dislikes = get_dislikes(video_id)
        self.dislike_button = customtkinter.CTkButton(self.search_result_frame, image=None,
                                                      text=f"Dislikes: {dislikes['dislikes']}",
                                                      command=lambda: dislike_button_event(self.youtube, video_id),
                                                      fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                                      hover_color=("gray50", "gray50"), border_color="red",
                                                      border_width=1)
        self.dislike_button.grid(row=1, column=3, padx=10, pady=10)
        if self.youtube:
            self.sub_button.configure(border_color="green")
            self.like_button.configure(border_color="green")
            self.dislike_button.configure(border_color="green")
        self.download_button = customtkinter.CTkButton(self.search_result_frame, image=None, text="Download",
                                                       command=lambda: self.run_downloader(video_id), fg_color=("gray70", "gray30"),
                                                       text_color=("gray10", "gray90"), hover_color=("gray50", "gray50"),
                                                       border_color="green",
                                                       border_width=1)
        self.download_button.grid(row=1, column=4, pady=10)
        self.description = customtkinter.CTkTextbox(self.search_result_frame, width=400)
        self.description.grid(row=2, column=1, pady=10)
        self.description.insert("0.0", f"{video_details[0]['Description']}")
        self.views = customtkinter.CTkLabel(self.search_result_frame, text=f"Views:{video_stats[0]['Views']}",
                                            text_color=("gray10", "gray90"))
        self.views.grid(row=1, column=2, pady=(0, 60))
        if video_details[0]['Description'] == '':
            self.description.insert("0.0", "No Description Found")
        global generated_frame
        self.generated_frame = 1
        self.drawplot(avg_views, views)

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def search_button_event(self):
        if len(self.scrollable_frame_buttons) != 0:
            self.scrollable_frame.grid_forget()
            self.scrollable_frame = customtkinter.CTkScrollableFrame(master=self.search_frame, label_text="Search Results", width=800)
            self.scrollable_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(0, weight=1)
        searchEntry = self.entry.get()
        search_result = youtube_search(args, searchEntry)
        search_titles = search_result[0]
        search_ids = search_result[1]
        for i in range(len(search_titles)):
            self.button = customtkinter.CTkButton(master=self.scrollable_frame, text=f"{search_titles[i]}",
                                                  fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                                  hover_color=("gray50", "gray50"),
                                                  command=lambda j=i: self.search_result_button_event(search_ids[j]))
            self.button.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_buttons.append(self.button)

    def run_downloader(self, video_id):
        Downloader(video_id)

    def login(self):
        self.youtube, LOGGED_IN = get_authenticated_service()

    def drawplot(self, avg_views, views):
        keys = ['average', 'this_video']
        values = [avg_views, views]
        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        NavigationToolbar2Tk(figure_canvas, self)
        axes = figure.add_subplot()
        axes.bar(keys, values)
        axes.set_title('Comparison')
        axes.set_ylabel('Views')
        figure_canvas.get_tk_widget().grid(master=self.search_result_frame, side=tk.TOP, fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
