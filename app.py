from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')          
def hello():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return "This is THE dashboard"


if __name__ == "__main__":
    app.run()

