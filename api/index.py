#!/usr/bin/env python3
"""
Lua Obfuscator - Vercel Serverless API Handler
Production-ready, optimized for cold starts
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from obfuscator import obfuscate_code
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# HTML Template (embedded for faster serverless deployment)
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 Lua Obfuscator Pro - Vercel</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}
        .container{max-width:1200px;margin:0 auto}
        .header{text-align:center;color:white;margin-bottom:30px}
        .header h1{font-size:2.5em;margin-bottom:10px;text-shadow:2px 2px 4px rgba(0,0,0,0.3)}
        .header p{font-size:1.1em;opacity:0.9}
        .main{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}
        .card{background:white;border-radius:12px;padding:20px;box-shadow:0 8px 32px rgba(0,0,0,0.1);display:flex;flex-direction:column}
        .card h2{font-size:1.3em;margin-bottom:15px;color:#667eea;border-bottom:2px solid #667eea;padding-bottom:10px}
        textarea{flex:1;padding:12px;border:2px solid #e0e0e0;border-radius:8px;font-family:'Courier New',monospace;font-size:0.9em;resize:vertical;min-height:300px}
        textarea:focus{outline:none;border-color:#667eea;box-shadow:0 0 0 3px rgba(102,126,234,0.1)}
        .options{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-bottom:20px}
        .option{display:flex;flex-direction:column;gap:10px}
        .option label{font-weight:600;color:#667eea}
        select,.input{padding:10px;border:2px solid #e0e0e0;border-radius:6px;font-family:inherit}
        select:focus,.input:focus{outline:none;border-color:#667eea}
        .checkbox{display:flex;gap:8px;align-items:center}
        input[type="checkbox"]{width:18px;height:18px;cursor:pointer;accent-color:#667eea}
        .checkbox label{cursor:pointer;margin:0}
        .buttons{display:flex;gap:10px;margin-top:20px}
        button{flex:1;padding:12px 24px;border:none;border-radius:8px;font-size:1em;font-weight:600;cursor:pointer;transition:all 0.3s;text-transform:uppercase;letter-spacing:0.5px}
        .btn-primary{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white}
        .btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 16px rgba(102,126,234,0.4)}
        .btn-secondary{background:#f0f0f0;color:#333}
        .btn-secondary:hover{background:#e0e0e0}
        .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin-top:15px;padding:15px;background:#f8f9fa;border-radius:8px}
        .stat{text-align:center}
        .stat-label{font-size:0.85em;color:#666;text-transform:uppercase;margin-bottom:5px}
        .stat-value{font-size:1.5em;font-weight:bold;color:#667eea}
        .message{padding:15px;border-radius:8px;margin-bottom:15px;display:none}
        .message.show{display:block}
        .message.success{background:#d4edda;color:#155724;border:1px solid #c3e6cb}
        .message.error{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb}
        @media(max-width:768px){.main{grid-template-columns:1fr}.header h1{font-size:1.8em}}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Lua Obfuscator Pro</h1>
            <p>Enterprise-Grade Code Protection on Vercel</p>
        </div>

        <div class="card">
            <h2>⚙️ Settings</h2>
            <div class="options">
                <div class="option">
                    <label for="mode">Mode</label>
                    <select id="mode">
                        <option value="obfuscate">Obfuscate</option>
                        <option value="minify">Minify</option>
                        <option value="beautify">Beautify</option>
                        <option value="remove_comments">Remove Comments</option>
                    </select>
                </div>

                <div class="option">
                    <label for="level">Protection Level</label>
                    <select id="level">
                        <option value="1">Light (Fast)</option>
                        <option value="2">Medium</option>
                        <option value="3" selected>Strong (Recommended)</option>
                        <option value="4">Maximum (Slowest)</option>
                    </select>
                </div>

                <div class="option checkbox">
                    <input type="checkbox" id="advanced" checked>
                    <label for="advanced">Advanced Encoding</label>
                </div>
            </div>
        </div>

        <div class="main">
            <div class="card">
                <h2>📝 Input Code</h2>
                <textarea id="input" placeholder="Paste your Lua code here..."></textarea>
            </div>

            <div class="card">
                <h2>🔒 Output Code</h2>
                <textarea id="output" readonly placeholder="Protected code will appear here..."></textarea>
                <div class="stats" id="stats" style="display:none">
                    <div class="stat">
                        <div class="stat-label">Original</div>
                        <div class="stat-value" id="origSize">0B</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Protected</div>
                        <div class="stat-value" id="newSize">0B</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Reduction</div>
                        <div class="stat-value" id="reduction">0%</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Lines</div>
                        <div class="stat-value" id="lines">0→0</div>
                    </div>
                </div>
                <button class="btn-secondary" onclick="copyCode()" style="margin-top:10px">📋 Copy</button>
            </div>
        </div>

        <div class="buttons">
            <button class="btn-primary" onclick="process()">🚀 Process Code</button>
            <button class="btn-secondary" onclick="clear()">🗑️ Clear</button>
        </div>

        <div id="msg" class="message"></div>
    </div>

    <script>
        function showMsg(text, type){
            const msg = document.getElementById('msg');
            msg.textContent = text;
            msg.className = 'message show ' + type;
            setTimeout(() => msg.className = 'message', 5000);
        }

        function formatSize(b){
            if(b===0) return '0B';
            const k=1024;
            const s=['B','KB','MB'];
            const i=Math.floor(Math.log(b)/Math.log(k));
            return Math.round(b/Math.pow(k,i)*100)/100 + s[i];
        }

        async function process(){
            const code = document.getElementById('input').value;
            if(!code.trim()) return showMsg('Enter code first', 'error');

            try{
                const res = await fetch('/api/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        code,
                        mode: document.getElementById('mode').value,
                        level: parseInt(document.getElementById('level').value),
                    })
                });

                const data = await res.json();
                if(data.success){
                    document.getElementById('output').value = data.result;
                    document.getElementById('origSize').textContent = formatSize(data.stats.original_size);
                    document.getElementById('newSize').textContent = formatSize(data.stats.result_size);
                    document.getElementById('reduction').textContent = data.stats.reduction;
                    document.getElementById('lines').textContent = data.stats.original_lines + '→' + data.stats.result_lines;
                    document.getElementById('stats').style.display = 'grid';
                    showMsg('✓ Code protected successfully!', 'success');
                } else {
                    showMsg('Error: ' + data.error, 'error');
                }
            } catch(e){
                showMsg('Error: ' + e.message, 'error');
            }
        }

        function copyCode(){
            document.getElementById('output').select();
            document.execCommand('copy');
            showMsg('Copied to clipboard!', 'success');
        }

        function clear(){
            document.getElementById('input').value = '';
            document.getElementById('output').value = '';
            document.getElementById('stats').style.display = 'none';
        }

        document.getElementById('input').addEventListener('keydown', e => {
            if(e.ctrlKey && e.key==='Enter') process();
        });
    </script>
</body>
</html>'''


@app.route('/', methods=['GET'])
def index():
    """Serve the web UI"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/process', methods=['POST'])
