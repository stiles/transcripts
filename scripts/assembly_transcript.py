import requests
import time
import os
import assemblyai as aai

# Your AssemblyAI API key
api_key = os.environ.get('ASSEMBLY_AI_KEY')
aai.settings.api_key = api_key

# Local file path to the audio you want to transcribe
local_file_path = "../audio/raw/joe-rogan-experience-2219-donald-trump.mp3"

# Initialize the transcriber with configuration for speaker labels
config = aai.TranscriptionConfig(speaker_labels=True, punctuate=True)
transcriber = aai.Transcriber()

# Define custom names for speakers based on your knowledge (manually set these)
speaker_mapping = {
    "Speaker A": "Joe Rogan",
    "Speaker B": "Donald Trump"
}

# Upload the local audio file to AssemblyAI using REST API
def upload_local_file(file_path):
    print("Uploading local audio file...")
    headers = {
        'authorization': api_key,
    }
    with open(file_path, 'rb') as f:
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, files={'file': f})
        if response.status_code == 200:
            print("Upload successful!")
            return response.json()['upload_url']
        else:
            print(f"Upload failed with status code {response.status_code}: {response.text}")
            return None

# Function to transcribe the audio and print out speaker-labeled segments
def transcribe_with_speaker_labels(file_path):
    # Upload the file and get the URL
    audio_url = upload_local_file(file_path)
    if not audio_url:
        print("Failed to upload audio. Exiting...")
        return
    
    print(f"Audio uploaded: {audio_url}")

    # Start transcription
    print("Starting transcription...")
    transcript = transcriber.transcribe(audio_url, config=config)

    # Display the transcription with custom speaker labels
    print("\nTranscription with Speaker Labels:")
    for utterance in transcript.utterances:
        # Replace default speaker labels with custom names
        custom_speaker = speaker_mapping.get(f"Speaker {utterance.speaker}", f"Speaker {utterance.speaker}")
        print(f"{custom_speaker}: {utterance.text}")

    # Optionally, save the transcript to a file
    output_file_path = "../transcripts/assembly/processed/assemblyai_speaker_transcript.txt"
    with open(output_file_path, "w") as f:
        for utterance in transcript.utterances:
            custom_speaker = speaker_mapping.get(f"Speaker {utterance.speaker}", f"Speaker {utterance.speaker}")
            f.write(f"{custom_speaker}: {utterance.text}\n")

    print(f"\nTranscription saved to '{output_file_path}'.")

# Run the transcription process
transcribe_with_speaker_labels(local_file_path)