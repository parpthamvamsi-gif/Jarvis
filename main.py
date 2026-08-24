from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class JarvisApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.lbl = Label(text="Jarvis Assistant Ready")
        btn = Button(text="Listen", size_hint=(1, 0.2))
        layout.add_widget(self.lbl)
        layout.add_widget(btn)
        return layout

if __name__ == '__main__':
    JarvisApp().run()
  
