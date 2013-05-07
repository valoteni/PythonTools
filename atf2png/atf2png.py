import os, sys, struct

def U24(bytes):
  return struct.unpack('<I', bytes + '\0')[0]

def ATFRGB888(data, count, n):
  l = []
  for ct in range(1, count):
    ts = []
    for f in range(1, n):
      len = U24(data.read(3))
      ts.append(data.read(len))
    l.append(ts)
  return l

def ATFRGBA8888(data, count, n):
  return ATFRGB888(data, count, n)
  
def ATFCOMPRESSED(data, count, n):
  dxt1DataLength = U24(data.read(3))
  dxt1Data = data.read(dxt1DataLength)
  dxt1ImageDataLength = U24(data.read(3))
  dxt1ImageData = data.read(dxt1ImageDataLength)
  pvrtcTopDataLength = U24(data.read(3))
  pvrtcTopData = data.read(pvrtcTopDataLength)
  pvrtcBottomDataLength = U24(data.read(3))
  pvrtcBottomData = data.read(pvrtcBottomDataLength)
  pvrtcImageDataLength = U24(data.read(3))
  pvrtcImageData = data.read(pvrtcImageDataLength)
  etc1TopDataLength = U24(data.read(3))
  etc1TopData = data.read(etc1TopDataLength)
  etc1BottomDataLength = U24(data.read(3))
  etc1BottomData = data.read(etc1BottomDataLength)
  etc1ImageDataLength = U24(data.read(3))
  etc1ImageData = data.read(etc1ImageDataLength)
  return [
    dxt1Data,
    dxt1ImageData,
    pvrtcTopData,
    pvrtcBottomData,
    pvrtcImageData,
    etc1TopData,
    etc1BottomData,
    etc1ImageData
  ]

class Atf():
  def __init__(self, data):
    self.data = data
    self.signature = data.read(3) # u8*3
    self.length = U24(data.read(3)) # u24
    tmp = ord(data.read(1))
    self.cubemap = int(tmp >> 7)
    self.format = int(tmp & (0xFF-1))
    self.log2width = pow(2, ord(data.read(1)))
    self.log2height = pow(2, ord(data.read(1)))
    self.count = ord(data.read(1))
    print self.signature
    print self.length
    print self.cubemap
    print self.format
    print self.log2width
    print self.log2height
    print self.count
    self.textureData = self.getTextureData()
    for i in range(0, len(self.textureData)):
      if self.textureData[i]:
        print 'i:%d, len:%d' % (i, len(self.textureData[i]))
  def getTextureData(self):
    if self.cubemap == 0:
      if self.format == 0:
        return ATFRGB888(self.data, self.count, 1)
      elif self.format == 1:
        return ATFRGBA8888(self.data, self.count, 1)
      else:
        return ATFCOMPRESSED(self.data, self.count, 1)
    elif self.cubemap == 1:
      if self.format == 0:
        return ATFRGB888(self.data, self.count, 6)
      elif self.format == 1:
        return ATFRGBA8888(self.data, self.count, 6)
      else:
        return ATFCOMPRESSED(self.data, self.count, 6)
    return None

if __name__ == "__main__":
  inputFile = 'canwu.atf'
  f = open(inputFile, 'rb')
  atf = Atf(f)
  f.close()
