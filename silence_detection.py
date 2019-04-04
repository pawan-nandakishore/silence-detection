import pydub as pdb 
from scipy.stats import norm 
import numpy as np 
import matplotlib.pyplot as plt 
import argparse



def get_wav(wav_file): 
    wave_file = pdb.AudioSegment.from_wav(wav_file)
    wav_file =wave_file.set_channels(1) # set stereo to mono 

    return wav_file 


def get_silent_regions(wav_file, min_silence_length= 500, silence_threshold= -35): 
    """ 
    Silent regions are in seconds 
    """
    return pdb.silence.detect_silence(wav_file,min_silence_len=min_silence_length,silence_thresh=silence_threshold)

def filter_wave(pdb_wav, freq, type= None): 
    if type_filter == "low": 
        return pdb_wav.low_pass_filter(freq)
    elif type_filter== "high":
        return pdb_wav.high_pass_filter(freq)
    elif type_filter == None :
        return pdb_wav 
    

def plot_silent_regions(wav_file, silent_regions, save_fig ="no"): 
    """
    Get silent regions from the function get_silent_regions
    Get wav_file from get_wav function  
    """
    np_wave = wav_file.get_array_of_samples()
    db_values = np.array(np_wave)
    normalized_db = db_values/np.max(db_values)
    audio_regions = normalized_db
    #1000 units is 1 sec 
    time_axis= np.arange(0,normalized_db.size)
    normalized_time = time_axis/(wav_file.frame_rate/1000)
    
    plt.rc("font", size = 25)
    fig, ax = plt.subplots(figsize=(20,8))
    for i in range(len(silent_regions)): 
        region = silent_regions[i]
        left_side= region[0]/1000
        right_side= region[1]/1000
        ax.axvspan(left_side,right_side, alpha=0.5, color='red')

    ax.plot(normalized_time/1000, normalized_db)
    plt.xlabel("time(s)")
    plt.ylabel("normalized amplitude")
    if save_fig== "yes": 
        plt.savefig("silent_regions_result.png", dpi = 100)
    plt.show()

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='put video name')
    parser.add_argument("video_name", type =str, help ="put video name " )
    parser.add_argument("-save", type= str, choices=["yes", "no"], help= "do you want to save the video")
    parser.add_argument("-silence_params", type =int, nargs = 2,  help= "shorter silence time and silence threshold")
    parser.add_argument("-filter", type = str, nargs = 2,  help= "chose high pass or low pass filter and add the frequncy range of filtering")

    
    args = parser.parse_args()
    type_filter, freq =args.filter
    
    waveFile = get_wav( args.video_name)

    if args.silence_params: 
        par1, par2 = args.silence_params
        silentRegions =get_silent_regions(waveFile,par1, par2 )
    else: 
        silentRegions =get_silent_regions(waveFile)
   
    
    filtered_waveFile = filter_wave(waveFile, float(freq), type_filter)
    plot_silent_regions(waveFile, silentRegions, save_fig = args.save)
