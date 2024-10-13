from django.apps import AppConfig

class ViralappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'viralapp'

    def ready(self):
        from .chatbot import ChatbotManager
        from .models import Resume
        demo_github_projects = [
            "https://github.com/ViralBiyawala/Stanford_LLM_Tutor",
            "https://github.com/ShivamSikotra11/MHA",
            "https://github.com/jitanshuraut/Learn-AI-Studio",
            "https://github.com/ViralBiyawala/ATLAS-PowerBI",
            "https://github.com/ViralBiyawala/BBMS",
            "https://github.com/ViralBiyawala/ViralShare",
            "https://github.com/ViralBiyawala/Portfolio",
            "https://github.com/ViralBiyawala/DS_ML_Projects/tree/main/A_Visual_History_of_Nobel_Prize_Winners",
            "https://github.com/ViralBiyawala/DS_ML_Projects/tree/main/Dr._Semmelweis_and_the_Discovery_of_Handwashing",
            "https://www.datacamp.com/datalab/w/058082b0-6db9-4b7e-a510-faa8de89f91d"
        ]

        # Define the portfolio URLs and demo GitHub projects
        portfolio_urls = [
            "https://github.com/ViralBiyawala/ViralBiyawala",
            "https://viralbiyawala.pythonanywhere.com/index",
            "https://viralbiyawala.pythonanywhere.com/education",
            "https://viralbiyawala.pythonanywhere.com/certification",
            "https://viralbiyawala.pythonanywhere.com/project"
        ]

        resume = Resume.objects.first()

        # Initialize the ChatbotManager with required inputs
        self.chatbot_manager = ChatbotManager(
            resume_path=resume.resume_file.url,
            portfolio_urls=portfolio_urls,
            github_project_urls=demo_github_projects
        )

        self.chatbot_manager.initialize_sources()

        # Step 2: Create the agent
        self.agent_executor = self.chatbot_manager.create_agent()