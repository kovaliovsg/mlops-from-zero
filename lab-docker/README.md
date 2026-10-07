# Lab · A model in a box

**Last verified:** 2026-10-06 · Docker engine 29.8.2 · Python 3.12 (in the image) · scikit-learn 1.9.1 · Windows

**Goal:** by the end, a real machine learning model answers questions from inside a Docker container on
your machine, and you have built the image yourself. This is the exact demo from the video, so you can
compare every output with what you saw.

**You need:** 30 minutes, VS Code, Git and Docker Desktop — see [Set up your machine](../SETUP.md). Run every
command in the VS Code terminal. The files are in this folder: `app.py` (the model behind a web address),
`requirements.txt` (the ingredients), `Dockerfile` (the recipe) and `checkpoint.py` (the taste test).

**Cost:** free. Nothing runs in Azure.

## Steps

### 1. Install Docker Desktop and prove it works

Install Docker Desktop as described in [Docker Desktop](../SETUP.md#5-docker-desktop) on the setup page.

Start Docker Desktop, wait for the whale icon to stop animating, then in a terminal:

```bash
docker run --rm hello-world
```

Expected output contains:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 2. Open the lab

With the labs cloned once ([Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code), steps 1–2):

1. Press `Ctrl+K`, then `Ctrl+O` (or the **File** menu, **Open Folder**).
2. Go into `mlops-from-zero`, select the `lab-docker` folder and click **Select Folder**.
3. Open the terminal: `` Ctrl+Shift+` ``.

This lab needs **no** `.venv`: Python and the libraries live inside the image you are about to build.

### 3. Look at the recipe

```bash
cat Dockerfile
```

Expected output:

```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Six lines. Base layer, a folder to work in, the slow layer (libraries) first, your code last, how to serve.

### 4. Build the image

```bash
docker build -t flower-api .
```

The first build downloads the base image and installs the libraries; expect **about a minute** (more on a slow connection).
The output ends with:

```
 => exporting to image
 => => naming to docker.io/library/flower-api:latest
```

### 5. Run a container from it

```bash
docker run -d -p 8000:8000 --name flower flower-api
```

Expected output: one long hexadecimal id, for example `31488862b71073a4b2021412d19bd89c7f...`.
The `-p 8000:8000` part connects port 8000 on your machine to port 8000 inside the box.

### 6. Ask the model a question

On Windows PowerShell type `curl.exe`, not `curl` (there `curl` is another command with a different output).

```bash
curl "localhost:8000/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2"
```

Expected output:

```
{"flower":"setosa"}
```

Now a bigger flower:

```bash
curl "localhost:8000/predict?sepal_length=6.7&sepal_width=3.0&petal_length=5.2&petal_width=2.3"
```

Expected output:

```
{"flower":"virginica"}
```

Prefer a browser? Open http://localhost:8000/docs — FastAPI gives you a free test page.

### 7. The checkpoint

`checkpoint.py` asks the model both questions from **inside** the container, so it needs nothing on your
machine:

```bash
docker exec flower python checkpoint.py
```

Expected output:

```
small flower: setosa
big flower:   virginica
CHECKPOINT OK
```

### 8. See it, stop it

```bash
docker ps
```

Expected output: one row, image `flower-api`, status `Up ...`, ports `0.0.0.0:8000->8000/tcp`.

```bash
docker stop flower
docker rm flower
```

## Checkpoint

`CHECKPOINT OK` printed by a container you built yourself. That model now runs the same on any machine with
Docker: the whole kitchen travels with it.

## Stretch (optional)

1. Change `max_iter=500` to `max_iter=50` in `app.py`, then run `docker build -t flower-api .` again.
   Watch the output: the `RUN pip install` layer says **CACHED** and the build takes a few seconds. That
   is the lasagna trick from the video.
2. Run two containers from the same image on two ports (`-p 8001:8000` and `-p 8002:8000`). One image,
   many containers.

## If it breaks

- **`docker: command not found` right after installing:** open a *new* terminal; the installer changed
  PATH for new windows only.
- **`error during connect` / `cannot find the file specified` (Windows):** Docker Desktop is not running.
  Start it and wait for the whale icon to settle.
- **`pip install` fails inside the build because a version no longer exists:** the pins in
  `requirements.txt` are frozen to the verified date. Remove the `==x.y.z` parts, build again, and open an
  issue so this lab gets re-pinned.
- **Port 8000 is already in use:** run with `-p 8080:8000` and query `localhost:8080`.
- **The download page moved:** search "Docker Desktop download"; the product name has been stable since 2017.

## Hand in

Commit the three files plus a `NOTES.md` with your two curl outputs to your fork under `lab-docker/`.
