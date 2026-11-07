# IR2 Project — Setup & Usage

This repository contains the shared Information Retrieval (IR2) testbed and the implementation of **GPL (Generative Pseudo Labeling)** for unsupervised domain adaptation in dense retrieval.

## 1. Prerequisites

Before starting, install:

- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

**macOS:** Use Docker Desktop for Mac (Apple Silicon or Intel).

**Windows:** Use Docker Desktop with WSL2 enabled.

Make sure Docker Desktop is running before executing any commands.

## 2. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/fserracrespi/ir2_Project.git
cd ir2_Project
```

## 3. Build the Docker image

Run the following command from the project root:

```bash
docker compose build
```

This builds a Linux environment containing Python and the required project dependencies.

The first build may take several minutes. Subsequent builds reuse cached layers.

## 4. Verify the installation

Check the Python version:

```bash
docker compose run --rm ir2 python --version
```

Verify that PyTorch is installed correctly:

```bash
docker compose run --rm ir2 python -c "import torch; print(torch.__version__)"
```

If both commands succeed, the environment is ready.

## 5. Run the baselines

Run BM25 on SciFact to verify the testbed:

```bash
docker compose run --rm ir2 python testbed.py baselines --systems bm25 --datasets scifact
```

Run the complete baseline evaluation:

```bash
docker compose run --rm ir2 python testbed.py baselines
```

The testbed evaluates retrieval systems on:

| Dataset | Description |
|---|---|
| SciFact | Scientific claim retrieval |
| NFCorpus | Medical information retrieval |
| ArguAna | Counterargument retrieval |

The evaluation metrics are **nDCG@10** and **Recall@100**.

Datasets and pretrained models are downloaded automatically when required.

## 6. Open an interactive Docker terminal

To work directly inside the Docker environment:

```bash
docker compose run --rm ir2 bash
```

Once inside the container, commands can be executed normally:

```bash
python testbed.py baselines --systems bm25 --datasets scifact
```

To exit:

```bash
exit
```

## 7. Evaluate a custom method

Custom methods are implemented under:

```text
pairs/<pair-id>/
```

Each method should generate retrieval rankings for the evaluation datasets in JSON format:

```json
{
  "query_id": {
    "document_id_1": 0.95,
    "document_id_2": 0.82
  }
}
```

Save the output files as:

```text
pairs/<pair-id>/runs/
├── scifact.json
├── nfcorpus.json
└── arguana.json
```

Then evaluate the method:

```bash
docker compose run --rm ir2 python testbed.py score pairs/<pair-id>/runs --method "GPL" --pair <pair-id> --against bge
```

This generates `results.json` with retrieval metrics and comparisons against the selected baseline.

**Important:** GPL training requires additional dependencies and configuration. The current Docker environment is intended for the shared testbed and baseline evaluation.

## 8. Updating the project

Download the latest changes:

```bash
git pull
```

If the Dockerfile or Python dependencies have changed, rebuild the image:

```bash
docker compose build
```

Otherwise, rebuilding is not necessary.

## 9. Useful Docker commands

| Command | Description |
|---|---|
| `docker compose build` | Build the Docker image |
| `docker compose run --rm ir2 bash` | Open an interactive container |
| `docker compose run --rm ir2 python testbed.py baselines` | Run all baselines |
| `docker compose ps` | List running Compose containers |
| `docker compose down` | Stop and remove Compose services |
| `docker image ls` | List available Docker images |

## 10. Troubleshooting

### Cannot connect to Docker daemon

Make sure Docker Desktop is running.

On macOS:

```bash
open -a Docker
```

Check the Docker connection:

```bash
docker info
```

### Docker image build fails

Rebuild with detailed logs:

```bash
docker compose build --no-cache --progress=plain
```

### Python dependency errors

Make sure the Docker image has been rebuilt after modifying `requirements.txt`.

```bash
docker compose build
```

### Apple Silicon compatibility

The current Compose configuration uses `linux/amd64` to provide a consistent environment across macOS and Windows.

On Apple Silicon, AMD64 containers run through emulation, which may reduce performance.

---

**IR2 Project — Université Paris-Saclay**

Paper: *GPL: Generative Pseudo Labeling for Unsupervised Domain Adaptation of Dense Retrieval*