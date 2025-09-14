from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

donation_file = os.path.join(BASE_DIR, "food_donations_list.xlsx")

# Initialize Excel if not exists
if not os.path.exists(donation_file):
    df = pd.DataFrame(columns=[
        "Donor Name", "Food Name", "Quantity", "Donate Date",
        "Phone", "Location", "Address"
    ])
    df.to_excel(donation_file, index=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_donation():
    if request.method == "POST":
        donor = request.form["donor"]
        food = request.form["food"]
        qty = request.form["quantity"]
        donate_date = request.form["donate_date"]
        phone = request.form["phone"]
        location = request.form["location"]
        address = request.form["address"]

        df = pd.read_excel(donation_file)
        new_entry = {
            "Donor Name": donor,
            "Food Name": food,
            "Quantity": qty,
            "Donate Date": donate_date,
            "Phone": phone,
            "Location": location,
            "Address": address
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(donation_file, index=False)

        return redirect(url_for("view_donations"))
    return render_template("add_donation.html")

@app.route("/view")
def view_donations():
    df = pd.read_excel(donation_file)
    records = df.to_dict(orient="records")
    return render_template("view_donations.html", donations=records)

if __name__ == "__main__":
    app.run(debug=True)
