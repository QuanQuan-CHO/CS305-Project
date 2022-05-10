from xml.dom import minidom

if __name__ == '__main__':
    DOMTree = minidom.parse("../www/vod/big_buck_bunny.f4m")
    data = DOMTree.documentElement
    medias = data.getElementsByTagName('media')
    bitrates = []
    for m in medias:
        if m.hasAttribute("bitrate"):
            bitrates.append(int(m.getAttribute("bitrate")))
    print(bitrates)
