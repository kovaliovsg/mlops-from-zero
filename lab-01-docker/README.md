# Lab 1 · A model in a box

**Last verified:** 2026-10-04 · Docker Desktop 4.x (engine 29.8) · Python 3.12 · scikit-learn 1.9.1 · Windows 11

**Goal:** by the end, a real machine learning model answers questions from inside a Docker container on
your machine, and you have built the image yourself. This is the exact demo from the video, so you can
compare every output with what you saw.

**You need:** 30 minutes, a terminal, and Docker Desktop. The three files are in this folder:
`app.py` (the model behind a web address), `requirements.txt` (the ingredients), `Dockerfile` (the recipe).

## Steps

### 1. Install Docker Desktop and prove it works

Download Docker Desktop for your operating system from https://www.docker.com/products/docker-desktop/
and install it. On Windows it needs WSL 2; the installer sets it up and may ask for a reboot.

Start Docker Desktop, wait for the whale icon to stop animating, then in a terminal:

```bash
docker run --rm hello-world
```

Expected output contains:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 2. Get the lab files

Either clone this repository or download the three files into a folder called `flower-api`:

```bash
git clone https://github.com/kovaliovsg/mlops-from-zero.git
cd mlops-from-zero/lab-01-docker
```

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

The first build downloads the base image and installs the libraries; expect **about 40–60 seconds**.
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

### 7. See it, stop it

```bash
docker ps
```

Expected output: one row, image `flower-api`, status `Up ...`, ports `0.0.0.0:8000->8000/tcp`.

```bash
docker stop flower
docker rm flower
```

## Checkpoint

Step 6 returned `{"flower":"setosa"}` from a container you built yourself. That model now runs the same
on any machine with Docker: the whole kitchen travels with it.

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

Commit the three files plus a `NOTES.md` with your two curl outputs to your fork under `lab-01-docker/`.
