import re
import json


# TODO: 處理一個標籤塞兩個字的case
# TODO: 修改self.seq後，存檔的功能

class Lyric:
    def __init__(self, file):
        """
        create a Lyric object by open a lyric file
        :param file: file_path
        """
        with open(file, 'r', encoding="utf-8") as f:
            self.text = f.read()
        self.seq = self.__parse(self.text)

    def __parse(self, text):
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

        for line in lines:
            try:
                time_string = re.findall(pat_string, line)[0]
                time_string = time_string.replace('[', '').replace(']', '')
                start, end = time_string.split(',')
                start = int(start)
                time_offset = start
            except IndexError:
                pass

            try:
                time_char = re.findall(pat_char, line)
                # Check if time is relative or absolute (fucking 2 versions ! !)
                chk = time_char[0].split(",")[0].split("<")[1]
                if chk == "0":
                    for char in time_char:
                        char = char.replace('<', '').replace('>', ',')
                        string = char.split(',')
                        start2 = string[0]
                        duration = string[1]
                        char = string[3]
                        start2 = int(start2) + time_offset
                        duration = int(duration)
                        seq.append((start2, duration, char, ''))
                else:
                    for char in time_char:
                        char = char.replace('<', '').replace('>', ',')
                        string = char.split(',')
                        start2 = string[0]
                        duration = string[1]
                        char = string[3]

                        start2 = int(start2)
                        duration = int(duration)
                        seq.append((start2, duration, char, ''))

            except IndexError:
                pass

        return seq

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

    # def save(self, path="test.lyrc"):
    #
    #     with open(path, mode='w') as f:
    #         f.write()
    #     pass

    def get_time_before_vocal(self):
        return self.seq[0][0]

    @staticmethod
    def is_chinese(char):
        if '\u4e00' <= char <= '\u9fff':
            return True
        else:
            return False


if __name__ == '__main__':
    import os
    import sys

    l = Lyric("test_data/a.zrce")
    data = {"total_duration": l.get_total_duration(),
            "data": [s for s in l.seq],
            }
    # json.dump(data, f)pytho
    # f = open("ha.json",mode='wb')
    # f.write(json.dumps(data, ensure_ascii=False).encode('utf8'))
    # f.close()

    sys.stdout.buffer.write(json.dumps(data, ensure_ascii=False).encode('utf8'))
    print()
    # sys.stdout.buffer.write('\n'.encode('utf8'))
    # print(json.dumps(data, ensure_ascii=False))