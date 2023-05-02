from pytube import Youtube


def search_resolution(video_url):
    try:
        video = Youtube(video_url)
        resolutions = []
        for i in video.streams.filter(file_extension='mp4'):
            resolutions.append(i.resolution)
            # adding the resolutions to the combobox
            #video_resolution['values'] = resolutions
    except:
        showerror(title='Error', message='An error occurred while searching for video resolutions!\n'\
                 'Below might be the causes\n->Unstable internet connection\n->Invalid link')


def download_video(video_url, resolution):
    try:
        #resolution = resolution.get
        try:
            def on_progress(stream, chunk, bytes_remaining):
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
                #progress_bar['value'] = percentage_completed
                #progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                #App.update()

            video = Youtube(video_url, on_progress_callback=on_progress)
            video.streams.filter(res=resolution).first().download()
            showinfo(title='Download Complete', message='Video has been downloaded successfully.')
            #progress_label.config(text='')
            #progress_bar['value'] = 0
        except:
            showerror(title='Download Error', message='Failed to download video for this resolution')
            #progress_label.config(text='')
            #progress_bar['value'] = 0
    except:
        showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the video\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                    'Make sure you have stable internet connection and the video link is valid')
        #progress_label.config(text='')
        #progress_bar['value'] = 0

try:
    link = input('link: ')
    video = download_video(link, resolution=input())
    print(f'"{video}" downloaded successfully')
except:
    print(f'Failed to download video\nThe '\
          'following might be the causes\n->No internet '\
          'connection\n->Invalid video link')
