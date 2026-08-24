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
                # App background ki vellakunda stay avneki flags:
                intent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, activity.getPackageName())
                intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
                
                recognizer.startListening(intent)

            activity.runOnUiThread(run_speech)
