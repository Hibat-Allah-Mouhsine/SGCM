from flask import Flask, render_template
import pymongo
app = Flask(__name__)

@app.route("/SGCM_Home")
def Main_Page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
