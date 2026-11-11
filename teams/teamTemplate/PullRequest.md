# Team Contribution Guide #

Follow these steps to add your team's projects to this repository.

## 1. Clone the repository ##

If you haven't cloned the repository yet:

```bash
git clone <repository-url>
cd TMR-AutoModelCar-Preparation
```

## 2. Create your own branch ##

Before making any changes, create a branch for your team. Do not work directly on main.

```bash
git checkout main
git pull
git checkout -b team/your-team-name
```


For example:

```bash
git checkout -b team/team1
```

### 3. Create your team folder ###

Inside the teams/ directory, create a folder with your team's name.

Your projects must be stored inside this folder.

The repository structure should look like this:

```text
TMR-AutoModelCar-Preparation/
│
├── common/
├── docs/
├── teams/
│   ├── teamTemplate/
│   ├── team1/
│   │   ├── project1/
│   │   └── project2/
│   └── team2/
│       └── project1/
│
├── week1_techstack_intro/
├── week2_intro_ml/
├── week3_steering_model/
└── README.md
```

## 4. Commit and push your changes ##

Once you have added your projects, save your changes to Git:

```bash
git add .
git commit -m "Add projects for team1"
git push -u origin team/your-team-name
```

Replace team1 with your actual team name.

## 5. Create a Pull Request (PR) ##
1. Go to the repository on GitHub.
2. You should see an option to Compare & pull request for your recently pushed branch. Click it.
3. Make sure the base branch is main and the compare branch is your team's branch.
4. Add a short title and description explaining what your team has added.
5. Click Create pull request.

## 6. Wait for review and merging ##

Once your Pull Request is created, I will review your changes.

If everything looks good, I will merge your Pull Request into main, and your team's projects will become part of the main repository.

### Important: ###

* Each team must work on its own branch.
* Each team must store its work inside teams/your-team-name/.
* Do not push directly to main.
* Do not modify other teams' folders.
* Only the repository owner will merge Pull Requests.
