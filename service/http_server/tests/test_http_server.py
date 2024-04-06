import json
import os
import subprocess
import time

import pytest
import requests


@pytest.fixture(autouse=True)
def setup_teardown():
    environ = os.environ.copy()
    environ["CLUSTERED_DATA_PATH"] = "tests/clustered_orig.csv"
    proc = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"], env=environ
    )
    while True:
        try:
            response = requests.get("http://localhost:8080/ping")
            if response.status_code == 200:
                break
        except:
            continue

        time.sleep(1)

    yield

    proc.kill()


def test_ping() -> None:
    response = requests.get("http://localhost:8080/ping")
    assert response.status_code == 200


def test_rating_empty() -> None:
    response = requests.get("http://localhost:8080/rating")
    assert response.status_code == 200
    assert float(response.text) == 0.0


def test_rating_set() -> None:
    for rating in [4, 3]:
        response = requests.post(f"http://localhost:8080/rating?rating={rating}")
        assert response.status_code == 200

    response = requests.get("http://localhost:8080/rating")
    assert response.status_code == 200
    assert float(response.text) == 3.5


def test_invalid_rating() -> None:
    for rating in [-1, 10, "asd"]:
        response = requests.post(f"http://localhost:8080/rating?rating={rating}")
        assert response.status_code != 200


def test_paper_stats() -> None:
    response = requests.get("http://localhost:8080/paper-stats")
    assert response.status_code == 200

    GOLD_RESPONSE_CLUSTERS = [
        {
            "index": 0,
            "description": "model study? new architectures",
            "size": 7,
            "percentage_of_total": 7.0,
        },
        {
            "index": 1,
            "description": "object detection, image segmentation -- downstream/real world tasks",
            "size": 13,
            "percentage_of_total": 13.0,
        },
        {
            "index": 2,
            "description": "?",
            "size": 9,
            "percentage_of_total": 9.0,
        },
        {
            "index": 3,
            "description": "generative image/3D models, diffusion models",
            "size": 10,
            "percentage_of_total": 10.0,
        },
        {
            "index": 4,
            "description": "applications?",
            "size": 4,
            "percentage_of_total": 4.0,
        },
        {
            "index": 5,
            "description": "graphs/clustering/...?",
            "size": 9,
            "percentage_of_total": 9.0,
        },
        {
            "index": 6,
            "description": "transformers, attention (LLMs, ViT, ...)",
            "size": 7,
            "percentage_of_total": 7.0,
        },
        {
            "index": 7,
            "description": "LLMs",
            "size": 19,
            "percentage_of_total": 19.0,
        },
        {
            "index": 8,
            "description": "reinforcement learning, uncertainty estimation",
            "size": 17,
            "percentage_of_total": 17.0,
        },
        {
            "index": 9,
            "description": "applications?",
            "size": 5,
            "percentage_of_total": 5.0,
        },
    ]

    response_json = json.loads(response.text)
    assert response_json["total_papers"] == 100
    for cluster, gold in zip(response_json["clusters"], GOLD_RESPONSE_CLUSTERS):
        for field in cluster.keys():
            if field == "percentage_of_total":
                assert cluster[field] == pytest.approx(gold[field], 1e-8)
            else:
                assert cluster[field] == gold[field]
