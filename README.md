# MLOps from Zero — the labs

Hands-on labs for the **MLOps from Zero** video course. Each video teaches the *why* and shows *how it
looked when it worked*. Each lab here is the *doing*: a short, copy-paste checklist you run on your own
machine, with the expected output under every command.

**Before your first lab: [set up your machine](SETUP.md)** — VS Code, Python, Git and the rest, with where to
get each one and the install choices that matter. Every lab runs locally in VS Code.

**[MLOps from Zero](https://www.youtube.com/playlist?list=PLKblUEvSYoDc)** — the video course these labs belong to, every lesson in order (YouTube playlist).

<a href="https://www.youtube.com/playlist?list=PLKblUEvSYoDc"><img src="assets/course-mlops-from-zero.jpg" width="480" alt="MLOps from Zero - the video course for these labs (YouTube playlist)"></a>

**[Run a lab in VS Code](https://youtu.be/g1SpgAq6Zqc)** — how to set up your machine and run any lab, recorded step by step (YouTube video).

<a href="https://youtu.be/g1SpgAq6Zqc"><img src="assets/video-run-a-lab-in-vs-code.jpg" width="480" alt="Run a lab in VS Code - how to set up and run a lab (YouTube video)"></a>

[![Labs verified](https://github.com/kovaliovsg/mlops-from-zero/actions/workflows/verify-labs.yml/badge.svg)](https://github.com/kovaliovsg/mlops-from-zero/actions/workflows/verify-labs.yml)

**Every lab is re-run automatically once a month by the pipeline above.** If a tool changes a link, a
version or a flag, the badge turns red, the lab gets fixed, and the video stays untouched. The date at
the top of each lab says when it was last verified.

## Labs

| Lab | For the video | What you build | Time |
|---|---|---|---|
| [Spot the drift](lab-what-is-mlops/) | What is MLOps? (after Part 3) | Name the two kinds of drift, then watch a model drift in one command | 15 min |
| [Stand up the prep-forecast repo](lab-python-for-mlops/) | Python for MLOps (after Part 7) | The running project's first brick: a locked environment, three years of order books with planted mistakes, a notebook turned into a tested command | 35 min |
| [A model in a box](lab-docker/) | Docker | A real scikit-learn model served by FastAPI, built into a Docker image, run as a container | 30 min |

More labs are added as the course grows. **Fork this repository**: your fork becomes the public,
end-to-end project that the course keeps telling you to build.

## How to use a lab

1. Set up your machine once ([SETUP.md](SETUP.md)), then open the lab's folder in VS Code and read its
   `README.md` top to bottom once.
2. Run the numbered steps. Compare what you see with the **expected output** under each command.
3. The **Checkpoint** is the one command that proves it worked.
4. Something different on your machine? Check **If it breaks** at the end of the lab, then
   [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) with the step number and the
   exact output.

## License

MIT — use the code however you like. The videos are © their author.
