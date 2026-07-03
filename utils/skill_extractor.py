class SkillExtractor:
    """
    Extract technical skills from resume text.
    """

    def __init__(self):
        self.skills = [
            "python",
            "sql",
            "mysql",
            "postgresql",
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "machine learning",
            "deep learning",
            "data analysis",
            "data science",
            "statistics",
            "power bi",
            "tableau",
            "excel",
            "streamlit",
            "flask",
            "fastapi",
            "git",
            "github",
            "docker",
            "aws",
            "azure",
            "nlp",
            "computer vision"
        ]

    def extract_skills(self, text):

        found_skills = []

        for skill in self.skills:
            if skill in text:
                found_skills.append(skill)

        return sorted(found_skills)