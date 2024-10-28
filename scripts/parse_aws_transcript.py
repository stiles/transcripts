import json

# Replace with the path to your downloaded Amazon Transcribe JSON file
transcript_json_path = 'transcripts/aws/raw/rogan_trump_aws_transcript.json'

# Function to parse the Amazon Transcribe JSON and format the transcript
def parse_transcribe_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Extract the list of items (words) from the JSON
    items = data['results']['items']
    speaker_segments = data['results'].get('speaker_labels', {}).get('segments', [])
    
    # Prepare a list to store all words with their speaker info
    transcript_words = []
    
    # Create a dictionary to map each word's start time to its speaker
    speaker_map = {}
    for segment in speaker_segments:
        speaker_label = segment['speaker_label']
        for word_info in segment['items']:
            start_time = word_info.get('start_time')
            if start_time:
                speaker_map[start_time] = speaker_label

    # Iterate through the items and construct the transcript
    current_speaker = None
    current_text = []
    formatted_transcript = []

    for item in items:
        if item['type'] == 'pronunciation':
            start_time = item.get('start_time')
            word = item['alternatives'][0]['content']
            speaker = speaker_map.get(start_time, current_speaker)
            
            # Check if the speaker changes
            if speaker != current_speaker:
                if current_speaker is not None and current_text:
                    # Add the accumulated text for the previous speaker
                    formatted_transcript.append(f"{current_speaker}: {' '.join(current_text)}")
                
                # Reset for new speaker
                current_speaker = speaker
                current_text = [word]
            else:
                current_text.append(word)
        
        elif item['type'] == 'punctuation':
            if current_text:
                current_text[-1] += item['alternatives'][0]['content']

    # Add the last accumulated speaker's text
    if current_text:
        formatted_transcript.append(f"{current_speaker}: {' '.join(current_text)}")

    return "\n".join(formatted_transcript)

# Convert the transcript and print it out
formatted_transcript = parse_transcribe_json(transcript_json_path)
print(formatted_transcript)

# Optionally save the formatted transcript to a file
with open('transcripts/aws/processed/formatted_transcript.txt', 'w') as f:
    f.write(formatted_transcript)

print("Formatted transcript saved to formatted_transcript.txt")