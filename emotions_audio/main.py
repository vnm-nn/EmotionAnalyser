# measure_wav.py
# Paul Boersma 2017-01-03
#
# A sample script that uses the Vokaturi library to extract the emotions from
# a wav file on disk. The file can contain a mono or stereo recording.
#
# Call syntax:
#   python3 measure_wav.py path_to_sound_file.wav

import sys
import scipy.io.wavfile

sys.path.append("../api")
import Vokaturi

sys.path.append(r"C:\Program Files\IronPython 2.7\Lib")

print("Загрузка библиотеки...")
Vokaturi.load("Vokaturi_win64.dll")

print("Считывание входного аудиофайла...")
file_name = sys.argv[1]
print("Имя файла: " + file_name)
(sample_rate, samples) = scipy.io.wavfile.read(file_name)
print("Частота дискретизации %.3f Герц" % sample_rate)

print("Создаем массив и загружаем в него образцы из библиотеки...")
buffer_length = len(samples)
print("%d образцов, %d каналов" % (buffer_length, samples.ndim))
c_buffer = Vokaturi.SampleArrayC(buffer_length)
if samples.ndim == 1:
    c_buffer[:] = samples[:] / 32768.0  # mono
else:
    c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0  # stereo

voice = Vokaturi.Voice (sample_rate, buffer_length)
voice.fill(buffer_length, c_buffer)

print("Распознавание эмоций...")
quality = Vokaturi.Quality()
emotionProbabilities = Vokaturi.EmotionProbabilities()
voice.extract(quality, emotionProbabilities)

if quality.valid:
    print("Нейтральная: %.3f" % emotionProbabilities.neutrality)
    print("Счастье: %.3f" % emotionProbabilities.happiness)
    print("Грусть: %.3f" % emotionProbabilities.sadness)
    print("Злость: %.3f" % emotionProbabilities.anger)
    print("Страх: %.3f" % emotionProbabilities.fear)
    with open("C:\\Users\\klimo\\Downloads\\emotions_audio\\emotions_audio\\result.txt", 'w+') as result_file:
        print('Записываем результаты в файл...')
        result_file.write(str(emotionProbabilities.neutrality) + '\n' +
                          str(emotionProbabilities.happiness)  + '\n' +
                          str(emotionProbabilities.sadness) + '\n' +
                          str(emotionProbabilities.anger) + '\n' +
                          str(emotionProbabilities.fear))

voice.destroy()