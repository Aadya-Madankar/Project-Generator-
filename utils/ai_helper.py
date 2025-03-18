"""
AI Helper module for interacting with Google's Generative AI models.
This module provides functions to interact with the Gemini API.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the genai library
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class AIHelper:
    """Class to handle interactions with the AI model."""
    
    def __init__(self, model_name='gemini-2.0-flash'):
        """Initialize the AI helper with the specified model."""
        self.model = genai.GenerativeModel(model_name)
    
    def generate_project_ideas(self, job_title, tools, industry, count=10):
        """Generate project ideas based on the given parameters."""
        prompt = f"""Generate exactly {count} project titles for a {job_title} using {tools} 
        with a focus in the {industry} industry. 
        Format the response as a numbered list (1., 2., etc.).
        Make these projects realistic, implementable, and tailored to the job role.
        """
        response = self.model.generate_content(prompt)
        # Process the response to extract project ideas
        project_list = response.text.split("\n")
        # Clean up the list (remove empty items and headers)
        clean_list = [item.strip() for item in project_list if item.strip() and not item.strip().lower().startswith(("project", "here", "title"))]
        return clean_list
    
    def generate_project_details(self, project_title, job_title, tools, industry):
        """Generate detailed explanation for a selected project."""
        prompt = f"""Provide a detailed explanation for the project: "{project_title}"
        This is for a {job_title} using {tools} with a focus in the {industry} industry.
        
        Structure your response with the following sections:
        1. Problem Statement: Clearly define the problem being addressed
        2. Project Goals: List the specific objectives (3-5 bullet points)
        3. Data Requirements: What data will be needed and potential sources
        4. Technical Approach: Step-by-step workflow with methodologies and tools
        5. Implementation Guide: Detailed implementation steps
        6. Deliverables: Expected outputs and their business value
        7. Skills Developed: What skills this project helps develop
        8. Extensions: Ways to extend or enhance the project
        
        Use markdown formatting for headers and sections.
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_mind_map(self, project_title, job_title, tools, industry):
        """Generate data for a mind map visualization of the project."""
        prompt = f"""Create a mind map for the project: "{project_title}"
        This is for a {job_title} using {tools} with a focus in the {industry} industry.
        
        Format the response as a properly formatted JSON with the following structure:
        {{
            "center": "{project_title}",
            "main_branches": [
                {{
                    "name": "Branch 1",
                    "sub_branches": ["Sub-branch 1.1", "Sub-branch 1.2"]
                }},
                {{
                    "name": "Branch 2",
                    "sub_branches": ["Sub-branch 2.1", "Sub-branch 2.2"]
                }}
            ]
        }}
        
        Create 4-6 main branches that represent key aspects of the project.
        Each main branch should have 2-4 sub-branches with more specific details.
        Make sure all values are meaningful and relevant to the project.
        Ensure the response is ONLY valid JSON with no additional text before or after.
        Use double quotes for all keys and string values.
        """
        try:
            response = self.model.generate_content(prompt)
            
            # Clean the response to ensure it's valid JSON
            text = response.text.strip()
            # Remove any markdown code block indicators
            if text.startswith("```json"):
                text = text.replace("```json", "", 1)
            if text.startswith("```"):
                text = text.replace("```", "", 1)
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Validate the JSON by parsing it
            import json
            json.loads(text)
            
            return text
        except Exception as e:
            print(f"Error generating mind map: {e}")
            # Return a fallback mind map structure
            fallback = {
                "center": project_title,
                "main_branches": [
                    {
                        "name": "Project Goals",
                        "sub_branches": ["Improve accuracy", "Increase efficiency", "Enhance user experience"]
                    },
                    {
                        "name": "Technologies",
                        "sub_branches": ["Python", "Data Science", "Machine Learning"]
                    },
                    {
                        "name": "Deliverables",
                        "sub_branches": ["Technical documentation", "Interactive dashboard", "Final report"]
                    },
                    {
                        "name": "Timeline",
                        "sub_branches": ["Planning phase", "Development phase", "Testing phase", "Deployment"]
                    },
                    {
                        "name": "Resources",
                        "sub_branches": ["Team members", "Computing resources", "Data sources"]
                    }
                ]
            }
            return json.dumps(fallback)
    
    def generate_sample_data(self, project_title, job_title, tools, industry):
        """Generate sample data structure for the project."""
        prompt = f"""For the project "{project_title}" in the {industry} industry,
        suggest a realistic data structure that might be used.
        
        Format your response as a list of possible tables/collections with their fields.
        For each table/collection, include 3-5 sample records with realistic values.
        
        Focus on data that would be relevant for a {job_title} using {tools}.
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_timeline(self, project_title, job_title, tools, industry):
        """Generate data for a project timeline visualization."""
        prompt = f"""Create a project timeline for the project: "{project_title}"
        This is for a {job_title} using {tools} with a focus in the {industry} industry.
        
        Format the response as a properly formatted JSON with the following structure:
        {{
            "phases": ["Phase 1", "Phase 2", "Phase 3"],
            "start_dates": ["2025-01-01", "2025-02-01", "2025-03-01"],
            "end_dates": ["2025-01-31", "2025-02-28", "2025-03-31"],
            "descriptions": ["Description 1", "Description 2", "Description 3"]
        }}
        
        Include 4-6 realistic project phases with appropriate start and end dates.
        Make sure all dates are in YYYY-MM-DD format and make sense chronologically.
        Ensure the response is ONLY valid JSON with no additional text before or after.
        Each description should be 1-2 sentences explaining the phase activities.
        Use double quotes for all keys and string values.
        """
        try:
            response = self.model.generate_content(prompt)
            
            # Clean the response to ensure it's valid JSON
            text = response.text.strip()
            # Remove any markdown code block indicators
            if text.startswith("```json"):
                text = text.replace("```json", "", 1)
            if text.startswith("```"):
                text = text.replace("```", "", 1)
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Validate the JSON by parsing it
            import json
            json.loads(text)
            
            return text
        except Exception as e:
            print(f"Error generating timeline: {e}")
            # Return a fallback timeline structure
            import datetime
            
            start_date = datetime.datetime.now()
            phases = ["Requirements Gathering", "Data Collection", "Model Development", "Testing", "Deployment"]
            durations = [15, 30, 45, 15, 15]  # days
            
            start_dates = []
            end_dates = []
            current_date = start_date
            
            for duration in durations:
                start_dates.append(current_date.strftime("%Y-%m-%d"))
                current_date = current_date + datetime.timedelta(days=duration)
                end_dates.append(current_date.strftime("%Y-%m-%d"))
                current_date = current_date + datetime.timedelta(days=1)  # 1 day gap
            
            fallback = {
                "phases": phases,
                "start_dates": start_dates,
                "end_dates": end_dates,
                "descriptions": [
                    "Define project requirements and gather necessary resources.",
                    "Collect and preprocess relevant data from healthcare systems.",
                    "Develop and train machine learning models on the collected data.",
                    "Thoroughly test models and validate results against requirements.",
                    "Deploy the solution to production environment and monitor performance."
                ]
            }
            return json.dumps(fallback)
    
    def generate_skills_graph(self, project_title, job_title, tools, industry):
        """Generate data for a skills network visualization."""
        prompt = f"""Create a network of skills required for the project: "{project_title}"
        This is for a {job_title} using {tools} with a focus in the {industry} industry.
        
        Format the response as a properly formatted JSON with the following structure:
        {{
            "nodes": [
                {{"id": "Skill 1", "group": 1}},
                {{"id": "Skill 2", "group": 2}},
                {{"id": "Skill 3", "group": 3}}
            ],
            "links": [
                {{"source": "Skill 1", "target": "Skill 2", "value": 1}},
                {{"source": "Skill 2", "target": "Skill 3", "value": 2}},
                {{"source": "Skill 1", "target": "Skill 3", "value": 3}}
            ]
        }}
        
        Create at least 8-12 skill nodes with appropriate links between them. 
        Group similar skills together (same group number).
        Include both technical and soft skills relevant to the project.
        Ensure the response is ONLY valid JSON with no additional text before or after.
        Use double quotes for all keys and string values.
        """
        try:
            response = self.model.generate_content(prompt)
            
            # Clean the response to ensure it's valid JSON
            text = response.text.strip()
            # Remove any markdown code block indicators
            if text.startswith("```json"):
                text = text.replace("```json", "", 1)
            if text.startswith("```"):
                text = text.replace("```", "", 1)
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Validate the JSON by parsing it
            import json
            json.loads(text)
            
            return text
        except Exception as e:
            print(f"Error generating skills graph: {e}")
            # Return a fallback simple skills graph structure
            fallback = {
                "nodes": [
                    {"id": "Python", "group": 1},
                    {"id": "Data Analysis", "group": 1},
                    {"id": "Machine Learning", "group": 1},
                    {"id": "Healthcare Domain", "group": 2},
                    {"id": "Data Visualization", "group": 1},
                    {"id": "Project Management", "group": 3},
                    {"id": "Communication", "group": 3},
                    {"id": "Problem Solving", "group": 3}
                ],
                "links": [
                    {"source": "Python", "target": "Data Analysis", "value": 3},
                    {"source": "Python", "target": "Machine Learning", "value": 3},
                    {"source": "Machine Learning", "target": "Healthcare Domain", "value": 2},
                    {"source": "Data Analysis", "target": "Data Visualization", "value": 2},
                    {"source": "Data Analysis", "target": "Healthcare Domain", "value": 2},
                    {"source": "Project Management", "target": "Communication", "value": 1},
                    {"source": "Problem Solving", "target": "Machine Learning", "value": 1}
                ]
            }
            return json.dumps(fallback)
