# **Reddit Thread to Video Automation**

This script automates the process of creating a video from a Reddit thread. It fetches the thread's title and top comments, generates text-to-speech (TTS) audio and images for the content, and combines them into a video with synchronized audio and visuals.

## **Features**

- Fetches a Reddit thread (title and top comments) based on a provided URL.
- Supports configurable number of top comments.
- Generates TTS audio for the thread title and comments using Google Text-to-Speech.
- Creates Reddit-styled images for the title and comments.
- Combines input video, generated audio, and images into a final video output.
- Supports dynamic configurations via command-line arguments.

## **Requirements**

- Python 3.8 or later.
- Required Python libraries:
  - `moviepy`
  - `argparse`
  - `google-cloud-texttospeech` (for Google TTS)
  - `Pillow`
  - `requests` (for fetching Reddit threads)
- [FFmpeg](https://ffmpeg.org/) installed and added to system PATH.

## **Setup Instructions**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/reddit-video-automation.git
   cd reddit-video-automation
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud Text-to-Speech:**

   - Create a project on [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Text-to-Speech API** for the project.
   - Generate and download a service account key (JSON file).
   - Set the environment variable to use the service account key:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account.json"
     ```

4. **Ensure FFmpeg is installed:**

   - Install FFmpeg and add it to your system PATH.
   - Verify installation:
     ```bash
     ffmpeg -version
     ```

5. **Prepare directories:**
   Ensure the following directories exist:
   - `input_videos/` (for input video files)
   - `output_audio/` (for generated audio files)
   - `output_images/` (for generated image files)
   - `final_output/` (for the final video output)

## **Usage**

### **Command-Line Arguments**

| Argument               | Default Value                  | Description                                            |
| ---------------------- | ------------------------------ | ------------------------------------------------------ |
| `--redditURL`          | _Required_                     | The URL of the Reddit thread to process.               |
| `--topComments`        | `5`                            | Number of top comments to include in the video.        |
| `--language`           | `en-US`                        | Language code for TTS (e.g., `en-US`, `pl-PL`).        |
| `--voice`              | `en-US-Casual-K`               | Name of the TTS voice to use.                          |
| `--gender`             | `MALE`                         | Gender of the TTS voice (`MALE`, `FEMALE`, `NEUTRAL`). |
| `--rate`               | `1.0`                          | Speaking rate for TTS.                                 |
| `--pitch`              | `0.2`                          | Pitch for TTS.                                         |
| `--inputVideo`         | `./input_videos/mcparkour.mp4` | Path to the input video file.                          |
| `--outputVideo`        | `./final_output/output.mp4`    | Path to the output video file.                         |
| `--outputAudioFolder`  | `output_audio`                 | Folder to save generated audio files.                  |
| `--outputImagesFolder` | `output_images`                | Folder to save generated image files.                  |
| `--debug`              | _Disabled_                     | Enable debug mode for detailed logs.                   |

### **Example Usage**

1. **Basic Example:**

   ```bash
   python main.py --redditURL "https://www.reddit.com/r/AskReddit/comments/xyz123"
   ```

2. **With Custom Number of Comments:**

   ```bash
   python main.py --redditURL "https://www.reddit.com/r/AskReddit/comments/xyz123" --topComments 10
   ```

3. **Custom TTS Configuration:**

   ```bash
   python main.py --redditURL "https://www.reddit.com/r/AskReddit/comments/xyz123" --language "pl-PL" --voice "pl-PL-Wavenet-A" --rate 0.8
   ```

4. **Debug Mode:**
   ```bash
   python main.py --redditURL "https://www.reddit.com/r/AskReddit/comments/xyz123" --debug
   ```

## **Folder Structure**

```
project/
│
├── input_videos/         # Input videos for the project
├── output_audio/         # Generated audio files
├── output_images/        # Generated Reddit-style images
├── final_output/         # Final video output
├── fonts/                # Custom fonts for images
├── main.py               # Main script to run the automation
├── RedditAPIService.py   # Service to fetch Reddit threads and comments
├── TTSService.py         # Google TTS integration
├── ImageService.py       # Reddit-style image generation
├── VideoEditService.py   # Video editing and composition
└── README.md             # This file
```

## **How It Works**

1. **Fetch Reddit Thread:**

   - The script uses the Reddit thread URL to fetch the thread title and top comments.

2. **Generate Audio:**

   - The title and comments are converted to speech using Google TTS.

3. **Generate Images:**

   - Reddit-styled images are created for the title and each comment.

4. **Combine Video, Audio, and Images:**

   - The input video is sliced to match the total duration of the audio.
   - Images and audio are synchronized and overlaid onto the video.

5. **Export Final Video:**
   - The final video is saved to the specified output directory.

## **Debugging**

- Use `--debug` to enable detailed logging during the process.
- Check the `output_audio/` and `output_images/` folders for intermediate files.
- Ensure FFmpeg and Google TTS are properly configured if you encounter issues.

## **To Do**

- Add support for multiple Reddit threads in one session.
- Include error handling for network and API issues.
- Add more styling options for generated images.

## **Contributing**

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.

## **License**

This project is open-source and available under the MIT License.
