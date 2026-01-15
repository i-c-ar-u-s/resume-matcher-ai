---
description: Steps to publish the local project to a new GitHub repository
---

This workflow will guide you through committing your changes and pushing your code to a new GitHub repository.

# Step 1: Check Git Status and Commit
First, we need to ensure all your files are tracked and committed.

1. Check the status of your files:
   ```powershell
   git status
   ```

2. Add all files to the staging area:
   // turbo
   ```powershell
   git add .
   ```

3. Commit the changes:
   Make sure to include a meaningful message.
   ```powershell
   git commit -m "Initial commit of Resume Matcher App"
   ```

# Step 2: Create Repository on GitHub
Since the GitHub CLI (`gh`) is not installed, you'll need to create the repository manually.

1. Open your browser and go to: https://github.com/new
2. Enter a **Repository name** (e.g., `resume-matcher-ai`).
3. Choose **Public** or **Private**.
4. **Do not** initialize with README, .gitignore, or License (since we already have them locally).
5. Click **Create repository**.

# Step 3: Link and Push
Once created, GitHub will show you a "Quick setup" page. Look for the section **"...or push an existing repository from the command line"**.

1. Copy the commands shown on GitHub. They will look similar to this (replace `YOUR-USERNAME` with your actual username):
   ```powershell
   git remote add origin https://github.com/YOUR-USERNAME/resume-matcher-ai.git
   git branch -M main
   git push -u origin main
   ```

2. Run those commands in your terminal. 

   You can use the command below to add the remote (UPDATE THE URL FIRST!):
   ```powershell
   # REPLACE THE URL BELOW WITH YOUR REPO URL
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

   Then rename the branch to main (if not already):
   // turbo
   ```powershell
   git branch -M main
   ```

   Finally, push your code:
   ```powershell
   git push -u origin main
   ```

# Verification
After pushing, refresh your GitHub repository page to see your files!
