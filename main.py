from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.utils import platform

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass, PythonJavaClass, java_method

    Intent = autoclass('android.content.Intent')
    RecognizerIntent = autoclass('android.speech.RecognizerIntent')
    SpeechRecognizer = autoclass('android.speech.SpeechRecognizer')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')

    class SpeechListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/RecognitionListener']
        __javacontext__ = 'app'

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method('(Landroid/os/Bundle;)V')
        def onReadyForSpeech(self, params): pass
        @java_method('()V')
        def onBeginningOfSpeech(self): pass
        @java_method('(F)V')
        def onRmsChanged(self, rmsdB): pass
        @java_method('([B)V')
        def onBufferReceived(self, buffer): pass
        @java_method('()V')
        def onEndOfSpeech(self): pass

        @java_method('(I)V')
        def onError(self, error):
            self.callback(f"Error code: {error}")

        @java_method('(Landroid/os/Bundle;)V')
        def onResults(self, results):
            matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
            if matches and matches.size() > 0:
                text = matches.get(0)
                self.callback(text)

        @java_method('(ILandroid/os/Bundle;)V')
        def onPartialResults(self, partialResults): pass
        @java_method('(ILandroid/os/Bundle;)V')
        def onEvent(self, eventType, params): pass

    class TTSOnInitListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
        __javacontext__ = 'app'

        def __init__(self, tts_instance):
            super().__init__()
            self.tts = tts_instance

        @java_method('(I)V')
        def onInit(self, status):
            if status == TextToSpeech.SUCCESS:
                self.tts.setLanguage(Locale.US)

class JarvisApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.label = Label(text="Jarvis Assistant Ready", font_size='20sp')
        self.btn = Button(text="Listen", size_hint=(1, 0.2), background_color=(0, 0.6, 0.9, 1))
        self.btn.bind(on_press=self.start_listening)
        
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn)
        
        self.tts = None
        return self.layout

    def on_start(self):
        if platform == 'android':
            request_permissions([Permission.RECORD_AUDIO, Permission.INTERNET])
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            self.tts_listener = TTSOnInitListener(None)
            self.tts = TextToSpeech(activity, self.tts_listener)
            self.tts_listener.tts = self.tts

    def speak(self, text):
        if platform == 'android' and self.tts:
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, None)

    def start_listening(self, instance):
        if platform == 'android':
            self.label.text = "Listening..."
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            def run_speech():
                recognizer = SpeechRecognizer.createSpeechRecognizer(activity)
                listener = SpeechListener(self.on_speech_result)
                recognizer.setRecognitionListener(listener)

                intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                recognizer.startListening(intent)

            activity.runOnUiThread(run_speech)

    @mainthread
    def on_speech_result(self, text):
        self.label.text = f"You said: {text}"
        
        # Simple Jarvis Response Logic
        response = f"I heard you say {text}"
        if "hello" in text.lower():
            response = "Hello boss! Jarvis system online and ready."
        elif "how are you" in text.lower():
            response = "All systems operational. How can I assist you?"
            
        self.speak(response)

if __name__ == '__main__':
    JarvisApp().run()
