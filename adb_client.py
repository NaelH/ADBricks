import subprocess

default_device = "192.168.240.112:5555"

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