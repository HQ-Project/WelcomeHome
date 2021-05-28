import pafy
import os

# url = "https://www.youtube.com/watch?v=auGuKPkg-NE"
url = "https://www.youtube.com/watch?v=xY8-vKsJ6QI"

print('0000')

result = pafy.new(url)

print('1111')
# print(result.audiostreams)

min_index = 0
for i, stream in enumerate(result.audiostreams):
    print(i, stream.get_filesize(), stream.bitrate)
    if stream.get_filesize() < result.audiostreams[min_index].get_filesize():
        print('here')
        min_index = i

print(min_index, '22222')

while True:
    try:
        result.audiostreams[i].download("duaibo.m4a")
        break
    except:
        pass

os.system('mocp -l duaibo.m4a')