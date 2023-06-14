from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading

#video_link = "None"


class Downloader(Tk):
    def __init__(self, video_id):
        super().__init__()
        self.video_link = f"https://youtu.be/{video_id}"
        self.title('YouTube Video Downloader')
        self.geometry('500x460+430+180')
        self.resizable(height=FALSE, width=FALSE)
        canvas = Canvas(self, width=500, height=400)
        canvas.pack()
        """Styles for the widgets"""

        label_style = ttk.Style()
        label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))
        button_style = ttk.Style()
        button_style.configure('TButton', foreground='#000000', font='DotumChe')
        self.search_resolution = ttk.Button(self, text='Search Resolution', command=lambda: self.searchThread(self.video_link))
        canvas.create_window(85, 315, window=self.search_resolution)
        self.resolution_label = ttk.Label(self, text='Resolution:')
        canvas.create_window(50, 260, window=self.resolution_label)
        self.video_resolution = ttk.Combobox(self, width=10)
        canvas.create_window(60, 280, window=self.video_resolution)
        self.progress_label = ttk.Label(self, text='')
        canvas.create_window(240, 360, window=self.progress_label)
        self.progress_bar = ttk.Progressbar(self, orient=HORIZONTAL, length=450, mode='determinate')
        canvas.create_window(250, 380, window=self.progress_bar)
        self.download_button = ttk.Button(self, text='Download Video', style='TButton',
                                     command=lambda: self.downloadThread(self.video_link))
        canvas.create_window(240, 410, window=self.download_button)

    def download_video(self, video_link):
        try:
            resolution = self.video_resolution.get()
            if resolution == '':
                showerror(title='Error', message='Please select a video resolution!!')
            elif resolution == 'None':
                showerror(title='Error', message='None is an invalid video resolution!!\n'
                                                 'Please select a valid video resolution')
            else:
                try:
                    def on_progress(stream, bytes_remaining):
                        total_size = stream.filesize

                        def get_formatted_size(total_size, factor=1024, suffix='B'):
                            for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                                if total_size < factor:
                                    return f"{total_size:.2f}{unit}{suffix}"
                                total_size /= factor
                            return f"{total_size:.2f}Y{suffix}"

                        formatted_size = get_formatted_size(total_size)
                        bytes_downloaded = total_size - bytes_remaining
                        percentage_completed = round(bytes_downloaded / total_size * 100)
                        self.progress_bar['value'] = percentage_completed
                        self.progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                        self.update()

                    video = YouTube(video_link, on_progress_callback=on_progress)
                    video.streams.filter(res=resolution).first().download()
                    showinfo(title='Download Complete', message='Video has been downloaded successfully.')

                    self.progress_label.config(text='')
                    self.progress_bar['value'] = 0
                except:
                    showerror(title='Download Error', message='Failed to download video for this resolution')
                    self.progress_label.config(text='')
                    self.progress_bar['value'] = 0
        except:
            showerror(title='Download Error', message='An error occurred while trying to ' \
                                                      'download the video\nThe following could ' \
                                                      'be the causes:\n->Invalid link\n->No internet connection\n' \
                                                      'Make sure you have stable internet connection and the video link is valid')
            self.progress_label.config(text='')
            self.progress_bar['value'] = 0

    def searchResolution(self, video_link):
        if video_link == '':
            showerror(title='Error', message='no video link!')
        else:
            try:
                video = YouTube(video_link)
                resolutions = []
                for i in video.streams.filter(file_extension='mp4'):
                    resolutions.append(i.resolution)
                self.video_resolution['values'] = resolutions
                showinfo(title='Search Complete', message='Check the Combobox for the available video resolutions')
            except:
                showerror(title='Error', message='An error occurred while searching for video resolutions!\n' 
                                                 'Below might be the causes\n->Unstable internet connection\n->Invalid link')

    def searchThread(self, video_link):
        t1 = threading.Thread(target=lambda: self.searchResolution(video_link))
        t1.start()


    def downloadThread(self, video_link):
        t2 = threading.Thread(target=lambda: self.download_video(video_link))
        t2.start()


if __name__ == "__main__":
    downloader = Downloader(video_link)
    downloader.mainloop()
