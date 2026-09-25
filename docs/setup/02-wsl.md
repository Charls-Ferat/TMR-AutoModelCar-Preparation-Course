# WSL 2 + Ubuntu 24.04 — Windows Setup

WSL lets us run Ubuntu/Linux tools directly inside Windows.

For this course, use:

* **WSL 2**
* **Ubuntu 24.04 LTS**

## 1. Open PowerShell as Administrator

Open the Start menu, search for **PowerShell**, right-click it, and select:

**Run as administrator**

---

## 2. Install WSL and Ubuntu 24.04

Run:

```powershell
wsl --install -d Ubuntu-24.04
```

If Windows asks you to restart, restart the computer.

After restarting, open Ubuntu from the Start menu.

The first launch may take a little while.

---

## 3. Create your Linux account

Ubuntu will ask you to create:

* a username
* a password

This is your **Linux/Ubuntu account**.

> When typing your password in Linux, nothing will appear on screen. This is normal.

---

## 4. Verify that WSL is using version 2

Open **PowerShell**:

```powershell
wsl --list --verbose
```

You should see something similar to:

```text
  NAME            STATE           VERSION
* Ubuntu-24.04    Running         2
```

The important part is:

```text
VERSION 2
```

---

## 5. Verify Ubuntu

Open Ubuntu and run:

```bash
lsb_release -a
```

You should see Ubuntu 24.04.

You can also run:

```bash
uname -a
```

---

## 6. Update Ubuntu

Inside **Ubuntu/WSL**, run:

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 7. Update WSL

Back in **PowerShell**, run:

```powershell
wsl --update
```

Then:

```powershell
wsl --status
```

---

## Useful commands

### Open Ubuntu from PowerShell

```powershell
wsl
```

### Shut down WSL

```powershell
wsl --shutdown
```

### See installed distributions

```powershell
wsl --list --verbose
```

---

## Done

You should now have:

```text
Windows
└── WSL 2
    └── Ubuntu 24.04
```

This Ubuntu environment will be used for ROS 2 and GPU/ML work.
