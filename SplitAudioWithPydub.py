# 1) Install pydub: pip install pydub
# 2) Install ffmpeg dependency: https://www.youtube.com/watch?v=IECI72XEox0
import os
# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence


def main():
    # Get current directory.
    pwd = os.getcwd()
    print("Current directory: " + pwd)
    # Get list of all files in current directory.
    files = os.listdir(pwd)
    # Filter out all files that are not .mp3 files.
    mp3files = [f for f in files if f[-4:] == ".mp3"]
    # Print list of all .mp3 files in current directory.
    print("List of all .mp3 files in current directory:")
    while True:
        for i in range(len(mp3files)):
            print(str(i) + ": " + mp3files[i])
        # Get user input.
        try:
            choice = int(input("Enter number of file to be processed: "))
            if choice >= 0 and choice < len(mp3files):
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid choice. Try again.")

    # Assign the chosen file to a variable.
    filename = mp3files[choice]
    print("You chose: " + filename)
    # Set file path.
    filepath = pwd + "\\" + filename
    print("Audio file to split on: " + filepath)
    out_directory = pwd + "\\pydub_output"
    print("Will provide output to: " + out_directory)

    # check if output directory exists
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)

    # obtain how long the audio should be silent for splitting to occur
    silence_threshold = int(input("\nEnter the silence threshold lenght in milliseconds: (default 150)"))
    print("Silence threshold length: " + str(silence_threshold))

    # Obtain how silent the audio should be for splitting to occur
    silence_thresh_db = int(input("\nEnter the silence threshold in dBFS, \n  " +
                                  "converted to negative: higher is more silent: (default 30) "))
    print("Silence threshold in dBFS: " + str(silence_thresh_db))

    # Provide a name for the output files.
    output_name = input("\nEnter the output file name: (e.g. my_audio_file) ")
    print("Output file name: " + output_name)

    # Provide how long the slince before and after the chunk should be for padding purposes.
    silence_padding = int(input("\nEnter the silence padding length in milliseconds: (default 50)"))

    audio = AudioSegment.from_file(filepath)

    chunks = split_on_silence(
        # Use the loaded audio.
        audio,
        # Specify that a silent chunk must be at least silence_threshold ms long.
        min_silence_len=silence_threshold,
        # Consider a chunk silent if it's quieter than x dBFS.
        silence_thresh=-silence_thresh_db,
        keep_silence=True
    )

    print ("\nNumber of chunks: " + str(len(chunks)) + "\n")

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        silence_chunk = AudioSegment.silent(duration=silence_padding)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        # Export the audio chunk with new bitrate.
        print("Exporting " + filename + str(i) + ".mp3")
        normalized_chunk.export(
            out_directory + "//" + filename + str(i) + ".mp3",
            bitrate="192k",
            format="mp3"
        )


# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


if __name__ == '__main__':
    main()