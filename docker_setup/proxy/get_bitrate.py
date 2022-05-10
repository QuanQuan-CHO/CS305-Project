# _*_ coding : utf-8 _*_
# @Time : 2022/5/10 14:43
# @Author : 黄柯睿
# @File : Demo
# @Project : CS305-Project\

from xml.dom import minidom

if __name__ == '__main__':
    DOMTree = minidom.parse("big_buck_bunny.f4m")
    data = DOMTree.documentElement
    medias = data.getElementsByTagName('media')
    bitrates = []
    for m in medias:
        if m.hasAttribute("bitrate"):
            bitrates.append(int(m.getAttribute("bitrate")))
    print(bitrates)
