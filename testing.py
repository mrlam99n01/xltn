import pvporcupine
import pyaudio
import struct
import pyautogui
import pyautogui  # to press a button to play the game
handle = pvporcupine.create(keyword_paths=['go_right.ppn','go_left.ppn','go_down.ppn'])
pyautogui.click(120,22)
print(handle.frame_length)
def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=handle.frame_length,input_device_index=None)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return  pcm

while True:
    pcm = get_next_audio_frame()
    keyword_index = handle.process(pcm)
    if keyword_index == 0:
        pyautogui.press('right')
        print("right")
    if keyword_index == 1:
        pyautogui.press('left')
        print("left")
    if keyword_index == 2:
        pyautogui.press('up')
        print("up")

