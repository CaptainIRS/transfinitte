from googletrans import Translator
from googletrans import LANGUAGES

def translate(text, dest='en'):
    translator = Translator()
    return translator.translate(text, dest=dest).text

if __name__ == '__main__':
    # Rinish Sam in Tamil
    print(translate('ரினிஷ் சம்'))