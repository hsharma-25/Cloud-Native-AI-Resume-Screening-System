import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.embeddings import get_embedding
from utils.similarity import compute_similarity

nlp = spacy.load("en_core_web_sm")

SKILL_VOCAB = [
    # Tech
    "python", "java", "sql", "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "data analysis", "pandas", "numpy",

    # Business / HR / Management
    "recruitment", "employee relations", "performance management",
    "training", "leadership", "communication", "project management",
    "human resources", "organizational development",

    # Tools
    "excel", "power bi", "tableau", "sap",

    # General
    "problem solving", "critical thinking", "time management"
]


def is_valid_phrase(phrase):
    doc = nlp(phrase)

    for token in doc:
        if token.pos_ not in ["NOUN", "PROPN"]:
            return False

    return True


def extract_keywords_from_jd(jd_text, top_n=20):
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1,2)
    )

    tfidf_matrix = vectorizer.fit_transform([jd_text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    top_indices = scores.argsort()[::-1]

    keywords = []

    for i in top_indices:
        word = feature_names[i]

        #Only keep if in skill vocab
        for skill in SKILL_VOCAB:
            if skill in word or word in skill:
                keywords.append(skill)

        if len(keywords) >= top_n:
            break

    return list(set(keywords))

def compare_skills(jd_text, resume_text):
    jd_keywords = extract_keywords_from_jd(jd_text)

    matched, missing = semantic_skill_match(
        jd_keywords,
        resume_text
    )

    return {
        "matched": matched,
        "missing": missing,
        "jd_keywords": jd_keywords
    }

from utils.embeddings import get_embedding
from utils.similarity import compute_similarity

def semantic_skill_match(jd_skills, resume_text, threshold=0.45):
    matched = []
    missing = []

    resume_text = resume_text.lower()

    for skill in jd_skills:

        #Exact match first
        if skill.lower() in resume_text:
            matched.append(skill)
            continue

        #Semantic fallback
        skill_embedding = get_embedding(skill)
        resume_embedding = get_embedding(resume_text[:1000])

        similarity = compute_similarity(
            skill_embedding,
            resume_embedding
        )

        if similarity >= threshold:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing

def skill_match_ratio(jd_text, resume_text):
    jd_keywords = extract_keywords_from_jd(jd_text)

    matched, _ = semantic_skill_match(
        jd_keywords,
        resume_text
    )

    if len(jd_keywords) == 0:
        return 0

    return len(matched) / len(jd_keywords)