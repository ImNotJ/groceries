import os
import subprocess
from datetime import datetime

# Define the repository path
repo_path = r'C:\Users\Administrator\groceries\grocery_prices'

# Define the commit message
commit_message = f'Automated commit on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

# Change to the repository directory
os.chdir(repo_path)

# Add all changes
subprocess.run(['git', 'add', '.'])

# Commit the changes
subprocess.run(['git', 'commit', '-m', commit_message])

# Push the changes
subprocess.run(['git', 'push'])
