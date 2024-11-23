import argparse
from RedditAPIService import RedditAPIService
from TTSService import TTSGenerator
from ImageService import ImageService
from VideoEditService import VideoEditService
import os
import html

# Clearing files in specified folders
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f"Could not delete {file_path}. Reason: {e}")

# Display all comments with indices
def display_all_comments(comments):
    """
    Displays all available comments with their indices.
    """
    print("\nAvailable Comments:")
    for i, comment in enumerate(comments):
        print(f"[{i}] {comment['body']} (Author: {comment['author']})")

# Select comments based on user input
def choose_comments_by_input(all_comments):
    """
    Allows the user to manually select comments by entering indices in the desired order.
    """
    while True:
        try:
            print("\nEnter the indices of the comments you want to include, separated by commas (in desired order):")
            user_input = input("Selected comments (e.g., 8,4,2): ")
            selected_indices = [int(idx.strip()) for idx in user_input.split(",") if idx.strip().isdigit()]
            
            # Validate indices
            invalid_indices = [idx for idx in selected_indices if idx < 0 or idx >= len(all_comments)]
            if invalid_indices:
                print(f"Invalid indices: {invalid_indices}. Please try again.")
                continue
            
            # Select comments in the provided order
            selected_comments = [all_comments[idx] for idx in selected_indices]
            return selected_comments
        except ValueError:
            print("Invalid input. Please enter valid indices separated by commas.")

# Argument parser
parser = argparse.ArgumentParser(description="Automate video creation from Reddit threads.")
parser.add_argument("--redditURL", type=str, required=True, help="URL of the Reddit thread to process.")
parser.add_argument("--topComments", type=int, default=5, help="Number of top comments to process.")
parser.add_argument("--selectComments", action="store_true", help="Enable manual selection of comments.")
parser.add_argument("--language", type=str, default="pl-PL", help="Language code for TTS.")
parser.add_argument("--voice", type=str, default="pl-PL-Standard-G", help="TTS voice name.")
parser.add_argument("--gender", type=str, default="MALE", choices=["MALE", "FEMALE", "NEUTRAL"], help="Gender of the TTS voice.")
parser.add_argument("--rate", type=float, default=1.2, help="Speaking rate for TTS.")
parser.add_argument("--pitch", type=float, default=0.2, help="Pitch for TTS.")
parser.add_argument("--inputVideo", type=str, default="./input_videos/mcparkour6min.mp4", help="Input video path.")
parser.add_argument("--outputVideo", type=str, default="./final_output/output.mp4", help="Output video path.")
parser.add_argument("--outputAudioFolder", type=str, default="output_audio", help="Folder for audio files.")
parser.add_argument("--outputImagesFolder", type=str, default="output_images", help="Folder for image files.")
parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
args = parser.parse_args()

# Clear folders
clear_folder(args.outputAudioFolder)
clear_folder(args.outputImagesFolder)

# Fetch the Reddit thread
thread = RedditAPIService(args.redditURL)
thread.fetch_thread()
info = thread.get_thread_info()

# Fetch all comments
all_comments = thread.get_all_comments()

# If --selectComments is enabled, allow manual selection
if args.selectComments:
    display_all_comments(all_comments)
    top_comments = choose_comments_by_input(all_comments)  # Comments are selected in the specified order
else:
    # Default to selecting top comments
    top_comments = thread.get_top_comments(n=args.topComments)

# Debugging output
if args.debug:
    print("\nSelected Comments:")
    for i, comment in enumerate(top_comments):
        print(f"{i}: {comment}")

# Process TTS and images
ttsClient = TTSGenerator(language_code=args.language, voice_name=args.voice, ssml_gender=args.gender, speaking_rate=args.rate, pitch=args.pitch)
imageService = ImageService()
titleImageService = ImageService(font_path='./fonts/reddit_sans/static/RedditSans-ExtraBold.ttf')

ttsClient.text_to_speech(html.unescape(info['title']), filename=os.path.join(args.outputAudioFolder, 'comment0.mp3'))
titleImageService.create_reddit_style_image(
    html.unescape(info['title']),
    output_path=os.path.join(args.outputImagesFolder, 'comment0.png'),
    subreddit=info['subreddit'],
    username=info['author']
)

for i, comment in enumerate(top_comments, start=1):
    ttsClient.text_to_speech(html.unescape(comment['body']), filename=os.path.join(args.outputAudioFolder, f"comment{i}.mp3"))
    imageService.create_reddit_style_image(
        html.unescape(comment['body']),
        output_path=os.path.join(args.outputImagesFolder, f"comment{i}.png"),
        subreddit=info['subreddit'],
        username=comment['author']
    )

# Create the video
videoService = VideoEditService(
    input_video_path=args.inputVideo,
    output_video_path=args.outputVideo,
    images_folder=args.outputImagesFolder,
    audio_folder=args.outputAudioFolder
)
videoService.edit_video()
