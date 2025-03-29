#### Learn everything you need to use Git and GitHub to track and store the changes of your source code.

[Link](https://www.udemy.com/course/git-for-beginners-course)

Notes 

- What is a Version Control System (VCS)?

    - A version control system (VCS) is a software tool that helps software developers manage changes to source code over time. It allows multiple developers to work on the same project simultaneously without overwriting each other's changes. VCS keeps track of every modification made to the code, enabling developers to revert to previous versions if needed.
    - VCS also provides a history of changes, making it easier to understand how the code has evolved over time. It is an essential tool for collaborative software development, ensuring that all team members can work together efficiently and effectively.

- Different Types of Version Control Systems

    - Local Version Control System (LVCS): A local version control system keeps track of changes to files on a single computer. It is simple and easy to use but lacks collaboration features. Examples include RCS (Revision Control System) and SCCS (Source Code Control System).

    - Centralized Version Control System (CVCS): A centralized version control system stores the code in a central repository, allowing multiple developers to work on the same project. It provides better collaboration features than LVCS but can be slower and less reliable. Examples include CVS (Concurrent Versions System) and Subversion (SVN).

    - Distributed Version Control System (DVCS): A distributed version control system allows developers to work on their own copies of the code, making it easier to collaborate and manage changes. Each developer has a complete copy of the repository, enabling offline work and faster operations. Examples include Git, Mercurial, and Bazaar.
    - Git is the most popular DVCS and is widely used in open-source and commercial projects. It provides powerful branching and merging capabilities, making it ideal for collaborative software development.

- Understanding the origin of Git

    - Git was created by Linus Torvalds in 2005 to manage the development of the Linux kernel. It was designed to be fast, efficient, and reliable, with a focus on supporting distributed development. Git's unique architecture allows for easy branching and merging, making it a popular choice for both open-source and commercial projects.
    - Git's design was influenced by the need for a version control system that could handle large projects with many contributors. It was built to be fast and efficient, with a focus on supporting distributed development. Git's unique architecture allows for easy branching and merging, making it a popular choice for both open-source and commercial projects.

- Install Git

    - To install Git on Windows, follow these steps:
        1. Download the Git installer from the official website: https://git-scm.com/download/win
        2. Run the installer and follow the prompts to complete the installation.
        3. During installation, you can choose to add Git to your system PATH for easier access from the command line.
        4. After installation, open a command prompt or Git Bash and type `git --version` to verify that Git is installed correctly.

    - To install Git on macOS, follow these steps:
        1. Open the Terminal application.
        2. Type `git --version` and press Enter. If Git is not installed, you will be prompted to install it.
        3. Follow the prompts to complete the installation.

    - To install Git on Linux, follow these steps:
        1. Open a terminal window.
        2. Use your package manager to install Git. For example, on Ubuntu, you can use the following command:
            ```bash
            sudo apt-get install git
            ```
        3. After installation, type `git --version` to verify that Git is installed correctly.
        4. You can also install Git from source by downloading the source code from the official website and following the instructions in the INSTALL file.

- Configure Username and Password:

    - Use the following commands:

        `git config --global user.name "Your Name"`

        `git config --global user.email "Your Email"`

    - To see all the configurations:

        `git config --list` or `git config -l --show-origin`, here -l is for list and --show-origin is to show the file where the configuration is stored.

- Working with Local Repositories:

    - To create a new local repository, use the following command:

        `git init <repository-name>`

    - To clone an existing repository, use the following command:

        `git clone <repository-url>`

    - To check the status of your local repository, use the following command:

        `git status`

    - To add files to the staging area, use the following command:

        `git add <file-name>` or `git add .` to add all files.

    - To commit changes to the local repository, use the following command:

        `git commit -m "Your commit message"`

    - To view the commit history, use the following command:

        `git log`

    - To view a specific commit, use the following command:

        `git show <commit-hash>`

    - To revert to a previous commit, use the following command:

        `git checkout <commit-hash>`, no need to type the entire hash, just the first 7 characters are enough.

    - To delete a file from the staging area, use the following command:

        `git rm <file-name>`

    - To rename a file in the staging area, use the following command:

        `git mv <old-file-name> <new-file-name>`

    - To view the differences between the working directory and the staging area, use the following command:
        `git diff`

    - To view the differences between the staging area and the last commit, use the following command:
        `git diff --cached`

    - To view the differences between two commits, use the following command:
        `git diff <commit-hash-1> <commit-hash-2>`

    - To view the differences between the working directory and a specific commit, use the following command:
        `git diff <commit-hash>`

    - To view the differences between two branches, use the following command:
        `git diff <branch-1> <branch-2>`

    - To push changes to a remote repository, use the following command:

        `git push <remote-name> <branch-name>`

    - To pull changes from a remote repository, use the following command:

        `git pull <remote-name> <branch-name>`

    - To fetch changes from a remote repository without merging, use the following command:

        `git fetch <remote-name>`

    - To create a new branch, use the following command:

        `git branch <branch-name>`

    - Log in one line

        `git log --pretty=oneline`, here --pretty=oneline is used to show the log in one line.

    
- Ignoring Files:

    - To ignore files in a Git repository, create a file named `.gitignore` in the root directory of your repository. Add the names of the files or directories you want to ignore, one per line. For example:

        ```
        # Ignore all .log files
        *.log

        # Ignore the node_modules directory
        node_modules/
        ```

    - Save the `.gitignore` file and commit it to your repository. Git will now ignore the specified files and directories.
    - To check which files are being ignored, use the following command:

        `git check-ignore -v <file-name>`


- Branching and Merging Code

    - Branching is a powerful feature of Git that allows you to create separate lines of development within a single repository. This is useful for working on new features or bug fixes without affecting the main codebase.

    - To create a new branch, use the following command:

        `git branch <branch-name>`

    - To switch to a different branch, use the following command:

        `git checkout <branch-name>`

    - To merge changes from one branch into another, first switch to the target branch and then use the following command:

        `git merge <source-branch-name>`

    - To delete a branch, use the following command:

        `git branch -d <branch-name>`

    - To view all branches in your repository, use the following command:

        `git branch`

    - To view all branches, including remote branches, use the following command:

        `git branch -a`

    - To view the commit history of a specific branch, use the following command:

        `git log <branch-name>`

- Pushing to a remote repository

    - To push changes to a remote repository, use the following command:

        `git push <remote-name> <branch-name>`

        `git push -u origin <branch-name>`, here -u is used to set the upstream branch, so you don't have to specify the remote and branch name every time you push.

    - To pull changes from a remote repository, use the following command:

        `git pull <remote-name> <branch-name>`

    - To fetch changes from a remote repository without merging, use the following command:

        `git fetch <remote-name>`

    - To view the remote repositories associated with your local repository, use the following command:

        `git remote -v`

    - To add a new remote repository, use the following command:

        `git remote add <remote-name> <repository-url>`

    - To remove a remote repository, use the following command:

        `git remote remove <remote-name>`

- Creating and Merging Pull Requests

    - A pull request is a way to propose changes to a repository. It allows you to request that your changes be merged into another branch or repository.

    - To create a pull request, follow these steps:

        1. Push your changes to a remote branch.
        2. Go to the repository on GitHub or GitLab.
        3. Click on the "Pull Requests" tab.
        4. Click on the "New Pull Request" button.
        5. Select the base branch and the compare branch.
        6. Add a title and description for your pull request.
        7. Click on the "Create Pull Request" button.

    - To merge a pull request, follow these steps:

        1. Go to the pull request on GitHub or GitLab.
        2. Review the changes and comments.
        3. Click on the "Merge Pull Request" button.
        4. Confirm the merge.

    - To close a pull request without merging, click on the "Close Pull Request" button.
    - To comment on a pull request, go to the pull request and add your comments in the comment box.

    - To resolve merge conflicts, follow these steps:

        1. Go to the pull request on GitHub or GitLab.
        2. Click on the "Resolve Conflicts" button.
        3. Edit the conflicting files to resolve the conflicts.
        4. Click on the "Mark as Resolved" button.
        5. Click on the "Commit Merge" button.
        6. Click on the "Merge Pull Request" button.

        7. Confirm the merge.

    - To view the commit history of a pull request, go to the pull request and click on the "Commits" tab.
    - To view the files changed in a pull request, go to the pull request and click on the "Files Changed" tab.

    - To view the comments on a pull request, go to the pull request and click on the "Conversation" tab.

    - To view the status of a pull request, go to the pull request and look for the "Status" section.

    - To view the checks on a pull request, go to the pull request and click on the "Checks" tab.

- Forking a repository

    
    - Forking a repository is a way to create a personal copy of someone else's repository. This allows you to make changes to the code without affecting the original repository.

    - To fork a repository, follow these steps:

        1. Go to the repository on GitHub or GitLab.
        2. Click on the "Fork" button.
        3. Select your account or organization where you want to fork the repository.
        4. Wait for the forking process to complete.

    - To clone your forked repository, use the following command:

        `git clone <repository-url>`

    - To push changes to your forked repository, use the following command:

        `git push origin <branch-name>`

    - To create a pull request from your forked repository to the original repository, follow these steps:

        1. Go to your forked repository on GitHub or GitLab.
        2. Click on the "Pull Requests" tab.
        3. Click on the "New Pull Request" button.
        4. Select the base branch and the compare branch.
        5. Add a title and description for your pull request.
        6. Click on the "Create Pull Request" button.

    - To view the commit history of your forked repository, use the following command:

        `git log`

    - To view the branches in your forked repository, use the following command:

        `git branch`

    - To view the remote repositories associated with your forked repository, use the following command:

        `git remote -v`

    - To add a new remote repository to your forked repository, use the following command:

        `git remote add <remote-name> <repository-url>`

    - To remove a remote repository from your forked repository, use the following command:

        `git remote remove <remote-name>`
