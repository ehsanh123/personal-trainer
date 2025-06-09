from flask import Flask, render_template, jsonify
import asyncio

app = Flask(__name__)

async def call_service():
    await asyncio.sleep(2)  # simulate long processing
    return "<b>Data from service:</b> Here is your dynamic result."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    result = asyncio.run(call_service())
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)