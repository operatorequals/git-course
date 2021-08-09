# OperatorEquals' Sandbox Git Course!

## Preface
This Git course is an ongoing project containing use cases that I've met (and still meet) while working in the IT industry as
*IT Security Consultant* (e.g Code Auditor) and *IT Security Engineer* (SecDevOps - Infrascode guy and CI/CD guy),
as well as an independent software and security tool *Developer*.

I struggled a lot learning Git (you can see my ongoing struggle in my [Public Repos](https://github.com/operatorequals?tab=repositories)), yet it amazes me.
The problem was always that as a newbie I never found a resource that actually helped me understand what I was doing, but only commands a guru wrote somewhere on
[StackExchange](https://stackexchange.com/) to someone having some problem that seemed close to mine.

What really happened and I learned Git is that after years, I failed in so many different ways that something clicked on my head.
Unfortunately some of my failures were in Git repositories that I professionally maintained. And many of the failures were on the same scenarios:
* I put *EVERYTHING* in one single commit - someone needs to `git revert`
* I commited a *Super Importand Production Secret* - am I fired?

And after a million `git rebase -i` and force-pushes (some of them in branches I wasn't supposed to push), I figured that if I had some sandboxed repositories that
recreated my problematic scenarios I would be able to fuck them up indefinitely and eventually succeed without spending hours on colleague Reviews and Q/A time.
And if also there was a way that these sandboxed repositories could automatically examine my commits and -even poorly- give me some feedback, I would learn
without asking about basics that I have missed, but make only targeted and well-educated questions!

I couldn't find such a resource anywhere on the Internet (very possible that I didn't search too well). So -when I felt mature enough- I made it!


## How to Use

##### Attention: DO NOT browse this repository if you are NOT looking for challenge **spoilers**

This course comes with some Git repositories with names of `challenge1.git`, `challenge2.git` ... `challengeN.git`, hosted on Heroku using the code of this repository (later on that).
To start a challenge you need to clone it. Then read its `README.md` and `git log` (mostly the commit that has a title starting with `[Objectives]`).

Example:
```bash
git clone https://git-interactive-course.herokuapp.com/challenge1.git
cd challenge1
cat README.md
git log
```

What you have to do to solve the challenge should be clear by then!

What is left is to create *a new branch*, do your magic and then `git push origin <yourbranch>` to get the feedback from the Git Course Server.
The Git Course Server checks each commit (message AND contents) for specific requirements, such as commit message conventions, expected code, file similarity,
and others. Every challenge has a dedicated script checking pushed commits, as each time the objectives are different and need to be checked in specific ways.

If a commit (or the whole diff) does not pass the tests, an informative message with the commit hash appears as a result of `git push` and the upstream changes
are discarded. You can `git push` your changes forever and check every part of your solution. There is no "final" push - it is no exam. It is a sandbox!

Finally, there is no scoring, no leaderboard and no logs of what you do! Learning sometimes takes suffering and frustration and watching people suffer or rewarding frustration points has never worked as a teaching experience for me.


## The Challenges
The implemented challenges up to now are:

### Challenge 1 - Commit Message conventions
This challenge asks the solver to write about 5 super-simple lines of Python code (as this is no coding course) and commit the changes using the commit
message convention already used in the repository. It is a warming up challenge, yet it shows the importance of adopting the style of something already present
before us, which is the case when joining software organisations.

```bash
git clone https://git-interactive-course.herokuapp.com/challenge1.git
```

### Challenge 2 - Atomic Commits
This challenge asks the solver to split an already existing commit to 2 commits. This involves rewriting history. The given commit is bloated in a sense that
contains changes that implement more than one feature, violating the principle of *1 thing per commit*. When maintaining big codebases, a change can always lead
to a bug - sometimes a Prod breaking one or a Security bug. Ensuring that the bug resides in exactly one (well documented on why it happened) commit is
essential in reverting the repository to a previous working state without side-affecting other useful changes.


```bash
git clone https://git-interactive-course.herokuapp.com/challenge2.git
```

### Challenge 3 - The Secret in the History
This challenge asks the solver completely remove a secret value commited in the Git repository. The secret has been added as a feature, and has been
followed by other commits, rendering it a bit low in commit history. This is a very common use cases that requires rewriting history. Solving such a
challenge does give great insight not only on correctly managing secrets in code, but also on how to undo changes long down in the `git log`.

```bash
git clone https://git-interactive-course.herokuapp.com/challenge3.git
```

### More to come...

## Run Locally
If you feel like hosting the whole project on your premises you can easily do so using Containers.
There are two Git repository connectivity options, the `http` and the `ssh`.
The `Makefile` residing in this repository will create a container image by just issuing `make image` - the `TYPE` parameter accepts both `ssh` and `http`(default),
and from there the sky is the limit!

You can go with `docker run ...` or even use Kubernetes and host it company-wide for a training session, or anything that runs containers basically.


## Feedback and *Dev-Mode*
This is an Open-Source Project hosted on Free services and under Public Domain. Any feedback on it, such as bugs on challenge checks or repositories,
recommendations for new challenges, typos and all else, are all welcome under the [*Issues* section of this repository](https://github.com/operatorequals/git-course/issues).
Also Pull Requests are very welcome and will be greatly appreciated!


## This Repository
Creating a Git course and explaining techniques and best-practices in a repository that does not use them itself does not make sense.
So this Git repository follows Git message conventions and does have atomic commits (as much as possible). Also, in case you go
*Dev-mode* you can ALWAYS find information on commit messages! Writing the commit message sometimes takes as much as the code
itself. Also, they are all writen with explaining to others (+ future self) everything that is getting done *and why* in mind.

## Implementation
The challenge feedback is solely based on the Git mechanism of [Server-Side hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks#_server_side_hooks). Specifically, `update` is used for branch-protection and `post-update` for the challenge checks.
The challenge checks are implemented in Python3 using [PyGit2](https://www.pygit2.org) to programmatically inspect Git objects (analyze commits, diffs, refs/branches, etc).

A small Python3 module is sloppily getting developed for generic commit checks ([gitcourselib.py](https://github.com/operatorequals/git-course/blob/master/generic/gitcourselib.py)) that could maybe be used independently.

Git Transports that are supported are `ssh` and `http`, implemented with basic OpenSSH with `git-shell` startup shell for `ssh`
and a custom Apache2 configuration for `http`. All parts of the implementation are Open-Source and available under `deploy/`.

## Donations
In case my work helped you, you can always buy me a beer or a liter of gas [through the Internet](https://www.buymeacoffee.com/operatorequals) or in case you meet me personally.
In the second case we can talk about privacy (during drinking the beer or driving somewhere), about the funny idea that
[Git resembles the Human Psychology](https://securosophy.com/2017/04/01/a-git-tutorial-of-human-psychology/), about self-organized communes
or anything you bring up :)

[![donation](https://cdn-images-1.medium.com/max/738/1*G95uyokAH4JC5Ppvx4LmoQ@2x.png)](https://www.buymeacoffee.com/operatorequals)
