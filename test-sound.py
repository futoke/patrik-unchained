import requests
import subprocess
# from pydub import AudioSegment
# from pydub.playback import play


# audio_data = AudioSegment.from_mp3("test.mp3")
# play(audio_data)

class RHVoiceREST:
    BUFF_SIZE = 1024

    def __init__(
            self, 
            text, 
            audio_format='wav', 
            speaker='aleksandr',
            url='http://192.168.1.63:8080/say'
        ):

        self._url = url
        self._params = {
            'text': text,
            'format': audio_format,
            'voice': speaker
        }
        self._data = None
        self._request()

    def _request(self):
        try:
            self._rq = requests.get(self._url, params=self._params, stream=True, timeout=60)
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            raise RuntimeError(str(e))
        if not self._rq.ok:
            raise RuntimeError('{}: {}'.format(self._rq.status_code, self._rq.reason))
        self._data = self._rq.iter_content

    def iter_me(self):
        if self._data is None:
            raise RuntimeError('No data')
        for chunk in self._data(chunk_size=self.BUFF_SIZE):
            yield chunk

    def save_fp(self, fp):
        for chunk in self.iter_me():
            fp.write(chunk)


phrase = "Привет, кожаные мешки"
popen = subprocess.Popen(['aplay', '-q', '-'], stdin=subprocess.PIPE)
try:
    if isinstance(phrase, str):
        RHVoiceREST(text=phrase).save_fp(popen.stdin)
except RuntimeError as e:
    print(e)
    popen.stdin.close()
    exit(1)
else:
    popen.stdin.close()
    popen.wait(300)