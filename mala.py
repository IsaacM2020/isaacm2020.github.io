import os
import subprocess
from typing import Optional


class GitDeployer:
    def __init__(self, repo_path: str, public_folder: str):
        self.repo_path = repo_path
        self.public_folder = public_folder
        self.target_branch = "gh-pages"

    def run_command(self, command: list[str]) -> tuple[int, str, str]:
        """
        Run a shell command and return its exit code, stdout, and stderr
        """
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.repo_path
        )
        stdout, stderr = process.communicate()
        return (
            process.returncode,
            stdout.decode('utf-8').strip(),
            stderr.decode('utf-8').strip()
        )

    def deploy(self) -> bool:
        """
        Deploy the public folder to GitHub Pages
        """
        print(f"Deploying {self.public_folder} to GitHub Pages...")

        # Create temporary branch for deployment
        temp_branch = "gh-pages-deploy"

        try:
            # Split the subtree
            code, out, err = self.run_command([
                'git', 'subtree', 'split', '--prefix', self.public_folder,
                '-b', temp_branch
            ])
            if code != 0:
                raise Exception(f"Failed to create subtree: {err}")

            # Force push to gh-pages branch
            code, out, err = self.run_command([
                'git', 'push', 'origin', f'{temp_branch}:gh-pages',
                '--force'
            ])
            if code != 0:
                raise Exception(f"Failed to push to gh-pages: {err}")

            # Clean up - delete temporary branch
            code, out, err = self.run_command(['git', 'branch', '-D', temp_branch])
            if code != 0:
                print(f"Warning: Failed to delete temporary branch: {err}")

            print("Deployment successful!")
            return True

        except Exception as e:
            print(f"Error during deployment: {str(e)}")
            return False


def main():
    # Using raw string (r"") to handle Windows paths correctly
    REPO_PATH = r"C:\Users\isaac\isaacblogs"  # Windows path with raw string
    PUBLIC_FOLDER = "public"  # Your public folder name

    deployer = GitDeployer(REPO_PATH, PUBLIC_FOLDER)
    deployer.deploy()


if __name__ == "__main__":
    main()