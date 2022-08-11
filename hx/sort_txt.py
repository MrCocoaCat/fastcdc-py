# python3    sort.py    fin_record.txt    new_record.txt
import sys
arg_list = sys.argv
sort_new = []
# r"C:\\Users\\admin\\Desktop\\fin_record.txt"
with open(arg_list[1], "r") as f:
    lines = f.readlines()
    for line in lines:
        l2_content = int(line.split(' ')[3])
        if l2_content not in sort_new:
            sort_new.append(l2_content)
    sort_new.sort()
    print(sort_new)
for i in sort_new:
    with open(arg_list[1], "r") as f1:
        lines1 = f1.readlines()
        for line1 in lines1:
            l2_content1 = int(line1.split(' ')[3])
            print(hex(l2_content1))
            if l2_content1 == int(i):
                with open(arg_list[2], "a+") as f2:
                    f2.write(line1)
# r"C:\\Users\\admin\\Desktop\\new_record.txt"
