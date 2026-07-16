---
title: "Lab 01 — Environment Setup"
layout: single
---

**Key concepts and tools**
- `git`, `git clone`, `git add`, `git commit`, `git push`, `git pull`, `git log`
- SSH key authentication (SCC and laptop)
- GitHub as a shared remote — push from one machine, pull on another
- `conda`, `conda env create -f`, `.condarc`
- `module load miniconda`, `conda activate`
- `NXF_SYNTAX_PARSER=v2` — strict Nextflow syntax parser required for static typing
- SCC OnDemand, VSCode on a compute node
- HPC concepts: head node vs. compute node, home directory vs. project directory

---

This lab covers the foundational tooling used throughout the semester. You will configure your SCC account, set up GitHub SSH keys on both the SCC and your laptop, and redirect your conda package storage to `/projectnb/bf528/students/<username>` to avoid filling up your home directory quota. You will install the required VSCode extensions and create the `nextflow_latest` conda environment (Nextflow 26.04) — this environment will be activated at the start of every subsequent lab.

The git activity demonstrates the core mental model: GitHub is a shared remote, not a copy of your code. You push commits from one machine so another machine can pull them. You will make a change on the SCC, push it to GitHub, clone the repo on your laptop, then push a second change from the laptop and pull it back on the SCC.

## Setup checklist

- [ ] Familiarize yourself with SCC OnDemand and VSCode
- [ ] Set up an SSH key on the SCC and link it to GitHub
- [ ] Edit `~/.condarc` to redirect conda package storage:

```bash
envs_dirs:
    - /projectnb/bf528/students/<your_loginname>/.conda/envs
pkgs_dirs:
    - /projectnb/bf528/students/<your_loginname>/.conda/pkgs
```

- [ ] Create the course Nextflow environment and persist the syntax parser flag:

```bash
module load miniconda
conda env create -f envs/base_env.yml
conda activate nextflow_latest
echo 'export NXF_SYNTAX_PARSER=v2' >> ~/.bashrc
source ~/.bashrc
nextflow -h   # confirm it installed correctly
```

- [ ] Accept the GitHub Classroom link and clone the repo onto the SCC
- [ ] Complete the two-machine git activity:
  - Edit `notes.md` on the SCC, commit, and push
  - Clone the repo on your laptop and confirm the commit arrived
  - Make a second change on the laptop, commit, and push
  - Pull on the SCC and confirm both changes are present
- [ ] Submit your BU email and GitHub username via the course form

## Git — GitHub as a shared remote

```
  SCC ──push──▶ GitHub ◀──pull── Laptop
  SCC ◀──pull── GitHub ◀──push── Laptop
```

Neither your SCC copy nor your laptop copy is the authoritative one — GitHub is
the common origin that keeps both in sync. The everyday rule: **pull before you
start working, push when you are done**.

The basic local cycle is **edit → stage → commit**, then push to share:

```bash
git add notes.md          # stage specific files, not git add .
git commit -m "message"   # permanent snapshot with a label
git push                  # send commits to GitHub
git pull                  # receive commits from GitHub
git log --oneline         # view commit history
```

Staging individual files (`git add <filename>`) rather than `git add .` keeps
you in control of what goes into each commit.

## Resources

- [Nextflow Hello World training](https://training.nextflow.io/latest/hello_nextflow/) — complete on your own time
- [SCC SSH + GitHub 2FA guide](https://www.bu.edu/tech/support/research/system-usage/connect-scc/access-and-security/using-scc-with-github-2fa/#AUTH)
- [SCC conda setup](https://www.bu.edu/tech/support/research/software-and-programming/common-languages/python/python-software/miniconda-modules/#Conda%20Modules)
- [GitHub SSH key setup (local machine)](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
