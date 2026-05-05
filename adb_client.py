import subprocess
import base64

default_device = "192.168.240.112:5555"
default_device = "7.7.7.7:5555"

def run_adb(args, device=None, timeout=15):
    """
    Execute les commande ADB
    Exemple d'utilisation : run_adb(["shell", "getprop", "ro_product.model"])
    """

    command = ["adb"]
    if device:
        command += ["-s", device]
    
    command += args

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()

def connect_device(device=default_device):
    """
    Connexion à un device (WayDroid par défaut)
    """
    return run_adb(["connect", device], device=None)

def list_devices():
    """
    Lister les devices disponible sur ADB
    """
    output = run_adb(["devices"], device=None)
    devices = []

    for line in output.splitlines()[1:]:
        if line.strip():
            parts = line.split()
            devices.append({
                "id": parts[0],
                "status": parts[1]
            })

    return devices

def list_files(devices, path):
    """
    Récupère les fichier à un emplacement précis sur un téléphone précis
    """


def get_device_model(device=default_device):
    """
    Récupère le modèle android
    """
    return run_adb(
        ["shell", "getprop", "ro.product.model"],
        device=None
    )

def get_android_version(device=default_device):
    """
    Récupère la version android
    """
    return run_adb(
        ["shell", "getprop", "ro.build.version.release"],
        device=None
    )

def get_devices():
    """
    Lister l'ensemble des appareils connecté
    """
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]

    devices = []
    for line in lines:
        if line.strip():
            parts = line.split()
            devices.append({
                "id": parts[0],
                "status": parts[1]
            })
    return devices

def connect_device(device=default_device):
    """
    Connecter un android
    """
    run_adb(["connect", device])

def disconnect_device(device=default_device):
    """
    Déconnecter l'android
    """
    run_adb(["disconnect", device])

def parse_ls_output(output):
    """
    Parseur des sorties de la commande ls
    """
    files = []

    for line in output.splitlines():
        if not line.strip():
            continue

        if line.startswith("total"):
            continue

        parts = line.split(maxsplit=7)

        if len(parts) < 8:
            continue

        permissions = parts[0]
        size = parts[4]
        date = parts[5]
        time = parts[6]
        name = parts[7]

        if name in [".", ".."]:
            continue

        file_type = "file"

        if permissions.startswith("d"):
            file_type = "directory"
        elif permissions.startswith("l"):
            file_type = "link"

        files.append({
            "name": name,
            "permissions": permissions,
            "size": size,
            "date": date,
            "time": time,
            "type": file_type
        })

    return files


def list_files(device, path="/sdcard/"):
    """
    Lister les fichiers d'un device et à un emplacement défini
    """
    if not path.endswith("/"):
        path += "/"

    output = run_adb([
        "-s", device,
        "shell",
        "ls", "-la", path
    ])

    return parse_ls_output(output)

def list_packages(device):
    """
    Liste les applications présent sur le téléphone
    """
    output = run_adb([
        "-s", device,
        "shell",
        "pm", "list", "packages"
    ])

    packages = []

    for line in output.splitlines():
        if line.startswith("package:"):
            packages.append(line.replace("package:", "").strip())

    return packages

def run_shell(device, command):
    return run_adb([
        "-s", device,
        "shell",
        command
    ])


def run_shell_all(command):
    devices = list_devices()
    results = []

    for device in devices:
        device_id = device["id"]
        status = device["status"]

        if status != "device":
            results.append({
                "device": device_id,
                "status": status,
                "output": "Appareil non prêt"
            })
            continue

        try:
            output = run_shell(device_id, command)
        except Exception as e:
            output = f"Erreur : {str(e)}"

        results.append({
            "device": device_id,
            "status": status,
            "output": output
        })

    return results


def get_logs(device, lines=200):
    """
    Récupère les logs Android les plus récents,
    puis les affiche du plus récent au plus ancien.
    """
    output = run_adb([
        "-s", device,
        "logcat",
        "-d"
    ])

    logs = output.splitlines()
    recent_logs = logs[-int(lines):]

    recent_logs.reverse()

    return "\n".join(recent_logs)
def get_screenshot(device):
    """
    Récupère une capture écran du device en base64.
    """
    result = subprocess.run(
        ["adb", "-s", device, "exec-out", "screencap", "-p"],
        capture_output=True,
        timeout=10
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode(errors="ignore"))

    return base64.b64encode(result.stdout).decode("utf-8")
    

def tap(device, x, y):
    """
    Simule un appui tactile sur l'écran.
    """
    return run_adb(
        ["shell", "input", "tap", str(x), str(y)],
        device=device
    )


def swipe(device, x1, y1, x2, y2, duration=300):
    """
    Simule un swipe.
    """
    return run_adb(
        [
            "shell", "input", "swipe",
            str(x1), str(y1),
            str(x2), str(y2),
            str(duration)
        ],
        device=device
    )


def input_text(device, text):
    """
    Envoie du texte sur le téléphone.
    """
    safe_text = text.replace(" ", "%s")

    return run_adb(
        ["shell", "input", "text", safe_text],
        device=device
    )


def keyevent(device, key):
    """
    Envoie une touche système Android.
    """
    keys = {
        "home": "KEYCODE_HOME",
        "back": "KEYCODE_BACK",
        "recent": "KEYCODE_APP_SWITCH",
        "power": "KEYCODE_POWER",
        "enter": "KEYCODE_ENTER",
        "volume_up": "KEYCODE_VOLUME_UP",
        "volume_down": "KEYCODE_VOLUME_DOWN"
    }

    keycode = keys.get(key)

    if not keycode:
        raise ValueError("Touche inconnue")

    return run_adb(
        ["shell", "input", "keyevent", keycode],
        device=device
    )