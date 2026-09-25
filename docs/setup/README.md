# TMR AutoModelCar Preparation Course — Setup Guides

These guides prepare your computer for the tools we will use during the course.

## Recommended order

Follow the guides in this order:

1. **Git** → `01-git.md`
2. **WSL 2 + Ubuntu 24.04** → `02-wsl.md`
3. **Python + virtual environments** → `03-python-venv.md`
4. **PyTorch + CUDA** → `04-pytorch-cuda-wsl.md`
5. **ROS 2 Jazzy** → `05-ros2-jazzy-wsl.md`

It is recommended to complete each guide and verify that everything works before moving to the next one.

---

## Windows vs WSL

There is an important distinction between the environments used in these guides.

### Python

For the general Python setup, follow:

**`03-python-venv.md`**

This guide uses **Python on Windows**.

You will learn how to create and use a Python virtual environment from both:

* PowerShell
* CMD

### PyTorch + CUDA

For machine learning and GPU work, follow:

**`04-pytorch-cuda-wsl.md`**

This setup uses **Python and PyTorch inside WSL/Ubuntu**, not the Windows Python installation.

The reason is that the ML environment used later in the course will run in Linux/WSL.

### ROS 2

ROS 2 is also installed and used **inside WSL/Ubuntu**.

Follow:

**`05-ros2-jazzy-wsl.md`**

---

## Using your IDE

You do **not** have to do all of your work directly from the Ubuntu terminal.

You can use an IDE/editor that supports working with WSL.

For example, if you use Visual Studio Code, you can open a project inside WSL and work with:

* Python
* PyTorch
* ROS 2
* Git
* Linux tools

directly from the IDE.

The important thing is to know **where your code is running**.

For example:

```text
Windows
├── PowerShell / CMD
│   └── Windows Python
│
└── WSL 2
    └── Ubuntu 24.04
        ├── PyTorch + CUDA
        └── ROS 2 Jazzy
```

When working on PyTorch or ROS 2, make sure your IDE is connected to **WSL**, rather than running the code with the Windows Python installation.

---

## A useful rule

When a guide says:

> **PowerShell / Windows**

run the command in Windows.

When it says:

> **WSL / Ubuntu**

run the command inside your Ubuntu terminal.

Do not assume that a command works in both environments.

---

## Recommended setup

By the end of these guides, your computer should have:

```text
Windows
│
├── Git
├── Python 3
│   └── Windows virtual environments
│
└── WSL 2
    └── Ubuntu 24.04
        ├── Python 3
        ├── PyTorch
        ├── CUDA / NVIDIA GPU support
        └── ROS 2 Jazzy
```

The Windows and WSL Python environments are **separate**.

You may have Python installed in both places. This is intentional.

---

## If something does not work

Don't immediately reinstall everything.

First check:

1. **Am I running the command in Windows or WSL?**
2. **Is my virtual environment activated?**
3. **Am I using the correct Python installation?**
4. **Did I follow the verification step in the guide?**
5. **Is the error actually related to the current guide?**

If you get stuck, keep the exact error message. It will make troubleshooting much easier.

---

## Before starting the course

You should be able to successfully verify:

* `git --version` in Windows
* WSL 2 with Ubuntu 24.04
* Python 3 in Windows
* A Windows Python virtual environment
* `nvidia-smi` inside WSL (if you have an NVIDIA GPU)
* `torch.cuda.is_available()` for GPU-enabled PyTorch
* ROS 2 Jazzy
* A ROS 2 publisher and subscriber communicating

Once these are working, your computer is ready for the development environment used in the course.
