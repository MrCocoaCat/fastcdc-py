import json
import os
import subprocess
# ROOT 路径，本脚本所在的绝对路径的上层路径
TOOLS_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(TOOLS_PATH)

import traceback

# 执行系统命令函数
def run_command(cmd, redirect_output=True, check_exit_code=True, shell_bool=True, path=ROOT):
    """
    Runs a command in an out-of-process shell, returning the
    output of that command.  Working directory is ROOT.
    执行命令，在一个程序外的shell进程,
    执行目录为ROOT
    """
    # subprocess模块用于产生子进程
    # 如果参数为redirect_output ，则创建PIPE
    if redirect_output:
        stdout = subprocess.PIPE
    else:
        stdout = None
    # cwd 参数指定子进程的执行目录为path，执行cwd 函数
    proc = subprocess.Popen(cmd, cwd=path, stdout=stdout, shell=shell_bool, stderr=subprocess.PIPE)
    # 如果子进程输出了大量数据到stdout或者stderr的管道，并达到了系统pipe的缓存大小的话，
    # 子进程会等待父进程读取管道，而父进程此时正wait着的话，将会产生死锁。
    # Popen.communicate()这个方法会把输出放在内存，而不是管道里，
    # 所以这时候上限就和内存大小有关了，一般不会有问题。
    # 使用communicate() 返回值为 (stdoutdata , stderrdata )
    communicate = proc.communicate()
    stdoutdata = bytes.decode(communicate[0])
    stderrdata = bytes.decode(communicate[1])
    if check_exit_code and proc.returncode != 0:
        # 程序不返回0，则失败
        print('Command "%s" failed.%s ,%s' % (cmd, stdoutdata, stderrdata))
    return proc.returncode, (stdoutdata, stderrdata, proc.pid)


def read_by_offset(path, qcow2_map_list2):
    try:
        f1 = open(path, 'rb')
        path_write_bash = "/mnt/liyubo/test_out_dir/"

        for i, val in enumerate(qcow2_map_list2):
            print(val, i, len(qcow2_map_list2))
            start = val['start']
            length = val['length']
            offset = val['offset']
            first_read = length
            if i == len(qcow2_map_list2) - 1:
                sec_read = 0
            else:
                next_offset = qcow2_map_list2[i+1]['offset']
                sec_read = next_offset - offset - first_read
                if sec_read < 0:
                    raise Exception("sec_read < 0")
            if i == 0:
                data = f1.read(offset)
                print(len(data))
                path_write = path_write_bash + str(i)
                f2 = open(path_write, 'wb')
                f2.write(data)
                f2.close()
                f3 = open(path_write, 'rb')
                date_com = f3.read()
                f3.close()
                if date_com != data:
                    raise Exception("date is different")
            data1 = f1.read(first_read)
            path_write_a = path_write_bash + str(i) + "a"
            f2 = open(path_write_a, 'wb')
            f2.write(data1)
            f2.close()
            f3 = open(path_write_a, 'rb')
            date_com = f3.read()
            f3.close()
            if date_com != data1:
                raise Exception("date is different")
            print("first_read:{A} f1.tell(): {B}  ".format(A=first_read, B=f1.tell()))
            if len(data1) != first_read:
                raise Exception("not same ,", len(data1), first_read)
            if sec_read != 0:
                path_write_b = path_write_bash + str(i) + "b"
                data2 = f1.read(sec_read)
                f2 = open(path_write_b, 'wb')
                if len(data2) != sec_read:
                    print("not same ,", len(data2), sec_read)
                f2.write(data2)
                f2.close()
                f3 = open(path_write_b, 'rb')
                date_com = f3.read()
                f3.close()
                if date_com != data2:
                    raise Exception("date is different")
                print("sec_read:{A} f1.tell(): {B}, offset:{C}".format(A=sec_read,
                                                                       B=f1.tell(),
                                                                       C=offset))
                if f1.tell() != next_offset:
                    print("f1.tell() != offset)")
            else:
                print("No sec_read")
                if f1.tell() != next_offset:
                    print("f1.tell() != offset)")
    except Exception as e:
            traceback.format_exc()
    return None


def get_qemu_info(path="/home/liyubo/Desktop/test_dir/u04.img"):
    cmd = "qemu-img map --output=json {IMG}".format(IMG=path)
    code, data = run_command(cmd)
    qcow2_map_list = json.loads(data[0])
    temp_list1 = [i for i in qcow2_map_list if i['zero'] is False]
    temp_list2 = sorted(temp_list1, key=lambda k: k["offset"])
    qcow2_map_offset = []
    qcow2_map_no_offset = []
    for i, val in enumerate(temp_list2):
        length = val['length']
        offset = val['offset']
        first_read = length
        if i == 0:
            qcow2_map_offset.append([0, offset , False])
        if i == len(temp_list2) - 1:
            qcow2_map_offset.append([offset, offset + length, True])
        else:
            temp1 = [offset, offset + length, True]
            # print(temp1)
            qcow2_map_offset.append(temp1)
            next_offset = temp_list2[i + 1]['offset']
            sec_read = next_offset - offset - first_read
            if sec_read > 0:
                temp2 = [offset + length, next_offset, False]
                # print(temp2)
                qcow2_map_offset.append(temp2)
    return qcow2_map_offset
