import numpy as np
import pandas as pd
from signal_class import Signal
import plotly_express as px



# ------------------------ Variables --------------------------- #

display_range=1000
signal_data = pd.read_csv("ecg_data.csv")[:display_range]
signal_time = signal_data["Time"]

# signal_amplitude = signal_data["Amplitude"]
# maximum_frequency = np.fft.fft(signal_data).max()
# sampling_frequency = 2 * maximum_frequency

added_signals_list = []


# ------------------------ Modifying Functions --------------------------- #

def generateNoisySignal(SNR):
    temp_noisy_data = signal_data.copy()
    SNR_db = 10 * np.log10(SNR)
    power = temp_noisy_data["Amplitude"] ** 2
    signal_average_power= np.mean(power)
    signal_average_power_db = 10 * np.log10(signal_average_power)
    noise_db = signal_average_power_db - SNR_db
    noise_watts = 10 ** (noise_db/10)

    noise = np.random.normal(0,np.sqrt(noise_watts), len(temp_noisy_data))
    temp_noisy_data["Amplitude"] += noise
    return temp_noisy_data

# ------------------------------------------------------------------------ #

# def generateSineWave(amplitude, frequency, phase):
#     phase_rad= phase*np.pi/180
#     time = np.arange(0, 10, 1/100)
#     sineWave = amplitude * np.sin(2 * np.pi * frequency * time + phase_rad)
#     sine_wave_data = pd.DataFrame(sineWave, time)
#     return sine_wave_data

# ------------------------------------------------------------------------ #

def renderAddedSignals(noise_flag, SNR = 100):
    clear_added_signal = signal_data.copy()
    noisy_added_signal = generateNoisySignal(SNR = SNR)
    for signal in added_signals_list:
        clear_added_signal["Amplitude"] += (signal.amplitude * np.sin(2 * np.pi * signal.frequency * signal_time + signal.phase))
        noisy_added_signal["Amplitude"] += (signal.amplitude * np.sin(2 * np.pi * signal.frequency * signal_time + signal.phase))
    if noise_flag:
        return noisy_added_signal
    else:
        return clear_added_signal

# ------------------------------------------------------------------------ #

def generateSampledSignal(factor, f_max):
    time = np.arange(0,0.5,1/(factor*f_max))
    # Find the period    
    T = signal_data["Time"][1] - signal_data["Time"][0]

    # sinc interpolation
    sincM = np.tile(time, (len(signal_data["Time"]), 1)) - np.tile(signal_data["Time"][:,np.newaxis], (1, len(time)))
    ynew = np.dot(signal_data["Amplitude"], np.sinc(sincM/T))

    #Plot
    df=pd.DataFrame(ynew,time)



    fig = px.line(df, markers=True, labels={
                     "index": "Time (s)",
                     "value": "Amplitude (mv)"
                 },
                title="Resulted Signal")
    
    fig.update_traces(marker=dict(color="crimson"))

  
    
    return  fig,df

# ------------------------------------------------------------------------ #

def addSignal(amplitude, frequency, phase):
    added_signals_list.append(Signal(amplitude = amplitude, frequency = frequency, phase = phase*np.pi/180))

# ------------------------------------------------------------------------ #

def removeSignal(amplitude, frequency, phase):
    
    for added_signal in added_signals_list:
        if added_signal.amplitude == amplitude and added_signal.frequency == frequency and added_signal.phase == phase:
            added_signals_list.remove(added_signal)
            return

# ---------------------------- Getter functions -------------------------- #

def getClearSignalData():
    return signal_data

# ------------------------------------------------------------------------ #

def getAddedSignalsList():
    return added_signals_list