from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract
import cv2
import re
from tqdm import tqdm
from multiprocessing import Pool
import tempfile

def pdftoimg(path):
    book = path
    save_path = re.sub(r'.pdf', '', path)
    txt_path = '{}/txt'.format(save_path)
    if os.path.exists(txt_path):
        return True
    print('-----Reading Pages------')
    with tempfile.TemporaryDirectory() as temp_path:
        pages = convert_from_path(book, output_folder=temp_path,fmt="jpg", thread_count=4)
        print('----Pages in memory-----')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        i=0
        print('Saving Images -----------')
        for page in tqdm(pages):
            page.save('{0}/{1:04d}.jpg'.format(save_path, i), 'JPEG')
            i+=1
    return True

# def imgtotxt(path):
#     save_path = '{}/txt'.format(path)
#     for page in tqdm(os.listdir(path)):
#         if (os.path.exists('{}/{}.txt'.format(save_path, page)) or not page.endswith('.jpg')):
#             continue
#         text = pytesseract.image_to_string(Image.open('{}/{}'.format(path, page)))
#         # print(page)
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)
#         with open('{}/{}.txt'.format(save_path, page), 'w', encoding='utf-8') as f:
#             f.write(text)
#     return True

def spawn(item):
    # print(item)
    path = item[0]
    page = item[1]
    # print(path)
    save_path = '{}/txt'.format(path)
    # print('spawned # {}'.format(page))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if (not os.path.exists('{}/{}.txt'.format(save_path, page))) and page.endswith('.jpg'):
        text = pytesseract.image_to_string(Image.open('{}/{}'.format(path, page)))
        # print(page)
        with open('{}/{}.txt'.format(save_path, page), 'w', encoding='utf-8') as f:
            f.write(text)
    return True

def imgtotxt(path):
    def iterator(path):
        for page in os.listdir(outdir):
            if page.endswith('.jpg'):
                yield [path,page]
    outdir = path
    pages = len([page for page in os.listdir(outdir) if page.endswith('.jpg')])
    print('Pages : {}'.format(pages))
    p = Pool(processes=4)
    data = list(tqdm(p.imap(spawn, iterator(outdir)), total=pages))
    p.close()
    # print(data)
    return True

def parse():
    for course in os.listdir('Books'):
        print(course + ":")
        for subject in os.listdir('Books/{}'.format(course)):
            print(subject + ':---------------------')
            for book in (os.listdir('Books/{}/{}'.format(course, subject))):
                if book.endswith(".pdf"):
                    name = book
                    name = re.sub(r'.pdf', '', name)
                    # print(name)
                    print(book)
                    path = 'Books/{}/{}/{}'.format(course, subject, book)
                    save_path = re.sub(r'.pdf', '', path)
                    txt_path = '{}/txt'.format(save_path)
                    if os.path.exists(save_path) and os.path.exists(txt_path):
                        if len(os.listdir(save_path))==len(os.listdir(txt_path)):
                            continue
                    if pdftoimg(path=path):
                        if imgtotxt(path=save_path):
                            print('____________OK_____________')
                        else:
                            print('______imgtotxt_error_______')
                    else:
                        print('______pdftoimg_error_______')
        print('-'*35)


if __name__ == "__main__":
    parse()