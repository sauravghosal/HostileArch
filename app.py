from flask import Flask
app = Flask(__name__)

@app.route("/{poopoo}")
def hello():
    return "hElLo WoRlD" + poopoo

if __name__ == '__main__':
    app.run(debug=True)
