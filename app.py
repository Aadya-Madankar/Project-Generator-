import streamlit as st
import os
import time
import json
from PIL import Image
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

# Import custom modules
from utils.ai_helper import AIHelper
from utils.visualization import (create_project_timeline, 
                              create_skills_graph)

# Page configuration
st.set_page_config(
    page_title="Data Project Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("static/css/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize AI helper
@st.cache_resource
def get_ai_helper():
    return AIHelper()

# Session state initialization
if 'project_ideas' not in st.session_state:
    st.session_state.project_ideas = []
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'project_details' not in st.session_state:
    st.session_state.project_details = None
if 'timeline_data' not in st.session_state:
    st.session_state.timeline_data = None
if 'skills_data' not in st.session_state:
    st.session_state.skills_data = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Generate"
if 'saved_projects' not in st.session_state:
    st.session_state.saved_projects = []
if 'job_title' not in st.session_state:
    st.session_state.job_title = ""
if 'tools' not in st.session_state:
    st.session_state.tools = ""
if 'industry' not in st.session_state:
    st.session_state.industry = ""

# Try to load custom CSS
try:
    load_css()
except:
    st.warning("Could not load custom CSS. Using default styles.")

# Initialize AI Helper
ai_helper = get_ai_helper()

# Create sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/idea.png", width=80)
    st.title("Data Project Generator")
    
    # Sidebar navigation
    selected = option_menu(
        "Main Menu", 
        ["Home", "Generate", "Explore", "Saved Projects", "About"], 
        icons=['house', 'magic', 'search', 'bookmark', 'info-circle'], 
        menu_icon="cast", 
        default_index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Actions")
    
    if st.sidebar.button("Generate New Projects"):
        st.session_state.active_tab = "Generate"
    
    if st.sidebar.button("View Saved Projects"):
        st.session_state.active_tab = "Saved Projects"

# Job profile variables
job_title = st.session_state.job_title
tools = st.session_state.tools
industry = st.session_state.industry

# Main content
if selected == "Home":
    # Header
    st.markdown("<header><h1>Data Project Generator</h1><p>Discover and design impactful data projects for your portfolio</p></header>", unsafe_allow_html=True)
    
    # How it works - 3 columns
    st.markdown("## How It Works")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/null/gender-neutral-user.png", width=60)
        st.markdown("### 1. Define Your Profile")
        st.markdown("Enter your job title, the tools you use, and your industry focus.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/null/idea.png", width=60)
        st.markdown("### 2. Generate Ideas")
        st.markdown("Our AI suggests tailored project ideas specific to your profile.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/null/visualization-skill.png", width=60)
        st.markdown("### 3. Explore Details")
        st.markdown("Get implementation details, timelines, and required skills.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sample project examples
    st.markdown("## Example Projects")
    
    # Create a 2x2 grid of example projects
    col1, col2 = st.columns(2)
    
    # Example 1
    with col1:
        st.markdown('<div class="example-card">', unsafe_allow_html=True)
        st.markdown("### Healthcare Patient Flow Optimization")
        st.markdown("**Role:** Data Scientist")
        st.markdown("**Tools:** Python, SQL, Tableau")
        st.markdown("**Industry:** Healthcare")
        st.markdown("A project to analyze hospital patient data and optimize resource allocation and patient flow through departments.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Example 2
    with col2:
        st.markdown('<div class="example-card">', unsafe_allow_html=True)
        st.markdown("### Financial Fraud Detection System")
        st.markdown("**Role:** Machine Learning Engineer")
        st.markdown("**Tools:** Python, TensorFlow, SQL")
        st.markdown("**Industry:** Finance")
        st.markdown("Building a real-time fraud detection system to identify suspicious transactions using machine learning algorithms.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Example 3
    with col1:
        st.markdown('<div class="example-card">', unsafe_allow_html=True)
        st.markdown("### Retail Customer Segmentation")
        st.markdown("**Role:** Data Analyst")
        st.markdown("**Tools:** Python, R, PowerBI")
        st.markdown("**Industry:** Retail")
        st.markdown("Analyzing customer purchase history to create meaningful segments for targeted marketing campaigns.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Example 4
    with col2:
        st.markdown('<div class="example-card">', unsafe_allow_html=True)
        st.markdown("### Supply Chain Optimization")
        st.markdown("**Role:** Operations Analyst")
        st.markdown("**Tools:** Python, Excel, Tableau")
        st.markdown("**Industry:** Manufacturing")
        st.markdown("Optimizing inventory management and logistics using historical data and predictive analytics.")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Generate":
    # Header
    st.markdown("<header><h1>Generate Project Ideas</h1><p>Create tailored data projects based on your profile</p></header>", unsafe_allow_html=True)
    
    # Job Profile Section
    st.markdown("## Job Profile")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        job_title = st.text_input("Job Title:", 
                          placeholder="e.g., data analyst, data scientist",
                          value=st.session_state.job_title)
        st.session_state.job_title = job_title
    
    with col2:
        tools = st.text_input("Tools:", 
                      placeholder="e.g., Python, R, SQL, PowerBI",
                      value=st.session_state.tools)
        st.session_state.tools = tools
    
    with col3:
        industry = st.text_input("Industry:", 
                        placeholder="e.g., Healthcare, Finance",
                        value=st.session_state.industry)
        st.session_state.industry = industry
    
    # Check if inputs are provided
    if not job_title or not tools or not industry:
        st.warning("Please fill in your job title, tools, and industry to generate project ideas.")
    else:
        # Button to generate project ideas
        if st.button("Generate Project Ideas"):
            with st.spinner("Generating project ideas..."):
                try:
                    # Generate project ideas
                    st.session_state.project_ideas = ai_helper.generate_project_ideas(
                        job_title, tools, industry
                    )
                    st.success(f"Generated {len(st.session_state.project_ideas)} project ideas!")
                except Exception as e:
                    st.error(f"Error generating project ideas: {e}")
        
        # Display project ideas
        if st.session_state.project_ideas:
            st.markdown("## Project Ideas")
            
            # Create a grid layout for project cards
            cols = st.columns(2)
            for i, idea in enumerate(st.session_state.project_ideas):
                with cols[i % 2]:
                    # Removed div with project-card class that was causing the styling issue
                    st.markdown(f"### {i+1}. {idea}")
                    if st.button("Select", key=f"select_{i}"):
                        st.session_state.selected_project = idea
                        # Clear previous project details
                        st.session_state.project_details = None
                        st.session_state.timeline_data = None
                        st.session_state.skills_data = None
                
            # Clear button for project ideas
            if st.button("Clear Ideas"):
                st.session_state.project_ideas = []
                st.session_state.selected_project = None
                st.session_state.project_details = None
                st.session_state.timeline_data = None
                st.session_state.skills_data = None
                st.rerun()
        
        # If a project is selected, provide detailed explanation
        if st.session_state.selected_project:
            st.markdown("---")
            st.markdown(f"## Selected Project: {st.session_state.selected_project}")
            
            # Create tabs for different visualizations
            project_tabs = st.tabs([
                "1. Details", 
                "2. Timeline", 
                "3. Skills Graph"
            ])
            
            # Details tab
            with project_tabs[0]:
                # Display project description
                if st.session_state.project_details:
                    st.markdown(f"### {st.session_state.selected_project}")
                    st.markdown(st.session_state.project_details)
                else:
                    if st.button("Generate Project Details"):
                        with st.spinner("Generating project details..."):
                            st.session_state.project_details = ai_helper.generate_project_details(
                                st.session_state.selected_project,
                                job_title,
                                tools,
                                industry
                            )
                            st.success("Project details generated!")
                            st.rerun()
            
            # Timeline tab
            with project_tabs[1]:
                if st.session_state.timeline_data is None:
                    if st.button("Generate Timeline"):
                        # Only generate timeline if we have project details
                        if st.session_state.project_details:
                            with st.spinner("Generating project timeline..."):
                                try:
                                    st.session_state.timeline_data = ai_helper.generate_timeline(
                                        project_title=st.session_state.selected_project,
                                        job_title=job_title,
                                        tools=tools,
                                        industry=industry
                                    )
                                    st.success("Timeline generated!")
                                except Exception as e:
                                    st.error(f"Error generating timeline: {e}")
                        else:
                            st.error("Please generate project details first.")
                
                if st.session_state.timeline_data:
                    # Create and display timeline
                    timeline_fig = create_project_timeline(st.session_state.timeline_data)
                    if timeline_fig:
                        st.plotly_chart(timeline_fig, use_container_width=True)
                    else:
                        st.error("Could not create timeline visualization.")
            
            # Skills Graph tab
            with project_tabs[2]:
                if st.session_state.skills_data is None:
                    if st.button("Generate Skills Graph"):
                        # Only generate skills graph if we have project details
                        if st.session_state.project_details:
                            with st.spinner("Generating skills graph..."):
                                try:
                                    st.session_state.skills_data = ai_helper.generate_skills_graph(
                                        project_title=st.session_state.selected_project,
                                        job_title=job_title,
                                        tools=tools,
                                        industry=industry
                                    )
                                    st.success("Skills graph generated!")
                                except Exception as e:
                                    st.error(f"Error generating skills graph: {e}")
                        else:
                            st.error("Please generate project details first.")
                
                if st.session_state.skills_data:
                    # Create and display skills graph
                    skills_fig = create_skills_graph(st.session_state.skills_data)
                    if skills_fig:
                        st.pyplot(skills_fig)
                    else:
                        st.error("Could not create skills graph visualization.")
            
            # Save project button
            if st.button("Save Project"):
                project_info = {
                    "title": st.session_state.selected_project,
                    "job_title": job_title,
                    "tools": tools,
                    "industry": industry,
                    "details": st.session_state.project_details,
                    "date_saved": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                
                # Add to saved projects if not already saved
                titles = [p.get("title") for p in st.session_state.saved_projects]
                if st.session_state.selected_project not in titles:
                    st.session_state.saved_projects.append(project_info)
                    st.success("Project saved!")
                else:
                    st.info("This project is already saved.")

elif selected == "Explore":
    # Header
    st.markdown("<header><h1>Explore Project Ideas</h1><p>Browse through a collection of pre-generated project ideas</p></header>", unsafe_allow_html=True)
    
    # Filter options
    st.markdown("## Filter Projects")
    col1, col2, col3 = st.columns(3)
    with col1:
        explore_role = st.selectbox("Role", 
            ["All Roles", "Data Analyst", "Data Scientist", "Data Engineer", "BI Developer", "ML Engineer"])
    with col2:
        explore_industry = st.selectbox("Industry", 
            ["All Industries", "Healthcare", "Finance", "Retail", "Technology", "Manufacturing"])
    with col3:
        explore_tool = st.selectbox("Primary Tool", 
            ["All Tools", "Python", "R", "SQL", "Excel", "PowerBI", "Tableau"])
    
    # Preset project examples
    explore_projects = [
        {
            "title": "Customer Segmentation Analysis", 
            "role": "Data Analyst", 
            "industry": "Retail", 
            "tools": "Python, Scikit-learn",
            "description": "Use clustering algorithms to segment customers based on purchasing behavior."
        },
        {
            "title": "Fraud Detection System", 
            "role": "Data Scientist", 
            "industry": "Finance", 
            "tools": "Python, TensorFlow",
            "description": "Build a machine learning model to detect fraudulent transactions."
        },
        {
            "title": "Patient Readmission Prediction", 
            "role": "Data Scientist", 
            "industry": "Healthcare", 
            "tools": "R, SQL",
            "description": "Predict which patients are likely to be readmitted to hospitals within 30 days."
        },
        {
            "title": "Data Warehouse ETL Pipeline", 
            "role": "Data Engineer", 
            "industry": "Technology", 
            "tools": "Python, SQL, Airflow",
            "description": "Design and implement an ETL pipeline for a data warehouse."
        },
        {
            "title": "Sales Performance Dashboard", 
            "role": "BI Developer", 
            "industry": "Retail", 
            "tools": "PowerBI, SQL",
            "description": "Create an interactive dashboard to track sales performance across regions."
        },
        {
            "title": "Predictive Maintenance System", 
            "role": "ML Engineer", 
            "industry": "Manufacturing", 
            "tools": "Python, scikit-learn",
            "description": "Build a model to predict equipment failures before they occur."
        },
        {
            "title": "HR Analytics Dashboard", 
            "role": "Data Analyst", 
            "industry": "Technology", 
            "tools": "Tableau, Excel",
            "description": "Analyze employee data to discover patterns in retention and productivity."
        },
        {
            "title": "Credit Scoring Model", 
            "role": "Data Scientist", 
            "industry": "Finance", 
            "tools": "Python, XGBoost",
            "description": "Develop a machine learning model to assess customer creditworthiness."
        }
    ]
    
    # Apply filters
    filtered_projects = explore_projects
    if explore_role != "All Roles":
        filtered_projects = [p for p in filtered_projects if p["role"] == explore_role]
    if explore_industry != "All Industries":
        filtered_projects = [p for p in filtered_projects if p["industry"] == explore_industry]
    if explore_tool != "All Tools":
        filtered_projects = [p for p in filtered_projects if explore_tool.lower() in p["tools"].lower()]
    
    # Display filtered projects
    if filtered_projects:
        st.markdown(f"## Found {len(filtered_projects)} Projects")
        
        cols = st.columns(2)
        for i, project in enumerate(filtered_projects):
            with cols[i % 2]:
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### {project['title']}")
                st.markdown(f"**Role:** {project['role']}")
                st.markdown(f"**Industry:** {project['industry']}")
                st.markdown(f"**Tools:** {project['tools']}")
                st.markdown(f"**Description:** {project['description']}")
                
                # Button to use this project as a template
                if st.button("Use as Template", key=f"use_{i}"):
                    st.session_state.selected_project = project['title']
                    st.session_state.active_tab = "Generate"
                    # Set sidebar values
                    job_title = project['role']
                    industry = project['industry']
                    tools = project['tools']
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No projects match your filter criteria. Try adjusting your filters.")

elif selected == "Saved Projects":
    # Header
    st.markdown("<header><h1>Saved Projects</h1><p>View and manage your saved project ideas</p></header>", unsafe_allow_html=True)
    
    if not st.session_state.saved_projects:
        st.info("You haven't saved any projects yet. Generate and save projects to see them here.")
    else:
        # Create tabs for each saved project
        project_tabs = st.tabs([project["title"] for project in st.session_state.saved_projects])
        
        for i, tab in enumerate(project_tabs):
            with tab:
                project = st.session_state.saved_projects[i]
                
                # Project metadata
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {project['title']}")
                    st.markdown(f"**Job Role:** {project['job_title']}")
                    st.markdown(f"**Industry:** {project['industry']}")
                    st.markdown(f"**Tools:** {project['tools']}")
                    st.markdown(f"**Saved on:** {project['date_saved']}")
                
                with col2:
                    # Delete project button
                    if st.button("Delete", key=f"delete_{i}"):
                        st.session_state.saved_projects.pop(i)
                        st.rerun()
                    
                    # Edit project button
                    if st.button("Continue Working", key=f"edit_{i}"):
                        st.session_state.selected_project = project['title']
                        st.session_state.active_tab = "Generate"
                        st.rerun()
                
                # Project details
                st.markdown("### Project Details")
                st.markdown(project['details'])
        
        # Export functionality
        st.markdown("---")
        st.markdown("### Export Projects")
        export_format = st.selectbox("Select export format:", ["JSON", "Markdown"])
        
        if st.button("Export All Projects"):
            if export_format == "JSON":
                # Export as JSON
                json_data = json.dumps(st.session_state.saved_projects, indent=4)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="data_projects.json",
                    mime="application/json"
                )
            else:
                # Export as Markdown
                markdown_text = ""
                for project in st.session_state.saved_projects:
                    markdown_text += f"# {project['title']}\n\n"
                    markdown_text += f"**Job Role:** {project['job_title']}\n\n"
                    markdown_text += f"**Industry:** {project['industry']}\n\n"
                    markdown_text += f"**Tools:** {project['tools']}\n\n"
                    markdown_text += f"**Saved on:** {project['date_saved']}\n\n"
                    markdown_text += f"## Project Details\n\n{project['details']}\n\n"
                    markdown_text += "---\n\n"
                
                st.download_button(
                    label="Download Markdown",
                    data=markdown_text,
                    file_name="data_projects.md",
                    mime="text/markdown"
                )

elif selected == "About":
    # Header
    st.markdown("<header><h1>About This App</h1><p>Learn more about the Data Project Generator</p></header>", unsafe_allow_html=True)
    
    # Developer Information
    st.markdown("## Developer")
    st.markdown("### Komal Lande")
    st.markdown("This application was created by Komal Lande as a tool to help data professionals generate project ideas tailored to their skills and interests.")
    
    # About the app
    st.markdown("## About the App")
    st.markdown("""
    The Data Project Generator is designed to help data professionals generate relevant and impactful project ideas 
    based on their specific job roles, tools, and industries. Whether you're building a portfolio, expanding your skills, 
    or looking for new challenges, this tool can help spark creative and practical project ideas.
    """)
    
    # Features
    st.markdown("## Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### AI-Powered Generation")
        st.markdown("Leverages Google's Gemini AI to create customized project ideas tailored to your profile.")
        
        st.markdown("### Detailed Exploration")
        st.markdown("Provides in-depth project details, implementation steps, and challenges to consider.")
    
    with col2:
        st.markdown("### Visual Planning")
        st.markdown("Creates timelines and skills graphs to help you visualize your project.")
        
        st.markdown("### Project Management")
        st.markdown("Save your favorite project ideas for later reference and export details for implementation.")
    
    # Technologies used
    st.markdown("## Technologies Used")
    st.markdown("""
    - **Streamlit**: Frontend framework for the web application
    - **Google Gemini AI**: AI model for generating project ideas and details
    - **Plotly & Matplotlib**: Data visualization libraries
    - **NetworkX**: Network graph creation for skills visualization
    """)
    
    # Contact/feedback section
    st.markdown("### Feedback & Suggestions")
    with st.form("feedback_form"):
        feedback_text = st.text_area("Share your thoughts or suggestions:", height=100)
        feedback_name = st.text_input("Your Name (optional):")
        feedback_email = st.text_input("Your Email (optional):")
        
        submit_button = st.form_submit_button("Submit Feedback")
        if submit_button:
            if feedback_text:
                st.success("Thank you for your feedback! We appreciate your input.")
            else:
                st.error("Please enter some feedback before submitting.")

# Check if the session state active tab needs to override the selected sidebar menu
if st.session_state.active_tab != selected:
    st.session_state.active_tab = selected
    st.rerun()