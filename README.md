![ADBricks Cover](https://raw.githubusercontent.com/NaelH/ADBricks/refs/heads/readme/assets/cover.png)
# 🧱 ADBricks

ADBricks est une API Flask en Python permettant de piloter un appareil Android via ADB depuis une interface web. Le projet propose des fonctionnalités comme la gestion des applications, les captures d’écran et l’accès aux informations système, avec une architecture modulaire basée sur des plugins.

---

## 🚀 Fonctionnalités

- 📱 Informations appareil (modèle, version Android, etc.)
- 🔋 État de la batterie
- 📦 Liste des applications installées
- 📸 Capture d’écran
- 🧩 Système de plugins dynamique
- 🌐 Interface web simple via Flask

---

## 🏗️ Architecture

```
ADBricks/
├── app.py
├── adb_client.py
├── plugin_loader.py
├── plugins/
│   └── example_plugin.py
├── templates/
│   └── index.html
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Prérequis

- Python 3.10+
- ADB installé

```bash
sudo apt update
sudo apt install adb python3 python3-venv
```

### 2. Installation

```bash
git clone https://github.com/NaelH/ADBricks.git
cd adbricks

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 📲 Configuration Android

1. Activer les options développeur
2. Activer le débogage USB
3. Connecter le téléphone

Vérification :

```bash
adb devices
```

---

## ▶️ Lancement

```bash
python3 app.py
```

Accès : http://127.0.0.1:5000

---

## 🔌 Système de plugins

Chaque plugin est un fichier Python dans le dossier `plugins/`.

### Structure d’un plugin :

```python
def register(app):
    @app.get("/api/plugin/example")
    def example():
        return {"status": "ok"}
```

Les plugins sont chargés automatiquement au démarrage.

---

## 🧪 Exemples d’API

| Endpoint            | Description        |
|--------------------|--------------------|
| /api/device        | Infos appareil     |
| /api/battery       | Batterie           |
| /api/apps          | Liste des apps     |
| /api/screenshot    | Capture écran      |

---

## 🔐 Sécurité

⚠️ ADB donne un accès complet au téléphone.

- Utiliser uniquement en local
- Ne pas exposer l’API sur Internet sans protection
- Ajouter une authentification si nécessaire

---

## 🛠️ Roadmap

- [ ] Authentification API
- [ ] Upload / Download fichiers
- [ ] Gestion SMS (si possible)
- [ ] Interface UI améliorée
- [ ] WebSocket (temps réel)
- [ ] Support multi-device

---

## 📄 Licence

Projet sous licence propriétaire.  
Toute reproduction, modification ou distribution est interdite sans autorisation.

---

## 👨‍💻 Auteur

Projet développé dans un objectif de pratique en cybersécurité, développement Python et automatisation.
