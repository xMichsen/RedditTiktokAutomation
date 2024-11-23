import argparse
from RedditAPIService import RedditAPIService
from TTSService import TTSGenerator
from ImageService import ImageService
from VideoEditService import VideoEditService
import os
import html

def clear_folder(folder_path):
    """
    Clears all files in the specified folder.
    """
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Could not delete {file_path}. Reason: {e}")

# Argument parser setup
parser = argparse.ArgumentParser(description="Automate video creation from Reddit threads.")

parser.add_argument("--redditURL", type=str, required=True, help="URL of the Reddit thread to process.")
parser.add_argument("--topComments", type=int, default=5, help="Number of top comments to process.")
parser.add_argument("--language", type=str, default="pl-PL", help="Language code for TTS (e.g., en-US, pl-PL).")
parser.add_argument("--voice", type=str, default="pl-PL-Standard-G", help="Name of the TTS voice to use.")
parser.add_argument("--gender", type=str, default="MALE", choices=["MALE", "FEMALE", "NEUTRAL"], help="Gender of the TTS voice.")
parser.add_argument("--rate", type=float, default=1.2, help="Speaking rate for TTS.")
parser.add_argument("--pitch", type=float, default=0.2, help="Pitch for TTS.")
parser.add_argument("--inputVideo", type=str, default="./input_videos/mcparkour6min.mp4", help="Path to the input video file.")
parser.add_argument("--outputVideo", type=str, default="./final_output/output.mp4", help="Path to the output video file.")
parser.add_argument("--outputAudioFolder", type=str, default="output_audio", help="Folder to save generated audio files.")
parser.add_argument("--outputImagesFolder", type=str, default="output_images", help="Folder to save generated images.")
parser.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logs.")

args = parser.parse_args()

# Debug mode
if args.debug:
    print("Debug mode enabled.")
    print(f"Arguments received: {args}")

# Clear folders before processing
clear_folder(args.outputAudioFolder)
clear_folder(args.outputImagesFolder)

# Reddit thread processing
thread = RedditAPIService(args.redditURL)
thread.fetch_thread()
info = thread.get_thread_info()

# Fetch top comments based on the argument
top_comments = thread.get_top_comments(n=args.topComments)

# TTS and Image services initialization
ttsClient = TTSGenerator(language_code=args.language, voice_name=args.voice, ssml_gender=args.gender, speaking_rate=args.rate, pitch=args.pitch)
imageService = ImageService()
titleImageService = ImageService(font_path='./fonts/reddit_sans/static/RedditSans-ExtraBold.ttf')

# Video service initialization
videoService = VideoEditService(
    input_video_path=args.inputVideo,
    output_video_path=args.outputVideo,
    images_folder=args.outputImagesFolder,
    audio_folder=args.outputAudioFolder
)

# Generate TTS and image for the title
ttsClient.text_to_speech(html.unescape(info['title']), filename=os.path.join(args.outputAudioFolder, 'comment0.mp3'))
titleImageService.create_reddit_style_image(
    html.unescape(info['title']),
    output_path=os.path.join(args.outputImagesFolder, 'comment0.png'),
    subreddit=info['subreddit'],
    username=info['author']
)

# Process comments
for i, comment in enumerate(top_comments, start=1):
    ttsClient.text_to_speech(html.unescape(comment['body']), filename=os.path.join(args.outputAudioFolder, f"comment{i}.mp3"))
    imageService.create_reddit_style_image(
        html.unescape(comment['body']),
        output_path=os.path.join(args.outputImagesFolder, f"comment{i}.png"),
        subreddit=info['subreddit'],
        username=comment['author']
    )
    if args.debug:
        print(f"Processed comment {i}: {comment}")

# Create the final video
videoService.edit_video()
