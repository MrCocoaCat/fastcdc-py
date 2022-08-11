# python3    testmap.py   存有数据块的缓存   目标cow   new_record
import os
import math
import codecs
import sys
import datetime
starttime = datetime.datetime.now()
#掩码
L1E = int(0x00fffffffffffe00)
L2E = int(0x00fffffffffffe00)
l1_off = 0
l2_off = 0
#拷贝父镜像数据至增量镜像，location为起始地址，length为长度
def new_read(filename, location, length, dst_filename, dst_location):
    with open(filename, 'rb') as fs:
        fs.seek(location, 1)
        resu = fs.read(length)
        writeback(dst_filename, resu, dst_location)
#返回10进制数据
def new_size(filename, location, length):
    with open(filename, 'rb') as fs:
        fs.seek(location, 1)
        resu = fs.read(length)
        resu1 = int(resu.hex(), 16)
        return resu1

#l1l2写入数据
def writeback(filename, content, location):
    with open(filename, 'rb+') as fs:
        fs.seek(location+len(content))
        fs.seek(location)
        fs.write(content)
arg_list = sys.argv

I = os.stat(arg_list[1])
I_img = arg_list[1]
cow = os.stat(arg_list[2])
cow_img = arg_list[2]
refcount_table_offset = int(new_size(cow_img, 48, 8))
refcount_offset = int(new_size(cow_img, refcount_table_offset, 8))
ref_now = 0

with open(arg_list[3], "r") as f:
    lines = f.readlines()
    for line in lines:
        l1_start = int(line.split(' ')[0])
        l1_content = int(line.split(' ')[1])
        l2_start = int(line.split(' ')[2])
        l2_content = int(line.split(' ')[3])
        l2_content_copy = l2_content
        off_cluster = int(line.split(' ')[4])
        off_length = int(line.split(' ')[5])
        if new_size(cow_img, l1_start, 8) != l1_content:
            l1_content = str(hex(l1_content))[2:]
            # print(l1_content)
            l1_content_a1 = ''
            for j in range(16):
                if (j + 1) % 2 != 0:
                    l1_content_a1 = l1_content_a1 + r'\x' + l1_content[j] + l1_content[j + 1]
            l1_content = l1_content_a1.encode(encoding='ascii', errors='strict')
            l1_content = codecs.escape_decode(l1_content, "hex-escape")
            writeback(cow_img, l1_content[0], l1_start)
        num_cluster = int(math.ceil(off_length / 65536))
        # print(num_cluster)
        i = 0
        while i < num_cluster:
            # print(i)
            # print(num_cluster)
            l2_content = str(hex(l2_content_copy + i*65536))[2:]
            print(l2_content)
            l2_content_a1 = ''
            for j in range(16):
                if (j + 1) % 2 != 0:
                    l2_content_a1 = l2_content_a1 + r'\x' + l2_content[j] + l2_content[j + 1]
            l2_content = l2_content_a1.encode(encoding='ascii', errors='strict')
            l2_content = codecs.escape_decode(l2_content, "hex-escape")
            writeback(cow_img, l2_content[0], l2_start + i * 8)
            i = i + 1
        # print("1")
        new_read(I_img, off_cluster, off_length, cow_img, l2_content_copy & L2E)
        # cow = os.stat(r"C:\\Users\\admin\\Desktop\\cow_Centos7.1")
        # ref = int(cow.st_size)
        ref = (l2_content_copy & L2E) + off_length
        if ref % 65536 == 0:
            ref = int(ref / 65536)
        else:
            ref = int(ref / 65536) + 1
        print(ref)
        while 1:
            if ref != ref_now:
                writeback(cow_img, b'\x00\x01', refcount_offset + ref_now * 2)
                ref_now += 1
            else:
                break
endtime = datetime.datetime.now()
print(starttime)
print(endtime)
