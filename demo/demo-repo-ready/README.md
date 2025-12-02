# AutoPR Demo (ready-to-push)

This folder contains a minimal demo repository you can copy to GitHub to showcase AutoPR in action.

How to use
1. Copy the entire `demo/demo-repo-ready` folder to a new GitHub repository (or push this folder as a new repo).
2. Update `.github/workflows/auto-pr-demo.yml` and set the installation line for AutoPR to point to your published repo or your AutoPR repo URL. Example:

```yaml
# pip install git+https://github.com/<YOUR_USER>/AutoPR.git
```

3. Create a Pull Request in the demo repo or push a branch — the workflow will run tests, call the AutoPR review runner and post a demo comment.

What the demo contains
- sample Python project with tests (src/sample.py + tests)
- GitHub Actions workflow to run tests and call AutoPR
- Example PR diff lives in demo/prs (for local demonstrations)
