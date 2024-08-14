# 一个效率较低的文本文件读取器
# 之前考虑到扭结种类很多，因此使用了二分查找法
# 后来想了想好像也没必要支持那么多种类的扭结

import json
import os
import re
import sys
from knotname_reg import knotname_reg

# 指定文本内容
# 获取文本内容中从扭结不变量到扭结名称的对应关系
# 一个扭结不变量可能对应着多种不同的扭结名称
def slow_dict_reader_raw(content: str) -> dict:
    ans = {}
    for line in content.split("\n"): # 逐行读入文件中的所有内容
        line = line.strip()
        if line == "" or line[0] == "#":
            continue # 跳过文件中的空行或者文件中以井号开头的行
        assert re.match(r"^\[.*\|.*\]$", line) is not None
        lpart, rpart = line[1:-1].split("|", 1) # lpart: 扭结不变量, rpart: 扭结名称
        rpart = knotname_reg(rpart)             # 做 writhe 修正
        if ans.get(lpart) is None:
            ans[lpart] = []
        if rpart not in ans[lpart]: # 将扭结不变量追加到指定的序列中
            ans[lpart].append(rpart)
    return ans

# 指定文本文件路径
# 获取文本文件内容中从扭结不变量到扭结名称的对应关系
def slow_dict_reader(filepath: str) -> dict:
    assert os.path.isfile(filepath)
    return slow_dict_reader_raw(open(filepath).read())

# 从标准输入流输入一个文本串，解析出对应关系 dict
# 并向标准输出流输出一个 json
def main():
    input_content = sys.stdin.read()
    print(json.dumps(slow_dict_reader_raw(input_content)))

if __name__ == "__main__":
    main()