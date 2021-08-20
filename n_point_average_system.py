import wave
import matplotlib.pyplot as plt
from scipy import signal as sg
import numpy as np
import playsound
from scipy.io.wavfile import write

def n_point_average_system(wavedata, Fs, n):
    # wavedata:音声データ, Fs:サンプリング周波数, n:n点平均のn
    # y[n] = 1/n Σ_{k=0}^{n-1} x[n-k]
    # 両辺X変換 -> Y(z) = 1/n Σ_{k=0}^{n-1} z^{-k}X(z)
    # 伝達関数 H(z) = 1/n Σ_{k=0}^{n-1}z^{-k}
    # 伝達関数の一般形 H(Z) = Σ_{k=0}^{n-1}b_k * x^{-k} / Σ_{k=0}^{n-1}a_k * x^{-k}

    a = [0]
    b = [1/n for _ in range(n)]
    output = sg.lfilter(a, b, wavedata)
    return output


if __name__ == "__main__":
    
    # ファイルパス
    fname = "./static/sample.wav"
    wr = wave.open(fname, mode='rb')

    # 波形データwavedata取得
    wr.rewind() # ポインタを先頭に戻す
    buf = wr.readframes(-1)   # バイナリー形式で読み込まれる -> 後で10進数に直す
    # サンプリング周波数は、標本化定理より可聴域20kHzの2倍
    Fs = 44000
    # print(type(data))

    # 10進数化
    if wr.getsampwidth() == 2:
        data = np.frombuffer(buf, dtype='int16')
    elif wr.getsampwidth() == 4:
        data = np.frombuffer(buf, dtype='int32')

    # ステレオの場合はチャンネル1を取得
    if wr.getnchannels() == 2:
        wavedata = data[::2]
    else:
        wavedata = data
    
    # 音源の波形グラフを表示
    time = np.arange(0, len(wavedata)) / Fs
    plt.figure(figsize=(16, 5))
    plt.plot(time, wavedata)
    plt.title("Wave data of the original sound", fontsize=12)
    plt.xlabel("Time [sec]")
    plt.ylabel("Amplitude")
    plt.xlim(0, 5)
    plt.show()

    # 短時間フーリエ変換
    # 窓関数はハニング窓、窓長は20msec、窓の重なりは10msec
    F, T, Adft = sg.stft(wavedata, fs=Fs, window="hann", nperseg=0.02*Fs, noverlap=0.01*Fs)

    # 振幅値をdBに変換
    P = 10 * np.log(np.abs(Adft))

    # 短時間フーリエ変換のスペクトログラムを表示
    plt.figure(figsize=(16, 5))
    plt.title("Spectrogram of the original sound", fontsize=12)
    plt.xlabel("Time [sec]")
    plt.ylabel("Frequency [kHz]")
    plt.xlim(0, 5)
    plt.pcolormesh(T, F/1000, P, cmap="rainbow")
    plt.colorbar(orientation="horizontal").set_label("Amplitude [dB]")
    plt.show()

    # 加工前の音を再生
    playsound.playsound(fname)

    # 3点平均システムをかけたサウンドを生成
    three_point_average_wavedata = n_point_average_system(wavedata, Fs, 3)

    # 加工後の音の波形グラフを表示
    plt.figure(figsize=(16, 5))
    plt.plot(time, three_point_average_wavedata)
    plt.title("Wave data of the three point average sound", fontsize=12)
    plt.xlabel("Time [sec]")
    plt.ylabel("Amplitude")
    plt.xlim(0, 5)
    plt.show()

    # 短時間フーリエ変換
    # 窓関数はハニング窓、窓長は20msec、窓の重なりは10msec
    F2, T2, Adft2 = sg.stft(three_point_average_wavedata, fs=Fs, window="hann", nperseg=0.02*Fs, noverlap=0.01*Fs)

    # 振幅値をdBに変換
    P2 = 10 * np.log(np.abs(Adft2))

    # 短時間フーリエ変換のスペクトログラムを表示
    plt.figure(figsize=(16, 5))
    plt.title("Spectrogram of the three point average sound", fontsize=12)
    plt.xlabel("Time [sec]")
    plt.ylabel("Frequency [kHz]")
    plt.xlim(0, 5)
    plt.pcolormesh(T2, F2/1000, P2, cmap="rainbow")
    plt.colorbar(orientation="horizontal").set_label("Amplitude [dB]")
    plt.show()

    # 加工後の音を書き出し
    # write('three_point_aberage.wav', Fs, three_point_average_wavedata)

    # 加工後の音を再生
    playsound.playsound('./three_point_aberage.wav')
