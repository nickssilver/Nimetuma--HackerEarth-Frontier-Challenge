# Public repo for the Repository link field

HackerEarth asks for a GitHub or GitLab URL. `gh` is not installed on this machine, so do this in Git Bash after you have a GitHub account logged into the website.

```bash
cd "/c/Users/workstation/Desktop/Development/Self/Frontier Engineering/nimetuma"
git init
git add .
git commit -m "Nimetuma: till-first agent for the micro1 Frontier Engineering Challenge"
```

On github.com click **New repository**, name it `nimetuma`, public, do not add a README.

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USER/nimetuma.git
git push -u origin main
```

Paste `https://github.com/YOUR_USER/nimetuma` into the HackerEarth repository field.
