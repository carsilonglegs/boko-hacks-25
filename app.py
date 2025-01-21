from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Route for the homepage
@app.route("/")
def home():
    return render_template("home.html")

# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Dummy authentication
        if username == "admin" and password == "password":
            flash("Login successful!", "success")
            return redirect("/")
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
