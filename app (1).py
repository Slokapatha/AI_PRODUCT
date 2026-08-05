import streamlit as st
import os
import json
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Career & Product Suite", page_icon="🚀", layout="wide")

st.title("🚀 AI Student Utility Suite")
st.write("Build V1 applications powered by Groq & Llama 3.3")

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error("⚠️ Groq API Key not found! Please configure it in your secrets.")
    st.stop()

client = Groq(api_key=api_key)

tab1, tab2 = st.tabs(["🎯 Resume & Email Tailor", "💡 Hackathon MVP Scoper"])

# =========================================================
# TAB 1: RESUME TAILOR
# =========================================================
with tab1:
    st.header("Smart Resume & Outreach Tailor")
    
    col1, col2 = st.columns(2)
    with col1:
        resume_input = st.text_area("Paste Your Resume:", height=200, placeholder="Paste text here...")
    with col2:
        jd_input = st.text_area("Paste Target Job Description:", height=200, placeholder="Paste JD here...")
        
    outreach_type = st.selectbox("Select Output Format:", [
        "LinkedIn Summary", 
        "LinkedIn DM", 
        "Cold Email", 
        "Cover Letter"
    ])
    
    if st.button("Draft Tailored Outreach", type="primary"):
        if not resume_input or not jd_input:
            st.warning("Please provide both Resume and Job Description.")
        else:
            PROMPTS = {
                "LinkedIn Summary": f"""You are an expert career coach. Write a compelling LinkedIn "About" Summary for the candidate, positioning them for the target Job Description.
STRICT RULES:
1. ONLY use facts, skills, and metrics explicitly stated in the RESUME. NO hallucinations.
2. Tone: Professional, forward-looking, and engaging. Maximum 3 short paragraphs.
RESUME: {resume_input}
JOB DESCRIPTION: {jd_input}""",

                "LinkedIn DM": f"""You are an expert career coach. Write a highly concise LinkedIn Direct Message (under 75 words) to a recruiter for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Tone: Direct, polite, and confident. Include a clear Call to Action (e.g., a 10-min chat).
RESUME: {resume_input}
JOB DESCRIPTION: {jd_input}""",

                "Cold Email": f"""You are an expert career coach. Write a Cold Email to a hiring manager for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Must include a catchy, professional Subject Line.
3. Tone: Professional, value-driven. Map 1-2 key resume achievements directly to the job requirements.
RESUME: {resume_input}
JOB DESCRIPTION: {jd_input}""",

                "Cover Letter": f"""You are an expert career coach. Write a formal Cover Letter for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Structure: Formal greeting, engaging opening, 2 body paragraphs matching resume skills to JD needs, and a professional closing.
RESUME: {resume_input}
JOB DESCRIPTION: {jd_input}"""
            }
            
            system_prompt = PROMPTS[outreach_type]
            
            with st.spinner(f"Drafting your {outreach_type}..."):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": system_prompt}],
                    temperature=0.3
                )
                
                st.success("Draft Generated!")
                st.markdown(res.choices[0].message.content)

