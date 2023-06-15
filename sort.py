import shutil, sys
from pathlib import Path

DIR_SORT = Path(sys.argv[1])
DIR_DICT = {"images": ('JPEG', 'PNG', 'JPG', 'SVG'),
             "video": ('AVI', 'MP4', 'MOV', 'MKV'),
             "documents": ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
             "audio": ('MP3', 'OGG', 'WAV', 'AMR'),
             "archives": ('ZIP', 'GZ', 'TAR')}
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()


def make_dir(parent_path, dirs):
    for directory in dirs:
        Path(parent_path, directory).mkdir()


def delete_empty_folders(folder):
    for f in folder.iterdir():
        if f.is_dir():
            try:
                f.rmdir()
            except OSError:
                delete_empty_folders(f)


def unzipping(folder):
    for file in folder.iterdir():
        Path(Path(folder, file.stem)).mkdir()
        shutil.unpack_archive(file, Path(folder, file.stem))
        file.unlink()


def sorting(folder):
    for k_dir in DIR_DICT:
        for file_suffix in DIR_DICT[k_dir]:
            filtered_files = tuple(folder.glob("**/*." + file_suffix))
            for file in filtered_files:
                shutil.move(file, Path(folder, k_dir))


def normalize(string):

    string = string.translate(TRANS)
    for letter in string:
        if not(letter.isalnum()) and letter not in ":\\/":
            string = string.replace(letter, "_")
    return string


def rename_folder(folder):
    for f in folder.iterdir():
        if f.is_dir():
            folder_ = str(f)[len(str(DIR_SORT))+1:]
            new_f = Path(DIR_SORT, normalize(str(folder_)))
            if f != new_f:
                f = f.rename(new_f)
            rename_folder(f)
        elif f.is_file():
            new_f = Path(f.parent, normalize(str(f.stem)) + f.suffix)
            if f != new_f:
                f.rename(new_f)


def main():
    rename_folder(DIR_SORT)
    make_dir(DIR_SORT, DIR_DICT.keys())
    sorting(DIR_SORT)
    unzipping(Path(DIR_SORT, "archives"))
    delete_empty_folders(DIR_SORT)


if __name__ == "__main__":
    main()
