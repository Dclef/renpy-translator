import os
import re
import shutil


# 移动rpy文件到当前文件夹
def move_rpy():
    path0 = os.getcwd()
    tran = path0.split('\\')[-1]
    filenames = []
    for root, dirs, files in os.walk(path0):
        for filename in files:
            filenames.append(os.path.join(root, filename))

    filenames = sorted(filenames)
    list1 = []
    for i in filenames:
        if 'rpyc' in i:
            continue
        if 'rpy' in i:
            list1.append(i.split('\n')[0])

    for txt in list1:
        try:
            txtlist = txt.split(tran)
            pathname = txtlist[1].split('\\')
            name = ''
            for i in pathname:
                if i != '':
                    name = name + i
                    if i != pathname[-1]:
                        name = name + '__'

            shutil.move(txt, os.path.join(path0, name))
            print(txt)
            print('>>>\n', os.path.join(path0, name), '\n')
        except:
            pass


# 还原移动后的rpy文件
def restore_rpy():
    path1 = os.getcwd()
    pathlist = os.listdir(path1)
    for i in pathlist:
        if 'rpy' in i and '__' in i:
            inew = i.replace('__', '\\')
            path3 = path1 + '\\' + inew
            with open(os.path.join(path1, i), 'r', encoding='utf8') as f:
                txt = f.read()
            with open(path3, 'w', encoding='utf8') as f:
                f.write(txt)
            os.remove(os.path.join(path1, i))
            print(os.path.join(path1, i))
            print('>>>\n', path3, '\n')


# Google翻译

def make_txt():
    path1 = os.getcwd()
    with open(os.path.join(path1, '1_alltxt.rpy'), 'w', encoding='utf8') as f:
        f.write('')

    rpylist = get_all_rpy(path1)

    for i in rpylist:
        if '1_alltxt.rpy' in i:
            continue
        with open(i, 'r', encoding='utf8') as f:
            text1 = f.read()
        with open(os.path.join(path1, '1_alltxt.rpy'), 'a', encoding='utf8') as f:
            f.write('\nbeginpath:' + i + '\n' + text1 + '\nendpath\n')

    print('创建 ', os.path.join(path1, '1_alltxt.rpy'))

    with open(os.path.join(path1, '1_alltxt.rpy'), 'r', encoding='utf8') as f:
        contentlist = f.readlines()

    with open(os.path.join(path1, '2_googletran.rpy'), 'w', encoding='utf8') as f:
        for xx in range(len(contentlist)):
            list1 = re.findall('    (?:#|old).*?"([^一-\u9fff]*)"', contentlist[xx])
            if list1 != []:
                f.write(str(xx) + '\n')
                if re.findall('^\\d{1,}$', list1[0]) != []:
                    f.write(list1[0] + '.\n\n')
                else:
                    f.write(list1[0] + '\n\n')

    print('创建 ', os.path.join(path1, '2_googletran.rpy'))

    with open(os.path.join(path1, '3_CN.rpy'), 'w', encoding='utf8') as f:
        f.write('')
    print('创建 ', os.path.join(path1, '3_CN.rpy'))


def get_all_rpy(path):
    rpylist = []
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if '.rpy' == os.path.splitext(filename)[1]:
                rpylist.append(os.path.join(parent, filename))
    return rpylist


def return_tran():
  path1 = os.getcwd()
  # 读取翻译后的内容
  with open(os.path.join(path1, '3_CN.rpy'), 'r', encoding='utf8') as f:
    translations = f.readlines()
  # 读取原始文本
  with open(os.path.join(path1, '1_alltxt.rpy'), 'r', encoding='utf8') as f:
    contentlist = f.readlines()
  # 替换原始文本
  for line in translations:
    if re.match(r"^\d+", line):
      num_str = line.split()[0]
      if num_str.isnumeric():
        nub = int(num_str)
        contentlist[nub+1] = re.sub('"(.*)"', '"'+translations[translations.index(line)+1].strip()+'"', contentlist[nub+1])
  # 保存修改后的文本
  with open(os.path.join(path1, '1_alltxt.rpy'), 'w', encoding='utf8') as f:
    f.writelines(contentlist)

  print("翻译内容已导入1_alltxt.rpy")
def to_file():
    path1 = os.getcwd()
    with open(os.path.join(path1, '1_alltxt.rpy'), 'r', encoding='utf8') as f:
        txt1 = f.read()

    filelist1 = re.findall('beginpath[\\w\\W]*?endpath', txt1)
    for ix in filelist1:
        pathname = re.findall('beginpath:(.*?)\n', ix)[0]
        with open(pathname, 'w', encoding='utf8') as f:
            f.write(ix)
        with open(pathname, 'r', encoding='utf8') as f:
            lines = f.readlines()
        lines = lines[1:-2]
        lines.append('\n')
        with open(pathname, 'w', encoding='utf8') as f:
            f.writelines(lines)

    print('1_alltxt.rpy已被分割为原rpy文件')


if __name__ == '__main__':
    while True:
        inp = input("请按序列号操作\n源文件操作：(1.源文件移动 2.源文件还原) 翻译文件操作：(3.文本合并 4.文本分割 5.文本还原) \n")
        if inp == '1':
            move_rpy()
        elif inp == '2':
            restore_rpy()
        elif inp == '3':
            make_txt()
        elif inp == '4':
            return_tran()
        elif inp == '5':
            to_file()
        else:
           break