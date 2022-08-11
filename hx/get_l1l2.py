# python3   get_l1l2.py   增量镜像名   l1l2.txt
import os
import sys
#掩码
L1E = int(0x00fffffffffffe00)
L2E = int(0x00fffffffffffe00)
#返回10进制数据
def new_size(filename, location, length):
    with open(filename, 'rb') as fs:
        fs.seek(location, 1)
        resu = fs.read(length)
        resu1 = int(resu.hex(), 16)
        return resu1
arg_list = sys.argv
# r"C:\\Users\\admin\\Desktop\\cowimg_Centos_7_x64_7.1"
I = os.stat(arg_list[1])
I_img = arg_list[1]

l1_table_offset = int(new_size(I_img, 40, 8))
l1_size = int(new_size(I_img, 36, 4))
# r"C:\\Users\\admin\\Desktop\\l1l2.txt"
with open(arg_list[2], "a+") as f:
    for i in range(l1_size):
        print(i)
        context_l1 = new_size(I_img, l1_table_offset + i * 8, int(8))
        if context_l1 > 10:
            l2_real = context_l1 & L1E
            print(l2_real)
            for j in range(int(65536/8)):
                context_l2 = new_size(I_img, l2_real + j * 8, int(8))
                if context_l2 > 10:
                    f.write(str(l1_table_offset + i * 8) + " " + str(context_l1) + " " + str(l2_real + j * 8) + " " + str(context_l2) + " 1\n")
