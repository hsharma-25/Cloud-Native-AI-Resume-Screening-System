from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(jd_embedding, resume_embedding):
    score = cosine_similarity([jd_embedding], [resume_embedding])[0][0]
    return score