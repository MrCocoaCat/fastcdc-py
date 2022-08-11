# python3    create_record.py   增量镜像名   选择镜像名   拷贝目的地   l1l2.txt   fin_record   map文件
import os
import sys
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
# r"C:\\Users\\admin\\Desktop\\cowimg_Centos_7_x64_7.1"
I_img = arg_list[1]
img_off = 0
# map
with open(arg_list[6], "r") as f:
    lines = f.readlines()
    for line in lines:
        img_length = int(line.split(' ')[1], 16)
        img_start = int(line.split(' ')[2], 16)
        # "/root/cowimg/cowimg_Centos_7_x64_7.1"
        if str(line.split(' ')[3]) == arg_list[2] + "\n":
            # r"C:\\Users\\admin\\Desktop\\create_Centos7"
            new_read(I_img, img_start, img_length, arg_list[3], img_off)
            # r"C:\\Users\\admin\\Desktop\\l1l2.txt"
            with open(arg_list[4], "r") as f_l1l2:
                lines1 = f_l1l2.readlines()
                for line1 in lines1:
                    l1_loca = int(line1.split(' ')[0])
                    l1_content = int(line1.split(' ')[1])
                    l2_loca = int(line1.split(' ')[2])
                    l2_content = int(line1.split(' ')[3])
                    l2_real = l2_content & L2E
                    if l2_real == img_start:
                        print(l2_real)
                        # r"C:\\Users\\admin\\Desktop\\fin_record.txt"
                        with open(arg_list[5], "a+") as f_fin:
                            f_fin.write(str(l1_loca) + " " + str(l1_content) + " " + str(l2_loca) + " " + str(l2_content) + " " + str(img_off) + " " + str(img_length) + " 1\n")
                        break
            img_off += img_length
