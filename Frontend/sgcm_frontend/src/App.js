import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async () => {
    try {
      const res = await axios.post('http://localhost:5000/process', { text: inputText });
      setResponse(res.data);
    } catch (error) {
      setResponse({ error: error.response?.data?.error || "Something went wrong" });
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <h1>Multilingual Input Processor</h1>
      <textarea
        rows="6"
        cols="60"
        placeholder="Type or paste your input here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        style={{ padding: '10px', fontSize: '16px', borderRadius: '5px', border: '1px solid #ccc' }}
      />
      <br />
      <button
        onClick={handleSubmit}
        style={{ marginTop: 10, padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}
      >
        Submit
      </button>

      {response && (
        <div style={{ marginTop: 30 }}>
          {response.error ? (
            <p style={{ color: 'red' }}>{response.error}</p>
          ) : (
            <>
              <p><strong>Detected Languages:</strong> {response.detected_languages.join(', ')}</p>

              <h3>Translated Sentences:</h3>
              <ul>
                {response.translations.map((item, index) => (
                  <li key={index} style={{ marginBottom: 5 }}>
                    <strong>Original:</strong> "{item.original}"<br />
                    <strong>Language:</strong> {item.detected_language}<br />
                    <strong>Translation:</strong> {item.translated}
                  </li>
                ))}
              </ul>

              <p><strong>Combined Translated Text:</strong><br />{response.combined_translated_text}</p>
              <p><strong>Extracted Keywords:</strong> {response.keywords.join(', ')}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
