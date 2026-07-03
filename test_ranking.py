from utils.ranking import CandidateRanker

ranker = CandidateRanker()

candidates = [
    {"name": "John Doe", "score": 92.4},
    {"name": "Alice Smith", "score": 84.7},
    {"name": "Michael Johnson", "score": 77.9},
    {"name": "Emma Wilson", "score": 89.2},
]

ranked = ranker.rank_candidates(candidates)

print("=" * 40)
print("Candidate Ranking")
print("=" * 40)

for i, candidate in enumerate(ranked, start=1):
    print(
        f"{i}. {candidate['name']} - {candidate['score']}%"
    )