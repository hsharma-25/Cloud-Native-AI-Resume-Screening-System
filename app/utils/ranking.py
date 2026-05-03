from utils.embeddings import get_embedding
from utils.similarity import compute_similarity
from utils.skills import compare_skills
from utils.skills import compare_skills, skill_match_ratio
from utils.suggestions import generate_suggestions

def rank_resumes(jd_text, resumes_dict):
    jd_embedding = get_embedding(jd_text)

    results = []

    for name, text in resumes_dict.items():
        resume_embedding = get_embedding(text)

        semantic_score = compute_similarity(jd_embedding, resume_embedding)
        skill_score = skill_match_ratio(jd_text, text)

        #Final hybrid score
        final_score = 0.7 * semantic_score + 0.3 * skill_score

        skill_data = compare_skills(jd_text, text)

        suggestions = generate_suggestions(
        skill_data["missing"]
        )

        results.append({
            "name": name,
            "score": final_score,
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "matched_skills": skill_data["matched"],
            "missing_skills": skill_data["missing"],
            "suggestions": suggestions
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
