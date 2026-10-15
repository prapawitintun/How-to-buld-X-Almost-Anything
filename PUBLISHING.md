# Publishing this starter repository

Destination for the currently connected account: `hellolayermind/build-for-humanity`. This is a proposed new repository, not a verified existing destination.

With an authenticated GitHub CLI, create a new public repository and push the current project:

```bash
git init -b main
git add .
git commit -m "Add Build for Humanity learning catalog and six starter labs"
gh repo create hellolayermind/build-for-humanity --public --source=. --remote=origin --push --description "Build technology from software and AI to CAD, fabrication, robotics, materials, and community systems."
```

These commands assume Git and the GitHub CLI are installed, your Git author identity is configured, and you are authenticated as an account permitted to create repositories under `hellolayermind`.

If that name already exists, inspect the existing repository before pushing or adding files. Never force-push an existing project.

Alternatively, create an empty GitHub repository, extract this archive, and upload the files inside its project directory. Use the README as the landing page. GitHub Pages hosting is optional and is not configured by this package.
