from flask import Flask
app = Flask(__name__)

@app.route("/{poopoo}")
def hello():
    return "hElLo WoRlD" + poopoo


def

if __name__ == '__main__':
    app.run(debug=True)
