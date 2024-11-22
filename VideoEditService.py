from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import os
import random

class VideoEditService:
    def __init__(self, input_video_path, output_video_path, images_folder='output_images', audio_folder='output_audio'):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.images_folder = images_folder
        self.audio_folder = audio_folder

    def edit_video(self):
        try:
            # Get lists of audio and image files
            audio_files = self.get_ordered_files(self.audio_folder, '.mp3')
            image_files = self.get_ordered_files(self.images_folder, '.png')

            if len(audio_files) != len(image_files):
                raise ValueError("The number of audio files and images is not the same.")

            # Calculate total audio duration
            total_audio_duration = self.get_total_audio_duration(audio_files)

            # Load the original video
            original_video = VideoFileClip(self.input_video_path)
            print(f"Original video duration: {original_video.duration} seconds")

            if original_video.duration < total_audio_duration:
                raise ValueError("The video length is shorter than the total audio duration.")

            # Cut a random segment of the video of appropriate length
            max_start_time = original_video.duration - total_audio_duration
            start_time = random.uniform(0, max(0, max_start_time))
            end_time = start_time + total_audio_duration

            # Cut the video segment
            video_clip = original_video.subclip(start_time, end_time)
            print(f"Selected video segment: {start_time} to {end_time} seconds")

            # List of clips with overlaid images and audio
            clips = []
            current_time = 0

            for idx, (audio_file, image_file) in enumerate(zip(audio_files, image_files)):
                try:
                    print(f"Processing audio: {audio_file}, image: {image_file}")

                    # Load the audio file
                    audio_clip = AudioFileClip(os.path.join(self.audio_folder, audio_file))
                    audio_duration = audio_clip.duration
                    print(f"Audio duration: {audio_duration} seconds")

                    # Check if the audio file is valid
                    if audio_clip is None or audio_duration <= 0:
                        raise ValueError(f"Invalid audio file: {audio_file}")

                    # Cut the video segment corresponding to the audio length
                    sub_video_clip = video_clip.subclip(current_time, current_time + audio_duration)
                    print(f"Sub-video segment: {current_time} to {current_time + audio_duration} seconds")

                    # Create an image as a clip
                    image_clip = ImageClip(os.path.join(self.images_folder, image_file)).set_duration(audio_duration)
                    image_clip = image_clip.set_position(("center", "center"))
                    # .resize(height=200)  # Optional: resize the image

                    # Overlay the image on the video
                    video_with_image = CompositeVideoClip([sub_video_clip, image_clip])

                    # Add audio to the clip
                    video_with_image = video_with_image.set_audio(audio_clip)

                    # Check if the clip is valid
                    if video_with_image is None:
                        raise ValueError(f"Generated clip is None for audio {audio_file} and image {image_file}")

                    # Add the clip to the list
                    clips.append(video_with_image)

                    current_time += audio_duration

                    # Release resources
                    # audio_clip.close()
                except Exception as e:
                    print(f"Error processing audio {audio_file} and image {image_file}: {e}")

            # Concatenate all clips
            print("Concatenating clips...")
            final_video = concatenate_videoclips(clips, method="compose").set_fps(30)

            # Check if final_video is valid
            if final_video is None:
                raise ValueError("Final video is None after concatenation")

            # Save the audio track for debugging
            print("Saving audio track...")
            final_video.audio.write_audiofile("debug_audio_output.mp3")

            # Save the final video
            print(f"Saving video to file: {self.output_video_path}")
            final_video.write_videofile(self.output_video_path, codec="libx264", audio_codec="aac")

            # Release resources
            original_video.close()
            print("Processing completed successfully.")

        except Exception as e:
            print(f"Unexpected error: {e}")

    def get_ordered_files(self, folder, extension):
        """Get an ordered list of files with the given extension"""
        files = [f for f in os.listdir(folder) if f.endswith(extension)]
        files.sort()
        return files

    def get_total_audio_duration(self, audio_files):
        """Calculate the total audio duration"""
        total_duration = 0
        for audio_file in audio_files:
            try:
                audio_clip = AudioFileClip(os.path.join(self.audio_folder, audio_file))
                if audio_clip is not None:
                    total_duration += audio_clip.duration
                audio_clip.close()
            except Exception as e:
                print(f"Error loading audio file {audio_file}: {e}")
        return total_duration