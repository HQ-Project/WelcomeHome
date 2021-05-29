import pafy
import os

url = "https://www.youtube.com/watch?v=ZbZSe6N_BXs"
file_name = "happy.m4a"

print('0000')

result = pafy.new(url)

print('1111')

min_index = 0
for i, stream in enumerate(result.audiostreams):
    print(i, stream.get_filesize(), stream.bitrate)
    if stream.get_filesize() < result.audiostreams[min_index].get_filesize():
        min_index = i

print(min_index, '22222')

while True:
    try:
        result.audiostreams[i].download(file_name)
        break
    except:
        pass

os.system("mocp -l {}".format(file_name))