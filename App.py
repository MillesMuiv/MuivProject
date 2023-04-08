import customtkinter
from Search import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("AppTitle")
        self.geometry(f"{1100}x{580}")
        searchval = customtkinter.StringVar()

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

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create Search frame
        self.search_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.search_frame.grid_columnconfigure(3, weight=1)

        self.entry = customtkinter.CTkEntry(self.search_frame, placeholder_text="Type Channel Name or Video Title", width=400)
        self.entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=20, sticky="new")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(master=self.search_frame, label_text="Search Results", width=800)
        self.scrollable_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_buttons = []

        self.search_button = customtkinter.CTkButton(self.search_frame, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text='Search', command=self.search_button_event)
        self.search_button.grid(row=0, column=3, padx=(10, 5), pady=20, sticky="ne")

        # create Youtube frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create Twitch frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("search")

        # configurations
        #def on_change():
         #   global SearchEntry
         #   SearchEntry = self.entry.get()
         #   print(SearchEntry)

        self.appearance_mode_menu.set("Dark")
        self.search_button_frame.configure(text='Search')

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.search_button.configure(fg_color=("gray75", "gray25") if name == "search" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "search":
            self.search_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.search_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def search_button_frame_event(self):
        self.select_frame_by_name("search")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

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
        for i in range(len(search_result)):
            button = customtkinter.CTkButton(master=self.scrollable_frame, text=f"{search_result[i]}",
                                             fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"),
                                             hover_color=("gray50", "gray50"))
            button.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_buttons.append(button)


if __name__ == "__main__":
    app = App()
    app.mainloop()
