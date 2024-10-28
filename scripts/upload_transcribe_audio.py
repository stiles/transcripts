import boto3
import time
import os

# AWS configurations
aws_region = 'us-west-1'
profile_name = 'haekeo'  # Your AWS profile name
bucket_name = 'stilesdata.com'  # Use the actual bucket name
audio_file_path = 'audio/raw/joe-rogan-experience-2219-donald-trump.mp3'

# Define the S3 key to include the "audio/" directory path within the bucket
s3_key = f'audio/{os.path.basename(audio_file_path)}'

# Initialize a boto3 session using the specified profile
session = boto3.Session(profile_name=profile_name, region_name=aws_region)

# Create S3 and Transcribe clients from the session
s3_client = session.client('s3')
transcribe_client = session.client('transcribe')

# Step 1: Upload the audio file to S3
def upload_audio_to_s3(file_path, bucket, key):
    try:
        s3_client.upload_file(file_path, bucket, key)
        print(f"Uploaded {file_path} to S3 bucket {bucket} as {key}.")
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {e}")

# Step 2: Start a transcription job
def start_transcription_job(job_name, s3_uri, language_code='en-US', speaker_labels=True):
    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='mp3',
            LanguageCode=language_code,
            Settings={
                'ShowSpeakerLabels': speaker_labels, 
                'MaxSpeakerLabels': 2,
                'ChannelIdentification': True  # Try enabling Channel Identification
            },
        )
        print(f"Started transcription job: {job_name}")
    except Exception as e:
        print(f"Failed to start transcription job: {e}")

# Step 3: Poll the transcription job status
def get_transcription_result(job_name):
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        
        if job_status in ['COMPLETED', 'FAILED']:
            break
        print(f"Job {job_name} is {job_status}. Waiting...")
        time.sleep(10)
    
    if job_status == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f"Transcription job completed. Transcript URI: {transcript_uri}")
        return transcript_uri
    else:
        print(f"Transcription job {job_name} failed.")
        return None

# Main function to orchestrate upload and transcription
def transcribe_audio(file_path, bucket, s3_key):
    # Upload audio file to S3
    upload_audio_to_s3(file_path, bucket, s3_key)
    
    # Generate S3 URI
    s3_uri = f's3://{bucket}/{s3_key}'
    
    # Create a unique transcription job name
    job_name = f"transcription-{int(time.time())}"
    
    # Start transcription job
    start_transcription_job(job_name, s3_uri)
    
    # Get the result of the transcription job
    transcript_url = get_transcription_result(job_name)
    
    if transcript_url:
        print("Transcription completed successfully!")
        print(f"Transcript can be accessed at: {transcript_url}")
    else:
        print("Transcription failed.")

# Run the transcription process
transcribe_audio(audio_file_path, bucket_name, s3_key)