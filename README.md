# MLOps from Zero — the labs

Hands-on labs for the **MLOps from Zero** video course. Each video teaches the *why* and shows *how it
looked when it worked*. Each lab here is the *doing*: a short, copy-paste checklist you run on your own
machine, with the expected output under every command.

[![Labs verified](https://github.com/kovaliovsg/mlops-from-zero/actions/workflows/verify-labs.yml/badge.svg)](https://github.com/kovaliovsg/mlops-from-zero/actions/workflows/verify-labs.yml)

**Every lab is re-run automatically once a month by the pipeline above.** If a tool changes a link, a
version or a flag, the badge turns red, the lab gets fixed, and the video stays untouched. The date at
the top of each lab says when it was last verified.

## Labs

| Lab | For the video | What you build | Time |
|---|---|---|---|
| [Spot the drift](lab-what-is-mlops/) | What is MLOps? | Name the two kinds of drift, then watch a model drift in one command | 15 min |
| [The first brick](lab-python-for-mlops/) | Python for MLOps | Python, pandas, one dataset, ten rows | 15 min |
| [A model in a box](lab-docker/) | Docker | A real scikit-learn model served by FastAPI, built into a Docker image, run as a container | 30 min |

More labs are added as the course grows. **Fork this repository**: your fork becomes the public,
end-to-end project that the course keeps telling you to build.

## How to use a lab

1. Open the lab folder and read its `README.md` top to bottom once.
2. Run the numbered steps. Compare what you see with the **expected output** under each command.
3. The **Checkpoint** is the one command that proves it worked.
4. Something different on your machine? Check **If it breaks** at the end of the lab, then
   [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) with the step number and the
   exact output.

## No install at all

Click **Code → Codespaces → Create codespace** on this repository. The dev container has Python, pip and
Docker ready. Every lab runs inside it unchanged.

## License

MIT — use the code however you like. The videos are © their author.
