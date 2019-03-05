import re
import json
import os

# TODO: 修改self.seq後，存檔的功能

DEFAULT_PITCH = "A4"
NO_PITCH = ""
DEFAULT_CHAR_VOCAL_FILE = ""
NO_CHAR_VOCAL_FILE = ""
NEW_LINE = "[NEW_LINE]"


class Lyric:
    def __init__(self, file):
        """
        create a Lyric object by open a lyricData file
        :param file: file_path
        """

        if os.path.splitext(file)[-1] == "json":
            with open(file, 'r', encoding="utf-8") as f:
                self.data = json.load(f)
                self.seq = self.data['data']
                self.meta_data_string = self.data['meta_data_string']

        else:
            with open(file, 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.meta_data_string = ""
            self.seq = self.__parse_zrce(self.text)
            self.data = {"total_duration": self.get_total_duration(),
                         "data": self.seq,
                         "lyric_file_path": file,
                         "background_music_path": "",
                         "char_vocal_folder": "",
                         "meta_data_string": self.meta_data_string,
                         "format_version": 1.0
                         }

    def __parse_zrce(self, text):
        """
        :param text:
        :return: list
                    a list of tuple(start_time(ms),duration(ms),char)
                    ex.[(1329, 1700, '小'), (3029, 601, '幸'), (3630, 1003, '運')]
        """
        lines = text.splitlines()
        seq = []
        time_offset = 0
        pat_string = re.compile("\[.+,.+\]")
        pat_char = re.compile("<\d+,\d+,\d+>[^<]+")
        self.meta_data_string = ""

        for line in lines:

            line_seq = []

            try:
                time_string = re.findall(pat_string, line)[0]
                time_string = time_string.replace('[', '').replace(']', '')
                line_start, line_duration = time_string.split(',')
                line_start, line_duration = int(line_start), int(line_duration)
                time_offset = line_start
            except IndexError:
                self.meta_data_string += line + '\n'
                continue

            try:
                time_char = re.findall(pat_char, line)
                # Check if time is relative or absolute (fucking 2 versions ! !)
                chk = time_char[0].split(",")[0].split("<")[1] == "0"

                for char in time_char:
                    char = char.replace('<', '').replace('>', ',')
                    string = char.split(',')
                    char_start = string[0]
                    char_duration = string[1]
                    char = string[3]
                    if chk:
                        char_start = int(char_start) + time_offset
                    else:
                        char_start = int(char_start)
                    char_duration = int(char_duration)
                    line_seq.append((char_start, char_duration, char, DEFAULT_PITCH, DEFAULT_CHAR_VOCAL_FILE))

            except IndexError:
                continue
            # seq.append((line_start, line_duration, NEW_LINE, NO_CHAR_VOCAL_FILE, DEFAULT_CHAR_VOCAL_FILE))
            seq.extend(line_seq)

        return seq

    def to_json_string(self):
        data = {"total_duration": self.get_total_duration(),
                "data": [s for s in self.seq],
                "lyric_file_path": "test_data/a.zrce",
                "background_music_path": "",
                "char_vocal_folder": "",
                "meta_data_string": self.meta_data_string,
                "format_version": 1.0
                }
        return json.dumps(data, ensure_ascii=False)

    def to_zrce_string(self):

        text_seq = [f'<{s[0]},{s[1]},0>{s[2]}'
                    if s[2] != NEW_LINE
                    else f'\n[{s[0]},{s[1] + s[0]}]'
                    for s in self.seq]

        return self.meta_data_string.strip() + ''.join(text_seq).strip()

    def get_total_duration(self):
        last_time = self.seq[-1][0]
        last_duration = self.seq[-1][1]
        return last_time + last_duration

    def get_lyric(self) -> object:
        lyric = ""
        for item in self.seq:
            lyric += item[2]
        return lyric

    def __len__(self):
        len(self.seq)

    def __getitem__(self, idx):
        return self.seq[idx]

    def get_time_before_vocal(self):
        return self.seq[0][0]

    @staticmethod
    def is_chinese(char):
        if '\u4e00' <= char <= '\u9fff':
            return True
        else:
            return False


if __name__ == '__main__':
    import sys

    l = Lyric("test_data/a.zrce")
    # l.to_lyrc()
    # print(l.to_zrce_string())
    # sys.stdout.buffer.write(l.to_zrce_string().encode('utf8'))
    sys.stdout.buffer.write(l.to_json_string().encode('utf8'))
    print()
    # sys.stdout.buffer.write('\n'.encode('utf8'))
    # print(json.dumps(data, ensure_ascii=False))
