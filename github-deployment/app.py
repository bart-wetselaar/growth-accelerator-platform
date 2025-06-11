from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Growth Accelerator Platform</h1><p>Azure Web App - Healthy</p>"

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
