import speech_recognition as sr
from deep_translator import GoogleTranslator

def translate_text(input_text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translation = translator.translate(input_text)
    return translation

def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech in both Tamil and English
        speech_text = recognizer.recognize_google(audio, language='ta-IN,en-IN')
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

    target_language = input("Enter the target language ('ta' for Tamil, 'en' for English): ")
    if target_language not in ['ta', 'en']:
        print("Invalid target language")
        return

    translation = translate_text(input_text, target_language)
    print(f"Translation in {target_language}: {translation}")

if __name__ == "__main__":
    main()