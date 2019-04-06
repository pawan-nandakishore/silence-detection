import os 
import pydub as pdb 
import argparse

def resize_audio(wave_file_loc,save_loc,  start_duration, end_duration):
    """
    Keep audio only till new_duration 
    Input: 
        wave_file_loc   : location of wave file
        save_loc        : where do you want to save the output 
        start_duration  : How long of the audio you want to keep (In seconds)
        end_duration    : End of the audio in seconds  
    """
    assert start_duration < end_duration


    wave_audio = pdb.AudioSegment.from_wav(wave_file_loc)
    wave_audio =wave_audio.set_channels(1) # set stereo to mono 
    start_duration =(start_duration) * 1000
    end_duration =(end_duration) * 1000
    
    assert end_duration > len(wave_audio)

    wave_audio = wave_audio[start_duration:end_duration]
    wave_audio.export(save_loc, format="wav")
    
    return wave_audio


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='put audio file name')
    parser.add_argument("audio_name", type =str, help ="put audio name " )
    parser.add_argument("save_name", type= str, help= "save audio track as.. ")
    parser.add_argument("start", type=float, help= "length of track you want to keep ")
    parser.add_argument("end", type=float, help= "length of track you want to keep ")
    args = parser.parse_args()

    _ = resize_audio(args.audio_name, args.save_name, args.start, args.end)
