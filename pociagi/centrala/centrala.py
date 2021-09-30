from flask import Flask, request, jsonify
from flask.templating import render_template

app = Flask(__name__, template_folder="templates")

@app.route("/centrala/endpoint", methods=["GET", "POST"])
def logpociag():
    if request.method=="POST":
        content = request.json
        print(content)
        return str(content)+" :)", 201

if __name__ == "__main__":
    app.run(host="centrala-api",port=1200)