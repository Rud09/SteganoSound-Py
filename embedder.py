import wave as w
import bitarray as b
import headerManager as hm
import os
import sys


def embed(fpath, mpath):
    song = w.open(fpath, mode='rb')
    songBytes = bytearray(list(song.readframes(song.getnframes())))

    msg = open(mpath, "rb")
    msgBits = b.bitarray()
    msgBits.fromfile(msg)

    hdr = hm.formHeader(mpath, os.path.getsize(mpath))
    hdrBits = b.bitarray()
    hdrBits.fromstring(hdr)

    bits = b.bitarray(hdrBits)
    bits.extend(msgBits)

    if bits.length() > len(songBytes):
        print("Data File too big to be hidden in given WAV File!!")
        sys.exit(1)

    for i, bit in enumerate(bits):
        songBytes[i] = (songBytes[i] & 254) | bit

    songMod = bytes(songBytes)

    with w.open("Mod"+os.path.basename(fpath), "wb") as fd:
        fd.setparams(song.getparams())
        fd.writeframes(songMod)

    print("File Hidden Successully!!")
    song.close()
