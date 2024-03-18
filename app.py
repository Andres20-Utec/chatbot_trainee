from flask import Flask, render_template, request, jsonify
from chatbot import respuesta_documento


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.form['message']    
    bot_response = respuesta_documento(user_message)[1]
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)