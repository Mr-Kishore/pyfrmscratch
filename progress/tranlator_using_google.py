import speech_recognition as sr
from googletrans import Translator

def translate_text(input_text, target_language='es'):
    translator = Translator()
    translation = translator.translate(input_text, dest=target_language)
    return translation.text

def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        speech_text = recognizer.recognize_google(audio)
        print("You said: " + speech_text)
        return speech_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def main():
    choice = input("Enter '1' for text input or '2' for voice input: ")

    if choice == '1':
        input_text = input("Enter the text to translate: ")
    elif choice == '2':
        input_text = recognize_speech()
        if input_text is None:
            return
    else:
        print("Invalid choice")
        return

    target_language = input("Enter the target language (e.g., 'es' for Spanish, 'fr' for French): ")
    translation = translate_text(input_text, target_language)
    print(f"Translation in {target_language}: {translation}")

if __name__ == "__main__":
    main()