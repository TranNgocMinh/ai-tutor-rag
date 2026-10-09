import json
import time
import random

import faiss
import numpy as np

from google import genai
from google.genai import types

from config import (
    GENERATION_MODEL,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
    TOP_K
)


class RAGEngine:

    def __init__(
        self,
        api_key
    ):

        self.client = genai.Client(
            api_key=api_key
        )

        self.index = faiss.read_index(
            "data/index.faiss"
        )

        with open(
            "data/chunks.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.chunks = json.load(f)


    def embed_text(
        self,
        text,
        max_retries=5
    ):

        last_error = None

        for attempt in range(
            max_retries
        ):

            try:

                result = (
                    self.client.models.embed_content(
                        model=EMBEDDING_MODEL,
                        contents=text,
                        config=
                        types.EmbedContentConfig(
                            output_dimensionality=
                            EMBEDDING_DIM
                        )
                    )
                )

                vector = np.array(
                    result.embeddings[0].values,
                    dtype="float32"
                )

                return vector

            except Exception as e:

                last_error = e

                wait = (
                    2 ** attempt
                    + random.uniform(0, 1)
                )

                time.sleep(wait)

        raise RuntimeError(
            f"Embedding lỗi: {last_error}"
        )


    def retrieve(
        self,
        question,
        top_k=TOP_K
    ):

        vector = self.embed_text(
            question
        )

        vector = (
            vector
            .reshape(1, -1)
            .astype("float32")
        )

        faiss.normalize_L2(
            vector
        )

        scores, indices = (
            self.index.search(
                vector,
                min(
                    top_k,
                    len(self.chunks)
                )
            )
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx < 0:
                continue

            results.append({
                "score":
                float(score),

                "text":
                self.chunks[idx]
            })

        return results


    def generate(
        self,
        prompt,
        max_retries=5
    ):

        last_error = None

        for attempt in range(
            max_retries
        ):

            try:

                response = (
                    self.client.models
                    .generate_content(
                        model=
                        GENERATION_MODEL,

                        contents=
                        prompt
                    )
                )

                if response.text:
                    return response.text

            except Exception as e:

                last_error = e

                error_text = str(e)

                if (
                    "503" in error_text
                    or "UNAVAILABLE"
                    in error_text
                    or "500"
                    in error_text
                ):

                    wait = (
                        2 ** attempt
                        + random.uniform(0, 1)
                    )

                    time.sleep(wait)

                else:
                    raise

        raise RuntimeError(
            f"Gemini lỗi: {last_error}"
        )
