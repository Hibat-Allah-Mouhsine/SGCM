from flask import Flask, request, jsonify
from flask_cors import CORS
from langdetect import detect
from deep_translator import GoogleTranslator
from keybert import KeyBERT
import re

app = Flask(__name__)
CORS(app)

kw_model = KeyBERT()

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    user_input = data.get('text', '')

    if not user_input.strip():
        return jsonify({'error': "No text provided."}), 400

    # Step 1: Split into sentences or chunks
    sentences = re.split(r'(?<=[.?!؟])\s+|(?<=،)\s+|(?<=\n)', user_input)  # Better splitting for multilingual input

    translations = []
    langs = set()
    combined_translated_text = ''

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        try:
            lang = detect(sentence)
            langs.add(lang)
        except Exception as e:
            lang = "undetected"

        try:
            translated = GoogleTranslator(source='auto', target='en').translate(sentence)
        except Exception as e:
            translated = f"[Translation failed: {str(e)}]"

        translations.append({
            'original': sentence,
            'detected_language': lang,
            'translated': translated
        })

        combined_translated_text += translated + " "

    # Step 2: Keyword Extraction on full translated text
    try:
        keywords = kw_model.extract_keywords(combined_translated_text.strip(), keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
        keyword_list = [kw[0] for kw in keywords]
    except Exception as e:
        return jsonify({'error': f"Keyword extraction failed: {str(e)}"}), 400

    return jsonify({
        'detected_languages': list(langs),
        'translations': translations,
        'combined_translated_text': combined_translated_text.strip(),
        'keywords': keyword_list
    })

if __name__ == '__main__':
    app.run(debug=True)
