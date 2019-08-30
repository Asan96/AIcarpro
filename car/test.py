#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import pyaudio


def play_audio(self, file_path):
    """
    播放录音
    :return:
    """
    print(str(self.now) + ' start play audio:')
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    print('rate------------------' + str(wf.getframerate()))
    print('channel------------------' + str(wf.getnchannels()))
    print('format------------------' + str(p.get_format_from_width(wf.getsampwidth())))
    data = wf.readframes(self.CHUNK)  # 读取数据
    i = 1
    while len(data) > 0:
        stream.write(data)
        # print('stream---------------'+str(data))
        # time.sleep(1)
        data = wf.readframes(self.CHUNK)
        # print('new stream*************'+str(data))
    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio
    print(str(self.now) + ' reply over！')
