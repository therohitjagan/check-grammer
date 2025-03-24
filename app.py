import language_tool_python
from flask import Flask, request, jsonify
from flask_cors import CORS  # For cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the language tool once at startup for better performance
tool = language_tool_python.LanguageTool('en-US')

@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    matches = tool.check(text)
    suggestions = []
    
    for match in matches:
        suggestions.append({
            'mistake': text[match.offset:match.offset + match.errorLength],
            'message': match.message,
            'suggestions': match.replacements[:5],  # Limit to top 5 suggestions
            'offset': match.offset,
            'length': match.errorLength,
            'context': text[max(0, match.offset-30):match.offset+match.errorLength+30]
        })
    
    return jsonify({
        'text': text,
        'suggestions': suggestions,
        'count': len(suggestions)
    })

# Simple health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # For development only - use a proper WSGI server in production
    app.run(host='0.0.0.0', port=5000, debug=False)