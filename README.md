Multi-Source Candidate Data Transformer

Overview
This project ingests candidate data from multiple sources (ATS and LinkedIn), normalizes the data, merges it into a canonical profile, 
tracks provenance information, calculates confidence scores, validates the output schema, and generates configurable output projections.

How to Run
Install:
pip install -r requirements.txt
Run Streamlit UI:
streamlit run ui.py

Sample Input
ATS Data
{
  "candidate_name": "Thomas Andrew",
  "email": "ThomasAndrew@gmail.com",
  "phone": "9876543210",
  "experience": 3,
  "skills": ["Python", "SQL","Machine Learning", "Data Analysis"]
}
LinkedIn Data
Thomas Andrew
Software Engineer
Location: Bangalore, India
Skills: Python, SQL, Machine Learning
Experience: 3 years

Sample Output Produced
Canonical Profile
{
"candidate_id":"C001"
"links":[]
"experience":[]
"education":[]
"full_name":"Thomas Andrew"
"emails":[
0:"thomasandrew@gmail.com"
]
"phones":[
0:"+919876543210"
]
"_raw_phones":[
0:"9876543210"
]
"headline":"Software Engineer"
"location":"Bangalore, India"
"years_experience":3
"skills":[
0:{
"name":"Python"
"confidence":0.9
"sources":[
0:"ATS"
1:"LinkedIn"
]
}
1:{
"name":"SQL"
"confidence":0.9
"sources":[
0:"ATS"
1:"LinkedIn"
]
}
2:{
"name":"Machine Learning"
"confidence":0.9
"sources":[
0:"ATS"
1:"LinkedIn"
]
}
3:{
"name":"Data Analysis"
"confidence":0.9
"sources":[
0:"ATS"
]
}
]
"provenance":{
"full_name":{
"source":"ATS"
"method":"preferred_source"
"confidence":0.95
}
"emails":{
"source":"ATS"
"method":"direct"
"confidence":0.95
}
"phones":{
"source":"ATS"
"method":"normalized"
"confidence":0.95
}
"headline":{
"source":"LinkedIn"
"method":"direct"
"confidence":0.85
}
"location":{
"source":"LinkedIn"
"method":"direct"
"confidence":0.85
}
"years_experience":{
"source":"ATS"
"method":"preferred_source"
"confidence":0.95
}
"skills":{
"source":"ATS + LinkedIn"
"method":"merged"
"confidence":0.9
"ats_skill_count":4
"linkedin_skill_count":3
}
}
"overall_confidence":0.91
}
Projection Output
{
"candidate_name":"Thomas Andrew"
"primary_email":"thomasandrew@gmail.com"
"skills_count":4
"experience":3
"confidence":0.91
}

Tests Performed
Test 1 – Name Normalization
Input: ANVI S
Output: Anvi S
Result: Passed
Test 2 – Phone Normalization
Input:9896768656
Output:+919896768656
Result: Passed
Test 3– Skill Deduplication
Input:Python, SQL and SQL, AWS
Output: Python, SQL, AWS
Result: Passed
Test 4– Email Normalization
Input:ANVIS1234@GMAIL.COM
Output:anvis1234@gmail.com
Result: Passed

Test 5 – Schema Validation
Generated profile validated successfully against the canonical Pydantic schema.
Result: Passed

Demo link:
https://drive.google.com/file/d/1Q_LfZvgQWyGfU1emGdr7vKWR7d8HN3O-/view?usp=sharing
