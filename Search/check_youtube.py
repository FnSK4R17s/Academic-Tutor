import re

def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    return re.match(youtube_regex, url)




# youtube_urls_test = [
#     'http://www.youtube.com/watch?v=5Y6HSHwhVlY',
#     'http://youtu.be/5Y6HSHwhVlY',
#     'http://www.youtube.com/embed/5Y6HSHwhVlY?rel=0" frameborder="0"',
#     'https://www.youtube-nocookie.com/v/5Y6HSHwhVlY?version=3&amp;hl=en_US',
#     'http://www.youtube.com/',
#     'http://www.youtube.com/?feature=ytca']


# for url in youtube_urls_test:
#     m = youtube_url_validation(url)
#     if m:
#         suffix = m.group(6)
#         print( 'OK {}'.format(url))
#         print(m.groups())
#         print(suffix)
#         link = "http://www.youtube.com/watch?v={}".format(suffix)
        
        
#     else:
#         print( 'FAIL {}'.format(url))
