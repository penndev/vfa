'官方flv标准介绍  https://www.adobe.com/content/dam/acom/en/devnet/flv/video_file_format_spec_v10.pdf'

class FlvTag:
    tagTypeItem = {8:"Audit",9:"Video",18:"Script"}
    def __init__(self,data) -> None:
        '分析flv tag header 内容获取datasize'
        self.data = data
        self.tagType = data[0]
        self.dataSize = int.from_bytes(data[1:4], byteorder='big')
        self.timeStamp = int.from_bytes(data[4:7], byteorder='big')
        self.timeStampExtended = data[7]
        self.streamID = data[8:11]
        self.previousTagSize = 0

    def setData(self,data):
        '解码媒体源数据'
        self.data += data
        self.previousTagSize = self.tagSize = int.from_bytes(data[self.dataSize:], byteorder='big')

    def getTagType(self):
        return self.tagTypeItem[self.tagType]
    

class FlvHeader:
    def __init__(self,data) -> None:
        self.data = data
        self.previousTagSize = int.from_bytes(self.data[9:14], byteorder='big')

class Struct:
    header = None
    body = []
    def __init__(self,flv) -> None:
        self.header = FlvHeader(flv.read(13))
        while(True):
            header = flv.read(11)
            if(header == b''):
                break
            tag = FlvTag(header)
            tag.setData(flv.read(tag.dataSize + 4))
            self.body.append(tag)
    def getBody(self):
        tags = []
        for item in self.body:
            tags.append(item.getTagType())
        return tags

def newFLv(pwd):
    with open(pwd, 'rb') as flv:
        return Struct(flv)

if __name__ == "__main__":
    strflv = newFLv("./docs/test.flv")
    print(strflv.body[22].tagType)


# with open("test.h264",'wb') as h:
#     for tag in flvAnalyze.body:
#         if tag.tagType == 9:
#             if tag.tag.Type == 1:
#                 for nalu in tag.tag.Data:
#                     h.write(bytes([0,0,0,1]))
#                     h.write(bytes(nalu))

# with open("test.aac",'wb') as h:
#     for tag in flvAnalyze.body:
#         if tag.tagType == 8:
#             if tag.tag.Type == 1:
                # adtsHeader = [0xff, 0xf1, 0x4c, 0x80,0x00,0x00,0xfc]
                # adtsLen = len(tag.tag.Data)+7
                # adtsLen = adtsLen << 5
                # adtsLen = adtsLen | 0x1f
                # adtsHeader[4:6] = adtsLen.to_bytes(2,'big')
                # h.write(bytes(adtsHeader))
                # h.write(bytes(tag.tag.Data))