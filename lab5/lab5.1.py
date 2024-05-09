import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# Змінна для зберігання попередніх значень шуму
previous_noise = None

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    global previous_noise
    y = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        if previous_noise is None:
            previous_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
        y += previous_noise
    return y

def butterworth_filter(data, cutoff_freq, fs, order=5):
    nyquist_freq = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y_filtered = filtfilt(b, a, data)
    return y_filtered

# Початкові параметри
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_show_noise = True
initial_show_filtered = True
initial_cutoff_frequency = 2.0

# Генерація часової осі
t = np.linspace(0, 10, 1000)
fs = 1 / (t[1] - t[0])  # частота дискретизації

# Створення графічного вікна
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.15, bottom=0.6)

# Створення графіку
line, = ax.plot(t, harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase,
                                       initial_noise_mean, initial_noise_covariance, initial_show_noise), label='Початкова гармоніка')
line_filtered, = ax.plot(t, harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase,
                                                 initial_noise_mean, initial_noise_covariance, initial_show_noise), label='Відфільтрована гармоніка')
ax.set_xlabel('Час')
ax.set_ylabel('Значення')
ax.legend()

# Змінні для зберігання попередніх значень шуму
previous_noise_mean = initial_noise_mean
previous_noise_covariance = initial_noise_covariance

ax_amplitude = plt.axes([0.2, 0.3, 0.65, 0.03])
ax_frequency = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_phase = plt.axes([0.2, 0.2, 0.65, 0.03])
ax_noise_mean = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_noise_covariance = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_cutoff_frequency = plt.axes([0.2, 0.05, 0.65, 0.03])

s_amplitude = Slider(ax_amplitude, 'Амплітуда гармоніки', 0.1, 10.0, valinit=initial_amplitude)
s_frequency = Slider(ax_frequency, 'Частота гармоніки', 0.1, 10.0, valinit=initial_frequency)
s_phase = Slider(ax_phase, 'Фазовий зсув гармоніки', 0.0, 2*np.pi, valinit=initial_phase)
s_noise_mean = Slider(ax_noise_mean, 'Амплітуда шуму', -1.0, 1.0, valinit=initial_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Дисперсія шуму', 0.01, 1.0, valinit=initial_noise_covariance)
s_cutoff_frequency = Slider(ax_cutoff_frequency, 'Частота зрізу фільтру', 0.1, 5.0, valinit=initial_cutoff_frequency)

# Створення чекбоксу для показу відфільтрованої гармоніки
axcolor = 'lightgoldenrodyellow'
rax_show_filtered = plt.axes([0.05, 0.4, 0.15, 0.06], facecolor=axcolor)
check_show_filtered = CheckButtons(rax_show_filtered, ['Відфільтрувати'], [initial_show_filtered])

# Функція для оновлення видимості відфільтрованої гармоніки
def update_filtered_visibility(label):
    line_filtered.set_visible(check_show_filtered.get_status()[0])
    fig.canvas.draw_idle()
check_show_filtered.on_clicked(update_filtered_visibility)

# Функція оновлення графіку
def update(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    cutoff_frequency = s_cutoff_frequency.val
    show_noise = check_show_noise.get_status()[0]
    show_filtered = check_show_filtered.get_status()[0]

    # Оновлення початкової гармоніки
    line.set_ydata(harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise))

    # Фільтрування гармоніки та оновлення відфільтрованої гармоніки
    if show_filtered:
        filtered_data = butterworth_filter(line.get_ydata(), cutoff_frequency, fs)
        line_filtered.set_ydata(filtered_data)
    else:
        line_filtered.set_ydata(np.zeros_like(t))

    # Оновлення попередніх значень шуму
    global previous_noise, previous_noise_mean, previous_noise_covariance
    if previous_noise is not None and (previous_noise_mean != noise_mean or previous_noise_covariance != noise_covariance):
        previous_noise = None
    previous_noise_mean = noise_mean
    previous_noise_covariance = noise_covariance

    fig.canvas.draw_idle()

check_show_filtered.on_clicked(update_filtered_visibility)

s_amplitude.on_changed(update)
s_frequency.on_changed(update)
s_phase.on_changed(update)
s_noise_mean.on_changed(update)
s_noise_covariance.on_changed(update)
s_cutoff_frequency.on_changed(update)

# Створення чекбоксу для відображення шуму
rax = plt.axes([0.05, 0.35, 0.15, 0.06], facecolor=axcolor)
check_show_noise = CheckButtons(rax, ['Показати шум'], [initial_show_noise])
check_show_noise.on_clicked(update)

# Створення кнопки Reset
resetax = plt.axes([0.8, 0.35, 0.15, 0.05])
button_reset = Button(resetax, 'Reset', color=axcolor)

# Функція для скидання параметрів до початкових значень
def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_frequency.reset()
    
    # Скидання попередніх значень шуму до початкових
    global previous_noise, previous_noise_mean, previous_noise_covariance
    previous_noise = None
    previous_noise_mean = initial_noise_mean
    previous_noise_covariance = initial_noise_covariance
    
    # Встановлення чекбоксів на початкові значення
    check_show_noise.set_active(initial_show_noise)
    check_show_filtered.set_active(initial_show_filtered)
    
    # Оновлення графіку з врахуванням початкових параметрів
    update(None)

button_reset.on_clicked(reset)


plt.show()
