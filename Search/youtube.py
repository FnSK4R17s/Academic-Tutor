from pytube import YouTube
import os

#To Do : Auto select video quality : Done /

def yt_down(link, destination):
    try:
        yt = YouTube(link, on_progress_callback=progress_Check)
    except:
        print("YouTube URL not reachable, Skipping.......")
        return "none", False
    vid_name = yt.title
    print(vid_name)

    thumb = yt.thumbnail_url
    print("Thumbnail : " + thumb)

    vid = yt.streams.filter(progressive=True).first()

    if not os.path.exists(destination):
        os.makedirs(destination)

    print("Downloading  [*]")
    global file_size
    file_size = vid.filesize
    vid.download(destination)
    print()
    print("Done !")
    return vid_name, True

# on_progress_callback takes 4 parameters.
def progress_Check(stream=None, chunk=None, file_handle=None, remaining=None):
	#Gets the percentage of the file that has been downloaded.
	percent = (100*(file_size-remaining))/file_size
	print("\r{:00.0f}% downloaded".format(percent), end='', flush=True)

def check():
    link = input("Enter Youtube link : ")
    try:
        destination = input("Enter destination : ")
    except:
        destination = "test"
    yt_down(link, destination)
    again = check()
    
if __name__ == "__main__":
    check()