# =========================================================
# TAB 2: HACKATHON SCOPER
# =========================================================
with tab2:
    st.header("Hackathon MVP Scoper")
    
    raw_idea = st.text_input("Enter your rough project idea:", placeholder="e.g., An app that tracks gym equipment usage in real-time")
    
    tools_available = st.multiselect(
        "Select tools you know how to use:",
        ["Python", "Streamlit", "HTML/CSS", "React", "Groq API", "Gemini API", "Supabase", "Firebase", "SQL"],
        default=["Python", "Streamlit", "Groq API"]
    )
    
    if st.button("Scope Project MVP", type="primary"):
        if not raw_idea:
            st.warning("Please enter a project idea.")
        else:
            scoping_prompt = f"""
            You are a Senior Technical Product Manager.
            Scope a 24-hour hackathon MVP for this idea: {raw_idea}
            
            AVAILABLE TECH STACK: {', '.join(tools_available)}
            
            INSTRUCTIONS:
            1. Define the core problem in 1 sentence.
            2. List 3 key features for V1 that CAN be built using ONLY the available tech stack.
            3. Output STRICT JSON format matching this schema:
            {{
              "project_title": "Catchy Name",
              "problem_statement": "1 sentence",
              "mvp_features": ["Feature A", "Feature B", "Feature C"],
              "tech_stack_mapping": "How the chosen tools will be used"
            }}
            """
            
            with st.spinner("Scoping MVP requirements..."):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": scoping_prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.4
                )
                
                json_data = json.loads(res.choices[0].message.content)
                
                st.subheader(f"📌 Project: {json_data.get('project_title')}")
                st.write(f"**Core Problem:** {json_data.get('problem_statement')}")
                
                st.markdown("**MVP Feature Scope:**")
                for feature in json_data.get("mvp_features", []):
                    st.markdown(f"- {feature}")
                    
                st.info(f"**Tech Stack Plan:** {json_data.get('tech_stack_mapping')}")

# =========================================================
# TAB 3: INTERNSHIP PROJECT SCOPER
# =========================================================
with tab3:
    st.header("Internship Project Scoper")

    uploaded_resume = st.file_uploader(
        "Upload Your Resume (PDF)",
        type=["pdf"]
    )

    target_role = st.selectbox(
        "Target Internship Role",
        [
            "Software Development",
            "AI/ML",
            "Data Science",
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "Cybersecurity",
            "Cloud Computing"
        ]
    )

    company_type = st.selectbox(
        "Target Company",
        [
            "Startup",
            "Product-Based Company",
            "Service-Based Company",
            "FAANG",
            "Research Internship"
        ]
    )

    if st.button("Generate Internship Roadmap", type="primary"):

        if uploaded_resume is None:
            st.warning("Please upload your resume.")
        else:

            # Extract text from PDF
            pdf_reader = PdfReader(uploaded_resume)

            resume_text = ""

            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            prompt = f"""
You are an experienced Software Engineering Hiring Manager.

Analyze the following resume.

Resume:
{resume_text}

Target Role:
{target_role}

Target Company:
{company_type}

Your task:

1. Summarize the candidate's strengths.
2. Identify missing skills.
3. Suggest ONE resume-worthy project that can be completed in 2-3 weeks.
4. Explain why this project improves internship chances.
5. Suggest the best tech stack based ONLY on existing skills.
6. Give a learning roadmap.

Return ONLY valid JSON.

{{
    "strengths":[
        "...",
        "...",
        "..."
    ],

    "skill_gaps":[
        "...",
        "...",
        "..."
    ],

    "recommended_project":{{
        "title":"",
        "description":"",
        "key_features":[
            "",
            "",
            ""
        ],
        "tech_stack":"",
        "difficulty":"",
        "duration":""
    }},

    "why_this_project":"",
    
    "learning_roadmap":[
        "...",
        "...",
        "...",
        "..."
    ]
}}
"""

            with st.spinner("Analyzing Resume..."):

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format={"type":"json_object"},
                    temperature=0.3
                )

                data = json.loads(res.choices[0].message.content)

                st.subheader("💪 Your Strengths")

                for item in data["strengths"]:
                    st.success(item)

                st.subheader("📉 Skill Gaps")

                for item in data["skill_gaps"]:
                    st.warning(item)

                project = data["recommended_project"]

                st.subheader("🚀 Recommended Project")

                st.markdown(f"### {project['title']}")

                st.write(project["description"])

                st.markdown("**Key Features**")

                for feature in project["key_features"]:
                    st.markdown(f"- {feature}")

                st.info(f"**Tech Stack:** {project['tech_stack']}")
                st.info(f"**Difficulty:** {project['difficulty']}")
                st.info(f"**Estimated Time:** {project['duration']}")

                st.subheader("🎯 Why This Project?")

                st.write(data["why_this_project"])

                st.subheader("📚 Learning Roadmap")

                for step in data["learning_roadmap"]:
                    st.markdown(f"- {step}")
