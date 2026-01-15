---
description: Steps to deploy the app to Streamlit Community Cloud
---

This workflow will guide you through deploying your Streamlit app to the web so anyone can access it.

# Step 1: Sign up for Streamlit Cloud
1.  Go to **[share.streamlit.io](https://share.streamlit.io/)**.
2.  Click **"Continue with GitHub"**.
3.  Authorize Streamlit to access your GitHub repositories.

# Step 2: Deploy the App
1.  Once logged in, click the **"New app"** button (top right).
2.  Select **"Use existing repo"**.
3.  In the "Repository" field, select your repo:
    `i-c-ar-u-s/resume-matcher-ai`
4.  (Optional) Changing the "App URL" to something custom if you want.
5.  **Main file path**: Ensure it says `app.py`.
6.  Click **"Deploy!"**.

# Step 3: Configure Secrets (Crucial!)
Your app will crash initially because it doesn't have the API Key. We need to add it securely.

1.  On your deployed app screen (it might show an error), look for the **"Manage app"** menu (bottom right corner usually, or the three dots in top right -> Settings).
2.  Alternatively, go to your App Dashboard, click the three dots next to your app, and select **"Settings"**.
3.  Click on the **"Secrets"** tab.
4.  Paste your API key in the following TOML format:

    ```toml
    GOOGLE_API_KEY = "your_actual_api_key_here"
    ```
    *(Copy the key from your local `.env` file)*

5.  Click **"Save"**.

# Step 4: Reboot
The app might auto-reload. If not, go to the top-right menu via the three dots and click **"Reboot"**.

🎉 **Done!** You now have a public link to share with anyone.
