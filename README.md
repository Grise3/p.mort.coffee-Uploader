![icon](https://github.com/Grise3/p.mort.coffee-Uploader/blob/main/p.mort.coffee.png?raw=true) 
# ☕ p.mort.coffee Uploader

A small **Python + Qt (PySide6)** desktop app to easily upload files to [https://p.mort.coffee](https://p.mort.coffee) using `curl`.

## 📦 Features

- One-click file upload with a graphical interface.
- Upload raw text via an integrated **text editor**.
- Automatically checks file size (limit: **100 MB**).
- Displays the upload link after completion.
- Button to **copy the link** to clipboard.
- Handles common errors (`413`, `404`, `502`, SSL issues).
- **Command-line file upload** supported.
- Auto-closes after a **40-second countdown**.

---

## 🚀 How to Use

### 🖱 GUI Mode (standard):

```bash
python main.py
```

Click:

- "**Upload File**" to choose a file.
- "**Upload Text**" to write and upload custom text content.

---

### 🖥 Command-Line Mode (direct upload):

```bash
python main.py /path/to/file.ext
```

The app will automatically upload the file and display the link.

---

## 📦 Dependencies

Make sure you have **Python 3.7+** installed, then install the following packages:

```bash
pip install PySide6 pyperclip
```

Required Python modules:

- `PySide6` – for the GUI
- `pyperclip` – to copy the link to clipboard

System requirement:

- `curl` must be available in your terminal/command prompt.

To check:

```bash
curl --version
```

---

## 🔧 How It Works

- The app uses Python's `subprocess` to call `curl`.
- Files or text are uploaded to `https://p.mort.coffee`.
- Handles expired SSL certificate warnings and lets the user continue if they choose to.

---

## 📸 Preview

![preview](https://github.com/Grise3/p.mort.coffee-Uploader/blob/main/p.mort.coffee.app.png?raw=true)

---

## 💡 Notes

- Max file size is **100 MB** (as enforced by the service).
- After uploading, a **countdown starts (40 seconds)** and the window auto-closes.
- The **text editor** is useful for quick notes, code snippets, or simple messages.

## 🛡️ Disclaimer

This tool uploads your files to a third-party service ([https://p.mort.coffee](https://p.mort.coffee)). Use at your own risk. Avoid uploading sensitive or private information unless you fully trust the host.
