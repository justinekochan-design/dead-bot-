[README.md](https://github.com/user-attachments/files/23487218/README.md)
# DeadBot Demo — Ada Lovelace (SIMULATION)

This is a ready-to-upload GitHub repository for the **Interactive Flask DeadBot demo** simulating a **public historical figure** (Ada Lovelace).

## What you get
- `app.py` — Flask app (mock LLM mode, safe-by-default)
- `frontend.html` — small static page (app serves the main UI)
- `persona.json` — persona metadata and seed utterances (public-figure, fictionalized)
- `requirements.txt`

## How to use (GitHub Codespaces)
1. Create a new GitHub repository and upload these files (or upload the ZIP as the repo).
2. Open the repository in **GitHub Codespaces** (Code → Codespaces → Create codespace).
3. Once the Codespace is ready, open the terminal and run:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
4. Click the **port** notification in Codespaces to open the running app in a browser tab.
5. The UI is interactive: you can send messages and toggle **Simulate Dead** to test silence.

## Notes on safety & ethics
- This simulation uses a **public historical figure** and public facts. Replies are fictionalized and always prefixed with **[SIMULATION]**.
- **Do not** use private, non-consented data of living or deceased private individuals.
- For a live LLM integration (OpenAI / Azure OpenAI), add an API call replacing the mock logic — but ensure consent, moderation, and transparency before using real-person data.

## License
This demo is provided for educational use. Use responsibly.
