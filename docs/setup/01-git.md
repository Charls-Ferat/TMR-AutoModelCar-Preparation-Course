# Git — Windows Setup

Git is used to download the course repository and work with your team's code.

## 1. Install Git

### Option A — PowerShell / Windows Terminal

Open **PowerShell** and run:

```powershell
winget install --id Git.Git -e --source winget
```

If Windows asks for permission, allow the installation.

### Option B — Installer

Download **Git for Windows** from the official Git website and run the installer.

For the installation options, the default settings are fine for this course.

---

## 2. Restart your terminal

Close PowerShell/CMD and open it again.

---

## 3. Verify Git

Run:

```powershell
git --version
```

You should see something similar to:

```text
git version 2.x.x
```

The exact version is not important.

Also verify that Git is available:

```powershell
where.exe git
```

You should see a path containing something similar to:

```text
C:\Program Files\Git\cmd\git.exe
```

---

## 4. Configure your Git identity

Use the name and email you want associated with your commits:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Check the configuration:

```powershell
git config --global --list
```

---

## Done

Git is ready.

You can now clone the course repository with:

```powershell
git clone https://github.com/Charls-Ferat/TMR-AutoModelCar-Preparation-Course.git
```
