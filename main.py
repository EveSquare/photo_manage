import shutil ,os ,pathlib ,datetime, time, glob
from PIL import Image, ExifTags

img_dir_path = "./img/"

img_dir = glob.glob(f"{img_dir_path}*")
files = []

def get_exif_datetime(path: str):
    # format 2020:11:26 10:48:48
    path = f"{img_dir_path}{path}"
    try:
        img = Image.open(path)

        exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
        for k, v in exif.items():
            if k == "DateTimeOriginal":
                return v
    except:
        return

def format_text(text: str):
    text_list = list(text)
    text_list[4] = '.'
    text_list[7] = '_'
    # またリストから文字列へ戻す
    text_changed = "".join(text_list)
    return text_changed[:10]

def make_folder(date: str):
    os.makedirs(f'./{date}', exist_ok=True)
    print(f"ファイルを生成:{date}")

def file_move(file_name: str, date: str):
    try:
        shutil.move(f'{img_dir_path}{file_name}', f'./{date}')
        print(f"ファイルを移動:{img_dir_path}{file_name} to ./{date}")
    except:
        os.remove(img_dir_path+file_name)
        print(f"ファイルを削除:{img_dir_path}{file_name}")

def creation_date(path_to_file):
    return os.stat(path_to_file).st_mtime


if __name__ == "__main__":
    for row in img_dir:
        files.append(row[6:])

    pics = [".jpg",".jpeg","png"]
    videos = [".mp4",".avi"]

    for i in files:
        # print(i[-4:])
        if i[-4:] in pics:
            # if get_exif_datetime(i) != None:
            file_datetime = format_text(get_exif_datetime(i))
            make_folder(file_datetime)
            file_move(i,file_datetime)
        elif i[-4:] in videos:
            video_datetime = datetime.datetime.fromtimestamp((creation_date(img_dir_path+i)))
            video_datetime_f = format_text(str(video_datetime))
            make_folder(video_datetime_f)
            file_move(i,video_datetime_f)
