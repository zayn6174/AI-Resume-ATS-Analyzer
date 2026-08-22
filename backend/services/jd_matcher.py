from typing import List, Dict

import numpy as np
import spacy
from sentence_transformers import SentenceTransformer
from rapidfuzz import fuzz

from backend.utils.matching import (
    fuzzy_match_keywords,
    normalize_skill
)


def calculate_semantic_similarity(
    resume_text: str,
    jd_text: str,
    embedder: SentenceTransformer
) -> float:

    embeddings = embedder.encode(
        [
            resume_text[:5000],
            jd_text[:5000]
        ],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    resume_emb = embeddings[0]
    jd_emb = embeddings[1]

    similarity = np.dot(
        resume_emb,
        jd_emb
    )

    return float(
        np.clip(similarity, 0.0, 1.0)
    )



def analyze_skills_gap(
    resume_skills: List[str],
    jd_text: str,
    nlp: spacy.Language
) -> List[str]:


    doc = nlp(
        jd_text[:5000]
    )

    jd_skills = set()


    for ent in doc.ents:

        if ent.label_ in [
            "PRODUCT",
            "ORG",
            "LANGUAGE"
        ]:
            jd_skills.add(
                ent.text.lower()
            )


    for chunk in doc.noun_chunks:

        ct = chunk.text.lower().strip()

        if 1 <= len(ct.split()) <= 4:
            jd_skills.add(ct)



    resume_normalized = {
        normalize_skill(skill)
        for skill in resume_skills
    }


    gap = []


    for jd_skill in jd_skills:

        jd_norm = normalize_skill(
            jd_skill
        )


        if jd_norm in resume_normalized:
            continue


        best_score = max(
            (
                fuzz.token_sort_ratio(
                    jd_norm,
                    rs
                )
                for rs in resume_normalized
            ),
            default=0
        )


        if best_score < 75:
            gap.append(
                jd_skill
            )


    return sorted(gap)[:20]



def calculate_match_percentage(
    jd_keywords: List[str],
    matched_keywords: List[str],
    semantic_similarity: float
) -> float:


    if not jd_keywords:
        return 0.0


    keyword_overlap = (
        len(matched_keywords)
        /
        len(jd_keywords)
    )


    match_pct = (
        keyword_overlap * 0.6
        +
        semantic_similarity * 0.4
    ) * 100


    return float(
        np.clip(
            match_pct,
            0.0,
            100.0
        )
    )



def compare_resume_with_jd(
    resume_text: str,
    resume_keywords: List[str],
    resume_skills: List[str],
    jd_text: str,
    jd_keywords: List[str],
    embedder: SentenceTransformer,
    nlp: spacy.Language,
) -> Dict:


    # -----------------------------
    # Semantic similarity
    # -----------------------------

    semantic_similarity = calculate_semantic_similarity(
        resume_text,
        jd_text,
        embedder
    )



    # -----------------------------
    # Keyword matching ONLY ONCE
    # -----------------------------


    keyword_result = fuzzy_match_keywords(
        resume_keywords,
        jd_keywords,
        threshold=80
    )


    matched_keywords = keyword_result["matched"]

    missing_keywords = keyword_result["missing"][:15]


    # -----------------------------
    # Skill gap
    # -----------------------------

    skills_gap = analyze_skills_gap(
        resume_skills,
        jd_text,
        nlp
    )



    match_percentage = calculate_match_percentage(
        jd_keywords,
        matched_keywords,
        semantic_similarity
    )

    return {

        "match_percentage": match_percentage,

        "semantic_similarity": semantic_similarity,

        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords,

        "skills_gap": skills_gap,

    }