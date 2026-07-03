from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeSimilarity:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def calculate_similarity(self, resume_text, job_description):

        resume_embedding = self.model.encode([resume_text])

        job_embedding = self.model.encode([job_description])

        similarity = cosine_similarity(
            resume_embedding,
            job_embedding
        )[0][0]

        return round(similarity * 100, 2)