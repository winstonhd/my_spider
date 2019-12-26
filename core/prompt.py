"""读取用户的输入"""
import os
import tempfile  # 在程序执行时创建一个临时文件或目录，使用完之后自动销毁


def prompt(default=None):
    editor = 'nano'
    with tempfile.NamedTemporaryFile(mode='r+') as tmpfile:  # r+ 表示可读写的文件
        if default:
            tmpfile.write(default)   # 一般的文件流操作都包含缓冲机制，write方法不直接将数据写入文件，而是写入内存中特定的缓冲区。
            tmpfile.flush()  # flush方法用来刷新缓冲区，将缓冲区中的数据立刻写入文件，同时清空缓冲区。
        child_pid = os.fork()  # 只在Unix有效，创建子进程，将当前的进程（父进程）复制一份（子进程），然后分别在父进程和子进程内返回。子进程永远返回0，父进程返回子进程的pid。
        is_child = child_pid == 0

        if is_child:  # 如果是子进程
            # os.execvp:执行一个新的程序，用新的程序替换当前子进程的进程空间，在执行参数传递过去的命令时使用PATH环境变量来查找命令
            os.execvp(editor, [editor, tmpfile.name])  # tmpfile.name 包含了临时文件的文件名，这个文件名是系统给的
        else:  # 如果是父进程
            os.waitpid(child_pid, 0)  # 只在Unix有效，等待子进程结束并杀死该子进程
            tmpfile.seek(0)  # 移动文件读取指针到文件开头
            return tmpfile.read().strip()  # strip() 移除字符串头恩爱的空格
