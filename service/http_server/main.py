import os

import pandas as pd
from fastapi import FastAPI, HTTPException, Response

MAX_COUNT = 10
CLUSTER_DESCRIPTIONS = [
    "model study? new architectures",
    "object detection, image segmentation -- downstream/real world tasks",
    "?",
    "generative image/3D models, diffusion models",
    "applications?",
    "graphs/clustering/...?",
    "transformers, attention (LLMs, ViT, ...)",
    "LLMs",
    "reinforcement learning, uncertainty estimation",
    "applications?",
]
MAX_CLUSTER = len(CLUSTER_DESCRIPTIONS) - 1

data_path = os.environ["CLUSTERED_DATA_PATH"]

app = FastAPI()
app.df = pd.read_csv(data_path)
app.ratings_sum = 0
app.ratings_num = 0

if app.df["cluster"].nunique() != len(CLUSTER_DESCRIPTIONS):
    raise ValueError(
        "Invalid clustered data -- number of clusters is different from the number of descriptions"
    )


def format_random_papers(df: pd.DataFrame, cluster: int, count: int = 5) -> list[str]:
    df = (
        df[df["cluster"] == cluster]
        .sample(n=count, replace=False)
        .reset_index(drop=True)
    )
    df["url"] = df["paperId"].apply(
        lambda paper_id: f"https://www.semanticscholar.org/paper/{paper_id}"
    )
    return df[["title", "year", "abstract", "url"]].to_dict(orient="records")


@app.get("/ping")
def ping():
    return Response()


@app.post("/rating")
def rate(rating: int):
    if rating < 0 or rating > 5:
        raise HTTPException(
            status_code=400, detail="Rating should be a whole number between 1 and 5"
        )

    app.ratings_num += 1
    app.ratings_sum += rating

    return Response()


@app.get("/rating")
def average_rating():
    if app.ratings_num == 0:
        return 0.0

    return app.ratings_sum / app.ratings_num


@app.get("/random-papers")
def random_papers(cluster: int, count: int = 5):
    if cluster < 0 or cluster > MAX_CLUSTER:
        raise HTTPException(
            status_code=400, detail="Cluster index should be between 0 and 9"
        )

    if count < 1 or count > MAX_COUNT:
        raise HTTPException(status_code=400, detail="Count should be between 1 and 10")

    return format_random_papers(df=app.df, cluster=cluster, count=count)


@app.get("/paper-stats")
def paper_stats():
    total_papers = len(app.df)
    clusters = [
        {
            "index": i,
            "description": description,
            "size": count,
            "percentage_of_total": count / total_papers * 100.0,
        }
        for (i, count), description in zip(
            app.df["cluster"].value_counts().sort_index().items(), CLUSTER_DESCRIPTIONS
        )
    ]
    return {
        "total_papers": total_papers,
        "clusters": clusters,
    }
