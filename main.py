from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

# Set background color
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class JarvisUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # Title Label
        self.title_label = Label(
            text="JARVIS AI ASSISTANT",
            font_size='24sp',
            bold=True,
            color=(0, 0.8, 1, 1),
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.title_label)

        # Output / Response Display
        self.output_label = Label(
            text="Hello Vamsi! How can I help you today?",
            font_size='16sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.output_label.bind(size=self.output_label.setter('text_size'))
        self.add_widget(self.output_label)

        # Input Box
        self.user_input = TextInput(
            hint_text="Ask Jarvis anything...",
            multiline=False,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.8, 1, 1)
        )
        self.user_input.bind(on_text_validate=self.send_command)
        self.add_widget(self.user_input)

        # Send Button
        self.send_btn = Button(
            text="COMMAND",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=50,
            background_color=(0, 0.6, 0.8, 1)
        )
        self.send_btn.bind(on_press=self.send_command)
        self.add_widget(self.send_btn)

    def send_command(self, instance):
        text = self.user_input.text.strip()
        if text:
            self.output_label.text = f"You: {text}\nJarvis: Processing standard response..."
            self.user_input.text = ""

class JarvisApp(App):
    def build(self):
        return JarvisUI()

if __name__ == '__main__':
    JarvisApp().run()
