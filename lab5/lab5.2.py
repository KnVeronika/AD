import numpy as np
from bokeh.layouts import column, row
from bokeh.models import Button, Slider, CheckboxGroup, ColumnDataSource
from bokeh.plotting import curdoc, figure

class NoiseGenerator:
    def __init__(self):
        self.previous_noise = None
        self.previous_noise_mean = None
        self.previous_noise_covariance = None
    
    def generate_noise(self, t, noise_mean, noise_covariance):
        # Генерація нового шуму, якщо параметри змінилися
        if self.previous_noise_mean != noise_mean or self.previous_noise_covariance != noise_covariance:
            self.previous_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
            self.previous_noise_mean = noise_mean
            self.previous_noise_covariance = noise_covariance
        return self.previous_noise

def median_filter(data, window_size):
    filtered_data = np.zeros_like(data)
    half_window = window_size // 2
    
    # Поелементна фільтрація
    for i in range(len(data)):
        start_index = max(0, i - half_window)
        end_index = min(len(data), i + half_window + 1)
        window = data[start_index:end_index]
        filtered_data[i] = np.median(window)
    
    return filtered_data

# Генерація часової осі
t = np.linspace(0, 10, 1000)

# Початкові параметри
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_window_size = 3

# Створення джерела даних для графіків
source = ColumnDataSource(data=dict(x=t, y=np.zeros_like(t), y_filtered=np.zeros_like(t)))

# Створення графічних об'єктів
plot = figure(title="Початкова гармоніка", y_range=(-5, 5))
line = plot.line('x', 'y', source=source, line_width=2)
plot.xaxis.axis_label = "Час"
plot.yaxis.axis_label = "Значення"

filtered_plot = figure(title="Фільтрована гармоніка", y_range=(-5, 5))
filtered_line = filtered_plot.line('x', 'y_filtered', source=source, line_width=2)
filtered_plot.xaxis.axis_label = "Час"
filtered_plot.yaxis.axis_label = "Значення"

noise_generator = NoiseGenerator()

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    noise = noise_generator.generate_noise(t, noise_mean, noise_covariance) if show_noise else np.zeros_like(t)
    y = amplitude * np.sin(2 * np.pi * frequency * t + phase) + noise
    return y

def update(attrname, old, new):
    amplitude = amplitude_slider.value
    frequency = frequency_slider.value
    phase = phase_slider.value
    noise_mean = noise_mean_slider.value
    noise_covariance = noise_covariance_slider.value
    show_noise = noise_checkbox.active
    
    source.data['y'] = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
    
    # Застосування медіанного фільтру, якщо вибрано відповідний чекбокс
    if filter_checkbox.active:
        window_size = window_size_slider.value
        source.data['y_filtered'] = median_filter(source.data['y'], window_size)
    else:
        source.data['y_filtered'] = np.zeros_like(t)

amplitude_slider = Slider(start=0.1, end=10.0, value=initial_amplitude, step=0.1, title="Амплітуда гармоніки")
frequency_slider = Slider(start=0.1, end=10.0, value=initial_frequency, step=0.1, title="Частота гармоніки")
phase_slider = Slider(start=0, end=2*np.pi, value=initial_phase, step=0.1, title="Фазовий зсув гармоніки")
noise_mean_slider = Slider(start=-1.0, end=1.0, value=initial_noise_mean, step=0.1, title="Амплітуда шуму")
noise_covariance_slider = Slider(start=0.01, end=1.0, value=initial_noise_covariance, step=0.01, title="Дисперсія шуму")
noise_checkbox = CheckboxGroup(labels=["Показати шум"], active=[0])
window_size_slider = Slider(start=3, end=30, value=initial_window_size, step=2, title="Розмір вікна медіанного фільтру")
filter_checkbox = CheckboxGroup(labels=["Застосувати фільтр"], active=[])

def reset():
    amplitude_slider.value = initial_amplitude
    frequency_slider.value = initial_frequency
    phase_slider.value = initial_phase
    noise_mean_slider.value = initial_noise_mean
    noise_covariance_slider.value = initial_noise_covariance
    noise_checkbox.active = [0]
    window_size_slider.value = initial_window_size
    filter_checkbox.active = []
    update(None, None, None)

reset_button = Button(label="Скинути", button_type="warning")
reset_button.on_click(reset)

for slider in [amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider]:
    slider.on_change('value', update)

noise_checkbox.on_change('active', update)
window_size_slider.on_change('value', update)
filter_checkbox.on_change('active', update)

controls = column([amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider,
                   noise_checkbox, window_size_slider, filter_checkbox, reset_button], width=200)
layout = row(column(plot, controls), filtered_plot)

curdoc().add_root(layout)
