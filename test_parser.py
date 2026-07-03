from utils.parser import ResumeParser
from utils.preprocessing import TextPreprocessor
from utils.skill_extractor import SkillExtractor
from utils.similarity import ResumeSimilarity

parser = ResumeParser()
preprocessor = TextPreprocessor()
extractor = SkillExtractor()
similarity = ResumeSimilarity()

resume_path = "data/test_resume.pdf"

resume_text = parser.extract_text(resume_path)

clean_text = preprocessor.clean_text(resume_text)

skills = extractor.extract_skills(clean_text)

job_description = """
We are hiring a Data Science Intern.

Skills Required:
Python
SQL
Pandas
NumPy
Machine Learning
Scikit-learn
Power BI
Statistics
Git
GitHub
"""

score = similarity.calculate_similarity(
    clean_text,
    job_description
)

print("=" * 50)

print("Extracted Skills")

for skill in skills:
    print("✓", skill)

print()

print("AI Match Score:", score, "%")