import os, urllib.request, random, pydub, speech_recognition, time
from DrissionPage.common import Keys
from DrissionPage import ChromiumPage


class RecaptchaSolver:
    def __init__(self, driver: ChromiumPage):
        self.driver = driver

    def solveCaptcha(self):
        iframe_inner = self.driver("@title=reCAPTCHA")
        time.sleep(0.1)

        # 点击验证码
        iframe_inner('.rc-anchor-content', timeout=1).click()
        self.driver.wait.ele_displayed("xpath://iframe[contains(@title, 'reCAPTCHA')]", timeout=3)

        # 有时候只需点击验证码即可解决
        if self.isSolved():
            return

            # 获取新的iframe
        iframe = self.driver("xpath://iframe[contains(@title, 'reCAPTCHA 验证将于 2 分钟后过期')]")

        # 点击音频按钮
        iframe('#recaptcha-audio-button', timeout=1).click()
        time.sleep(.3)

        # 获取音频源
        src = iframe('#audio-source').attrs['src']

        # 将音频下载到临时文件夹
        path_to_mp3 = os.path.normpath(
            os.path.join((os.getenv("TEMP") if os.name == "nt" else "/tmp/") + str(random.randrange(1, 1000)) + ".mp3"))
        path_to_wav = os.path.normpath(
            os.path.join((os.getenv("TEMP") if os.name == "nt" else "/tmp/") + str(random.randrange(1, 1000)) + ".wav"))

        urllib.request.urlretrieve(src, path_to_mp3)

        # 将mp3转换为wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = speech_recognition.AudioFile(path_to_wav)
        r = speech_recognition.Recognizer()
        with sample_audio as source:
            audio = r.record(source)

            # 识别音频
        key = r.recognize_google(audio)

        # 输入识别结果
        iframe('#audio-response').input(key.lower())
        time.sleep(0.1)

        # 提交结果
        iframe('#audio-response').input(Keys.ENTER)
        time.sleep(.4)

        # 检查验证码是否已解决
        if self.isSolved():
            return
        else:
            raise Exception("Failed to solve the captcha")

    def isSolved(self):
        try:
            return "style" in self.driver.ele(".recaptcha-checkbox-checkmark", timeout=1).attrs
        except:
            return False