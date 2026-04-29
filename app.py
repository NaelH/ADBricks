from flask import Flask, render_template, request, redirect
import adb_client

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/devices")
def devicespage():
    devices = adb_client.get_devices()
    return render_template("devices.html", devices=devices)

@app.route("/tcpip")
def tcpippage():
    return render_template("tcpip.html")

@app.route("/tcpip/connect", methods=["POST"])
def connect():
    device = request.form.get("device")
    adb_client.connect_device(device)
    return redirect("/devices")

@app.route("/api/devices")
def api_devices():
    return "<p>API DEVICES</p>"

@app.route("/api/device")
def api_device():
    return "<p>API DEVICE SANS LE S</p>"

if __name__ == "__main__":
    app.run()