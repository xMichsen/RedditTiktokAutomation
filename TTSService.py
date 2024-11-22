from google.cloud import texttospeech
from dotenv import load_dotenv
import os

class TTSGenerator:
    def __init__(self, language_code='pl-PL', voice_name=None, ssml_gender='NEUTRAL', speaking_rate=1.2, pitch=0.2):
        load_dotenv()
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.client = texttospeech.TextToSpeechClient.from_service_account_file(credentials_path)
        self.language_code = language_code
        self.voice_name = voice_name
        self.ssml_gender = getattr(texttospeech.SsmlVoiceGender, ssml_gender)
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

    def text_to_speech(self, text, filename='output.mp3'):
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Voice selection
        voice_params = {
            'language_code': self.language_code,
            'ssml_gender': self.ssml_gender
        }
        if self.voice_name:
            voice_params['name'] = self.voice_name

        voice = texttospeech.VoiceSelectionParams(**voice_params)

        # Generating speech
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=self.audio_config
        )

        # Saving to file
        with open(filename, 'wb') as out:
            out.write(response.audio_content)
            print(f'Audio file has been saved as {filename}.')
