import os
import shutil
import subprocess

# Set variables for your paths and file names
HUGO_SITE_PATH = r'C:\Users\isaac\isaacblogs'  # Replace with your Hugo site directory
OBSIDIAN_VAULT_PATH = r'C:\Users\isaac\OneDrive\Documents\obby1\posts'  # Replace with your Obsidian vault directory
OBSIDIAN_IMAGE_PATH = r'C:\Users\isaac\OneDrive\Documents\obby1\Attachments'  # Replace with your Obsidian image directory
STATIC_IMAGE_PATH = os.path.join(HUGO_SITE_PATH, 'static', 'images')  # Hugo static images directory
CONTENT_PATH = os.path.join(HUGO_SITE_PATH, 'content')  # Hugo content directory

def run_command(command):
    """Run a system command and print output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        exit(1)

def git_add_commit_push():
    """Add, commit, pull, and push changes to the remote Git repository."""
    # Navigate to the Hugo site directory
    os.chdir(HUGO_SITE_PATH)

    # Add all changes
    print("Adding all changes...")
    run_command("git add .")

    # Commit changes with a custom message
    commit_message = input("Enter your commit message: ")
    run_command(f"git commit -m \"{commit_message}\"")

    # Pull latest changes from the remote repository
    print("Pulling latest changes...")
    run_command("git pull origin master")

    # Push changes to the remote repository
    print("Pushing changes to the remote repository...")
    run_command("git push -u origin master")

def copy_images():
    """Copy images from Obsidian to Hugo static images folder."""
    print("Copying images from Obsidian to Hugo site...")
    if not os.path.exists(STATIC_IMAGE_PATH):
        os.makedirs(STATIC_IMAGE_PATH)

    for file_name in os.listdir(OBSIDIAN_IMAGE_PATH):
        full_file_name = os.path.join(OBSIDIAN_IMAGE_PATH, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, STATIC_IMAGE_PATH)
    print("Images copied successfully.")

def update_thumbnail():
    """Update front matter of markdown files with thumbnail image."""
    thumbnail_file = input("Enter the image file name for thumbnail (e.g., 'thumbnail.jpg') or leave blank if not needed: ")
    
    if thumbnail_file:
        print("Updating content with thumbnail reference...")
        for root, dirs, files in os.walk(os.path.join(HUGO_SITE_PATH, 'content')):
            for file_name in files:
                if file_name.endswith('.md'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'thumbnail:' not in content:
                        with open(file_path, 'a', encoding='utf-8') as f:
                            f.write(f"\nthumbnail: /images/{thumbnail_file}")
                        print(f"Added thumbnail to {file_name}")
                    else:
                        print(f"Thumbnail already exists in {file_name}")

def process_obsidian_md():
    """Process a markdown file from Obsidian vault to Hugo content folder."""
    md_file_name = input("Enter the name of the .md file from Obsidian (e.g., 'example.md'): ")
    md_file_path = os.path.join(OBSIDIAN_VAULT_PATH, md_file_name)
    
    # Check if the file exists
    if not os.path.exists(md_file_path):
        print(f"The file {md_file_name} does not exist in the Obsidian vault.")
        return

    # Create a folder in the content directory with the name of the markdown file (without extension)
    folder_name = os.path.splitext(md_file_name)[0]  # Remove file extension
    folder_path = os.path.join(CONTENT_PATH, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

    # Copy the markdown file to the new folder and rename it to index.md
    shutil.copy(md_file_path, os.path.join(folder_path, 'index.md'))
    print(f"Copied {md_file_name} as index.md to {folder_path}")

    # Copy the featured image (featured.jpg) to the folder
    featured_image_path = os.path.join(OBSIDIAN_IMAGE_PATH, 'featured.jpg')
    if os.path.exists(featured_image_path):
        shutil.copy(featured_image_path, os.path.join(folder_path, 'featured.jpg'))
        print(f"Copied featured.jpg to {folder_path}")
    else:
        print("featured.jpg not found in Obsidian image folder.")

def main():
    """Main function to deploy Hugo site and manage images."""
    git_add_commit_push()
    copy_images()
    update_thumbnail()
    process_obsidian_md()

    print("Script completed successfully!")

if __name__ == "__main__":
    main()
