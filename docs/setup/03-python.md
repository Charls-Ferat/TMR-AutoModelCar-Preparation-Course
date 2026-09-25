# Python 3 + Virtual Environments — Windows Setup

Python will be used for machine learning and other course exercises.

A **virtual environment** keeps each project's Python packages separate.

## 1. Install Python 3

Open **PowerShell** and check whether Python is already installed:

```powershell
python --version
```

Also try:

```powershell
py --version
```

If one of these works and reports Python 3, you can use that installation.

If Python is not installed, install it from the official Python website.

After installation, close and reopen PowerShell.

---

## 2. Verify Python

In **PowerShell**:

```powershell
python --version
```

You should see something similar to:

```text
Python 3.x.x
```

Also check:

```powershell
python -m pip --version
```

---

# PowerShell

## 3. Create a project

For example:

```powershell
mkdir python-test
cd python-test
```

---

## 4. Create a virtual environment

Run:

```powershell
python -m venv .venv
```

This creates:

```text
python-test/
└── .venv/
```

---

## 5. Activate the environment

In **PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

Your terminal should now show something similar to:

```text
(.venv) PS C:\...\python-test>
```

---

## 6. Verify the environment

Run:

```powershell
python --version
```

Then:

```powershell
python -m pip --version
```

The paths should point into `.venv`.

---

## 7. Install a package

For example:

```powershell
python -m pip install numpy
```

Check it:

```powershell
python -c "import numpy; print(numpy.__version__)"
```

---

## 8. Deactivate

When you are finished:

```powershell
deactivate
```

---

# CMD

The same virtual environment can be used from **Command Prompt**.

Open **CMD** and navigate to the project:

```cmd
cd path\to\python-test
```

Create the environment if you have not already:

```cmd
python -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate.bat
```

You should see:

```text
(.venv) C:\...\python-test>
```

Verify:

```cmd
python --version
```

Deactivate:

```cmd
deactivate
```

---

## Important

Every time you work on a Python project, activate its virtual environment first.

### PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### CMD

```cmd
.venv\Scripts\activate.bat
```

Then use:

```powershell
python
python -m pip install <package>
```

Using `python -m pip` is preferred because it makes sure you are using the `pip` belonging to the active Python environment.

---

## If PowerShell blocks activation

If PowerShell reports that script execution is disabled, run PowerShell normally and execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Done

You should now be able to:

1. Install Python 3.
2. Create a `.venv`.
3. Activate it from PowerShell.
4. Activate it from CMD.
5. Install Python packages inside it.