def process():
    """Main obfuscation endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        code = data.get('code', '')
        mode = data.get('mode', 'obfuscate')
        level = data.get('level', 3)
        
        if not code.strip():
            return jsonify({'success': False, 'error': 'Code cannot be empty'}), 400
        
        if len(code) > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({'success': False, 'error': 'Code too large (max 10MB)'}), 413
        
        # Process code
        result = obfuscate_code(code, mode, level)
        
        return jsonify({
            'success': True,
            'result': result['result'],
            'stats': result['stats']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/compare', methods=['POST'])
def compare():
    """Compare different modes"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        modes = {}
        for mode in ['minify', 'beautify', 'obfuscate']:
            result = obfuscate_code(code, mode, 3)
            modes[mode] = {
                'code': result['result'],
                'size': result['stats']['result_size']
            }
        
        return jsonify({
            'success': True,
            'comparison': modes
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    """API information"""
    return jsonify({
        'service': 'Lua Obfuscator Pro',
        'version': '2.0',
        'modes': ['obfuscate', 'minify', 'beautify', 'remove_comments'],
        'levels': [1, 2, 3, 4],
        'max_size': '10MB',
        'features': [
            'Variable Obfuscation',
            'String Encoding',
            'Dead Code Injection',
            'Control Flow Obfuscation',
            'Advanced Minification',
            'Comment Removal'
        ]
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy'}), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500
