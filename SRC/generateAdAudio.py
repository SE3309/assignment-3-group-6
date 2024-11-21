from pydub.generators import Sine
import random
import os

# Directory to save the generated audio files
# The './' refers to the current directory where the Python script resides
output_dir = "./audio"
os.makedirs(output_dir, exist_ok=True)

# Generate 200 audio files
num_files = 200
for i in range(1, num_files + 1):
    # Duration in milliseconds (5-10 seconds)
    duration = random.randint(5000, 10000)
    # Random frequency between 200Hz and 1000Hz
    frequency = random.randint(200, 1000)

    # Generate sine wave audio
    sine_wave = Sine(frequency).to_audio_segment(duration=duration)

    # Save the audio file as MP3
    file_path = os.path.join(output_dir, f"ad_{i}.mp3")
    sine_wave.export(file_path, format="mp3")
    print(f"Generated: {file_path}")

print(f"{num_files} audio files generated in the '{output_dir}' directory.")