from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        deci = (request.args.get('decibel'))
        return deci

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=80)