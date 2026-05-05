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

@app.route("/tcpip/disconnect", methods=["POST"])
def disconnect():
    device = request.form.get("device")
    adb_client.disconnect_device(device)
    return redirect("/devices")

@app.route("/files")
def files():
    device = request.args.get("device")
    path = request.args.get("path", "/sdcard/")

    devices = adb_client.list_devices()

    if not device:
        if devices:
            device = devices[0]["id"]
        else:
            return render_template(
                "files.html",
                device=None,
                path=None,
                files=[]
            )

    files = adb_client.list_files(device, path)

    parent_path = None

    if path != "/":
        parent_path = "/".join(path.rstrip("/").split("/")[:-1])

        if parent_path == "":
            parent_path = "/"

    return render_template(
        "files.html",
        device=device,
        path=path,
        parent_path=parent_path,
        files=files
    )

@app.route("/apps")
def apps():
    selected_device = request.args.get("device")
    devices = adb_client.list_devices()

    if not devices:
        return render_template(
            "apps.html",
            devices=[],
            selected_device=None,
            apps=[]
        )

    if not selected_device:
        selected_device = devices[0]["id"]

    apps = adb_client.list_packages(selected_device)

    return render_template(
        "apps.html",
        devices=devices,
        selected_device=selected_device,
        apps=apps
    )

@app.route("/shell", methods=["GET", "POST"])
def shell():
    devices = adb_client.list_devices()
    selected_device = request.args.get("device") or request.form.get("device")

    if not devices:
        return render_template(
            "shell.html",
            devices=[],
            selected_device=None,
            command=None,
            output=None,
            results=[]
        )

    if not selected_device:
        selected_device = devices[0]["id"]

    output = None
    results = []
    command = None

    if request.method == "POST":
        command = request.form.get("command")
        target = request.form.get("target")

        if command:
            if target == "all":
                results = adb_client.run_shell_all(command)
            else:
                try:
                    output = adb_client.run_shell(selected_device, command)
                except Exception as e:
                    output = f"Erreur : {str(e)}"

    return render_template(
        "shell.html",
        devices=devices,
        selected_device=selected_device,
        command=command,
        output=output,
        results=results
    )

    
@app.route("/api/devices")
def api_devices():
    return "<p>API DEVICES</p>"

@app.route("/api/device")
def api_device():
    return "<p>API DEVICE SANS LE S</p>"

if __name__ == "__main__":
    app.run()