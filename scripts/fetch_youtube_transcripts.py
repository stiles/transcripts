import os
import json
import pandas as pd

# transcript pulled from this url: https://www.youtube.com/api/timedtext?v=hBMoPUAeLnY&ei=8-IeZ54S7JCx8g_N27mxDw&caps=asr&opi=112496729&exp=xbt&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1730102627&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cexp%2Cxoaf&signature=E33305ABF9E87255928BC2B841A752E376102DEF.6983F94150F9998F690204C0F3DB676F463A111E&key=yt8&kind=asr&lang=en&fmt=json3&xorb=2&xobt=3&xovt=3&cbrand=apple&cbr=Chrome&cbrver=130.0.0.0&c=WEB&cver=2.20241025.01.00&cplayer=UNIPLAYER&cos=Macintosh&cosver=10_15_7&cplatform=DESKTOP

# Directory paths
youtube_dir = 'youtube_transcripts/raw/'
processed_dir = 'youtube_transcripts/processed/'

# Ensure the processed directory exists
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

# Function to convert timedtext JSON into a transcript
def convert_timedtext_to_transcript(timedtext_data):
    events = timedtext_data.get('events', [])
    transcript_lines = []
    
    for event in events:
        # Extract the segments if available
        segments = event.get('segs', [])
        if segments:
            for segment in segments:
                text = segment.get('utf8', '').strip()
                if text and text != "\n":
                    transcript_lines.append(text)
    
    # Join the lines into a single coherent transcript
    return ' '.join(transcript_lines)

# Process YouTube timed-text transcripts, including from .txt files
def process_youtube_timedtext():
    processed_transcripts = []
    
    # Iterate through the files in youtube_transcripts directory
    for filename in os.listdir(youtube_dir):
        if filename.endswith('.json') or filename.endswith('.txt'):
            input_path = os.path.join(youtube_dir, filename)

            # Load the YouTube JSON
            try:
                with open(input_path, 'r') as f:
                    timedtext_data = json.load(f)
            except json.JSONDecodeError:
                print(f"Failed to parse {filename}. Skipping.")
                continue

            # Convert to a single transcript string
            transcript = convert_timedtext_to_transcript(timedtext_data)

            if not transcript:
                print(f"No transcript data found for {filename}.")
            else:
                # Append transcript data
                processed_transcripts.append({
                    'filename': filename.replace('.json', '').replace('.txt', ''),
                    'transcript': transcript
                })

                # Save the processed transcript to a new file
                output_path = os.path.join(processed_dir, f'{filename.replace(".json", "").replace(".txt", "")}_transcript.json')
                with open(output_path, 'w') as f_out:
                    json.dump({
                        'filename': filename.replace('.json', '').replace('.txt', ''),
                        'transcript': transcript
                    }, f_out, indent=4)

    return pd.DataFrame(processed_transcripts)

# Process YouTube timed-text transcripts
youtube_df = process_youtube_timedtext()

# Save combined YouTube transcripts to JSON and CSV if data is present
if not youtube_df.empty:
    youtube_df.to_csv(f'{processed_dir}processed_transcripts.csv', index=False)
    youtube_df.to_json(f'{processed_dir}processed_transcripts.json', indent=4, orient='records')
    print("Processed YouTube transcripts successfully!")
else:
    print("No transcripts were processed. Please check the input files.")
