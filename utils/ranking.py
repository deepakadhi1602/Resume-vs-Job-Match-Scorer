class CandidateRanker:
    """
    Rank candidates based on their AI match score.
    """

    def rank_candidates(self, candidates):

        ranked_candidates = sorted(
            candidates,
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked_candidates