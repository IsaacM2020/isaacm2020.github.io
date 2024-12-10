import os
import re
import shutil
import json
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Listbox, Scrollbar
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess
from PIL import Image

# Global variables
featured_image_path = None
dropped_files = []
config_path = "config.json"
config = {}

def load_config():
    global config
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            config = json.load(file)
    else:
        config = {
            "documents_path": "",
            "obsidian_vault_path": "",
            "site_repository_path": ""
        }

def save_config():
    with open(config_path, "w") as file:
        json.dump(config, file, indent=4)

def setup_configuration():
    # Let the user choose directories
    user_documents = filedialog.askdirectory(title="Select Documents Folder")
    obsidian_vault = filedialog.askdirectory(title="Select Obsidian Vault Path")
    site_repo = filedialog.askdirectory(title="Select Site Repository Path")

    if user_documents and obsidian_vault and site_repo:
        config["documents_path"] = user_documents
        config["obsidian_vault_path"] = obsidian_vault
        config["site_repository_path"] = site_repo
        save_config()
        messagebox.showinfo("Setup", "Configuration saved successfully!")
    else:
        messagebox.showerror("Error", "Setup incomplete. Please provide all paths.")

def ensure_configured():
    if not config["documents_path"] or not config["obsidian_vault_path"] or not config["site_repository_path"]:
        messagebox.showinfo("Configuration Required", "Please set up the paths first.")
        setup_configuration()

def process_files():
    global featured_image_path, dropped_files
    ensure_configured()
    
    target_folder_name = target_folder_entry.get()
    if not target_folder_name.strip():
        messagebox.showerror("Error", "Please enter a folder name.")
        return

    target_folder = os.path.join(config["site_repository_path"], "content", "posts", target_folder_name)

    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)  # Remove the existing folder
    os.makedirs(target_folder, exist_ok=True)

    first_image_handled = False  # Flag to handle the first image duplication

    for filepath in dropped_files:
        filename = os.path.basename(filepath)

        if filename.endswith(".md"):
            # Process Markdown files
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            # Find and replace image links
            images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
            for image in images:
                encoded_image = image.replace(' ', '%20')
                markdown_image = f"![Image Description]({encoded_image})"
                content = content.replace(f"[[{image}]]", markdown_image)

                if not first_image_handled:
                    source_image_path = os.path.join(os.path.dirname(filepath), image)
                    if os.path.exists(source_image_path):
                        target_image_path = os.path.join(target_folder, image)
                        shutil.copy(source_image_path, target_image_path)
                        first_image_handled = True

            target_md_path = os.path.join(target_folder, "index.md")
            with open(target_md_path, "w", encoding="utf-8") as file:
                file.write(content)

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            shutil.copy(filepath, target_folder)

    # Handle featured image
    if featured_image_path and os.path.exists(featured_image_path):
        featured_target_path = os.path.join(target_folder, "featured.png")
        if not featured_image_path.lower().endswith('.png'):
            img = Image.open(featured_image_path)
            img.save(featured_target_path, 'PNG')
        else:
            shutil.copy(featured_image_path, featured_target_path)

    messagebox.showinfo("Success", f"Files processed and saved to:\n{target_folder}")
    dropped_files = []
    featured_image_path = None
    dropped_files_label.config(text="Drop files here")
    featured_image_label.config(text="No image selected")

def select_featured_image():
    global featured_image_path
    ensure_configured()
    filetypes = [
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpg *.jpeg"),
        ("All image files", "*.png *.jpg *.jpeg")
    ]
    featured_image_path = filedialog.askopenfilename(
        initialdir=config["obsidian_vault_path"],
        title="Select Featured Image",
        filetypes=filetypes
    )
    if featured_image_path:
        featured_image_label.config(text=f"Selected: {os.path.basename(featured_image_path)}")
    else:
        featured_image_label.config(text="No image selected")

def on_drop(event):
    global dropped_files
    dropped_files = event.data.split(" ")
    dropped_files_label.config(text="\n".join(dropped_files))

def browse_files():
    global dropped_files
    ensure_configured()
    filetypes = [("All files", "*.*")]
    selected_files = filedialog.askopenfilenames(
        initialdir=config["obsidian_vault_path"],
        title="Select Markdown or Image Files",
        filetypes=filetypes
    )
    dropped_files.extend(selected_files)
    dropped_files_label.config(text="\n".join(dropped_files))

def push_to_github():
    ensure_configured()
    try:
        site_path = config["site_repository_path"]
        os.chdir(site_path)
        commands = [
            ["git", "add", "."],
            ["git", "commit", "-m", "Site update"],
            ["git", "pull"],
            ["git", "push", "-u", "origin", "master"]
        ]
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"Command {' '.join(cmd)} output: {result.stdout}")
        messagebox.showinfo("GitHub Push", "Successfully pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("GitHub Push Error", f"Git error: {e.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
load_config()
root = TkinterDnD.Tk()
root.title("Markdown and Image Processor with Post Manager")
root.geometry("800x800")

setup_button = Button(root, text="Setup Paths", command=setup_configuration)
setup_button.pack(pady=10)

Label(root, text="Drag and drop Markdown and image files below:").pack(pady=10)

dropped_files_label = Label(root, text="Drop files here", bg="lightgray", relief="sunken", width=50, height=10)
dropped_files_label.pack(pady=10)
dropped_files_label.drop_target_register(DND_FILES)
dropped_files_label.dnd_bind("<<Drop>>", on_drop)

browse_button = Button(root, text="Browse Files", command=browse_files)
browse_button.pack(pady=5)

Label(root, text="Enter new post folder:").pack(pady=10)
target_folder_entry = Entry(root, width=40)
target_folder_entry.pack(pady=5)

process_button = Button(root, text="Process Files", command=process_files)
process_button.pack(pady=20)

Label(root, text="Featured Image:").pack(pady=5)
featured_image_button = Button(root, text="Select Featured Image", command=select_featured_image)
featured_image_button.pack(pady=5)
featured_image_label = Label(root, text="No image selected")
featured_image_label.pack(pady=5)

github_push_button = Button(root, text="Push to GitHub", command=push_to_github)
github_push_button.pack(pady=5)

root.mainloop()
