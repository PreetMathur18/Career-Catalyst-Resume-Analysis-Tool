import streamlit as st
import subprocess
import nltk
import spacy
from spacy.matcher import PhraseMatcher
nltk.download('stopwords')
# from spacy.cli import download

# Download the model if not already downloaded
# download('en_core_web_sm-2.3.1')

# Load the model
# nlp = spacy.load('en_core_web_sm-2.3.1')
# nlp=spacy.load('en_core_web_sm-2.3.1')

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')
# from spacy.cli import download

# # Download the SpaCy model if not already downloaded
# download('en_core_web_sm')


# Load the SpaCy model
# nlp = spacy.load('en_core_web_sm')
# import fitz
# from PyPDF2 import PdfFileReader
from streamlit.components.v1 import html
import pandas as pd
import base64, random
import time, datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io, random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, cyber_course, software_course, database_course, hci_course, robot_course, cc_course, game_course, bio_course, ds_recommended_skills,web_recommended_skills,android_recommended_skills,ios_recommended_skills,uiux_recommended_skills,cyber_recommended_skills, software_recommended_skills,database_recommended_skills,hci_recommended_skills,robot_recommended_skills,cc_recommended_skills,game_recommended_skills,bio_recommended_skills 
#resume_videos, interview_videos
import pafy
import plotly.express as px
import youtube_dl
# import yt_dlp as youtube_dl


def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title


def get_table_download_link(df, filename, text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>"""
    st.markdown(pdf_display, unsafe_allow_html=True)
# def show_pdf(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#     html(pdf_display, height=1000, width=700, scrolling=True)


# def show_pdf(file_path):
#     pdf_images = convert_from_path(file_path)

#     for i, image in enumerate(pdf_images):
#         image_bytes = image.convert("RGB").tobytes()
#         encoded_image = base64.b64encode(image_bytes).decode("utf-8")
#         st.image(f"data:image/png;base64,{encoded_image}", caption=f"Page {i+1}", use_column_width=True)

# def course_recommender(course_list):
#     st.subheader("**Courses & Certificates🎓 Recommendations**")
#     c = 0
#     rec_course = []
#     no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
#     random.shuffle(course_list)
#     for c_name, c_link in course_list:
#         c += 1
#         st.markdown(f"({c}) [{c_name}]({c_link})")
#         rec_course.append(c_name)
#         if c == no_of_reco:
#             break
#     return rec_course
def course_recommender(course_list, unique_key):
    st.markdown("<h1 style='text-decoration: underline; font-size: 25px;'>Courses & Certificates🎓 Recommendations</h1>", unsafe_allow_html=True)
    # st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    no_of_reco = st.slider(f'Choose Number of Course Recommendations:', 1, 10, 4, key=f'slider_{unique_key}')
    random.shuffle(course_list)
    rec_course = []

    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break

    return rec_course

connection = pymysql.connect(host='mysql-38506d7c-kashyap-f2fe.a.aivencloud.com', user='avnadmin', password='AVNS_K7131xonxcfemuBFLVh', database='defaultdb', port=15380)
cursor = connection.cursor()


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills,
                courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (
    name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills,
    courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

# def insert_data(name, email, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
#     # Your existing insert_data function remains the same
#     DB_table_name = 'user_data'
#     insert_sql = "insert into " + DB_table_name + """
#     values (0,%s,%s,%s,%s,%s,%s,%s,%s)"""
#     rec_values = (
#     name, email, str(no_of_pages), reco_field, cand_level, skills, recommended_skills,
#     courses)
#     cursor.execute(insert_sql, rec_values)
#     connection.commit()

# def saved_first(res_score, timestamp):
#     # Your existing saved_first function remains the same
#     DB_table_name = 'user_data'
#     insert_sql = "insert into " + DB_table_name + """
#     values (0,%s,%s)"""
#     rec_values = (
#     str(res_score), timestamp)
#     cursor.execute(insert_sql, rec_values)
#     connection.commit()

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon='./Logo/SRA_Logo.ico',

)


def run():
    st.title("Career Catalyst")
    st.sidebar.markdown("# Choose User")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    # st.sidebar.markdown(link, unsafe_allow_html=True)
    img = Image.open('./Logo/SRA_Logo.jpg')
    img = img.resize((800, 425))
    st.image(img)

    # Create the DB
    # db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    # cursor.execute(db_sql)
    # connection.select_db("sra")

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(500) NOT NULL,
                     Recommended_skills VARCHAR(500) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    if choice == 'Normal User':
        # st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Upload your resume, and get recommendation based on it."</h4>''',
        #             unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #d73b5c;'>Choose your Resume</h1>", unsafe_allow_html=True)
        # Use the file uploader
        pdf_file = st.file_uploader(" ", type=["pdf"])
        # pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            # with st.spinner('Uploading your Resume....'):
            #     time.sleep(4)
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            # show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello " + resume_data['name'])
                st.markdown("<h1 style='text-decoration: underline; font-size: 30px;'>Your Basic info</h1>", unsafe_allow_html=True)
                # st.subheader("**Your Basic info**")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                                unsafe_allow_html=True)
                    

                # st.markdown("<h1 style='text-decoration: underline; font-size: 30px;'>Skills Recommendation💡</h1>", unsafe_allow_html=True)
                # st.subheader("**Skills Recommendation💡**")
                ## Skill shows
                keywords = st_tags(label='### Skills that you have',
                                   text='See our skills recommendation',
                                   value=resume_data['skills'], key='1')

                ##  recommendation
            
                ds_keyword= ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                            'streamlit', 'Data Analytics','Quantitative Analysis''Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                            'Data Mining', 'Clustering & Classification',
                            'Web Scraping', 'ML Algorithms', 'Keras',
                            'Probability', 'Scikit-learn', 
                            'Machine Leaning','AI','Matplotlib']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy',  'Java',  'SDK', 'SQLite']
                ios_keyword= ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword=['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                'user research', 'user experience']
                cyber_keyword=['Network Security','Penetration Testing','Security Architecture','Risk Assessment','Ethical Hacking','Cryptographic Protocols','Firewall Management','Network Security','Penetration Testing','Security Architecture','Risk Assessment','Ethical Hacking','Cryptographic Protocols','Firewall','cybersecurity','Security risk management','problem solving']
                software_keyword=['Software Development Life Cycle','Software Engineering','Software Architecture','Software Development Life Cycle','Software Engineering','Software Architecture','Software Testing','Software Maintenance','Agile/Scrum methodologies','Software Testing']
                database_keyword=['SQL','Mysql','Database Management Systems','Database Design','Database Administration','Data Modeling','NoSQL','Database Management']
                hci_keyword=['Human Computer Interaction','User Experience','Usability','Interaction Design','HCI','User interface (UI) design']
                robot_keyword=['Robotics','Robotics Programming','Control Systems','Robotics Control']
                cc_keyword=['Azure','Google Cloud','cloud','AWS','IaaS','PaaS','SaaS','DevOps','Cloud Storage','Linux','Python','Distributed computing','Virtualization','Scalability','Fault tolerance']
                game_keyword=['C++','Java','Unity','Unreal Engine ',' Godot','GameMaker','JavaScript','HTML5','CSS3','OpenGL',' DirectX','Vulkan','Lua','game development','game engine programming','game physics','artificial intelligence in games','Visulisation']
                bio_keyword=["Genomics","Computational Biology","Genomic data analysis","Computational biology","Sequence alignment algorithms","Biostatistics","Bioinformatics tools and databases"]

                domain_info = {
                    'Data Science': {'keywords': ds_keyword, 'recommended_skills': ds_recommended_skills,'courses': ds_course},
                    'Cloud Computing and Distributed Systems':{'keywords':cc_keyword,'recommended_skills':cc_recommended_skills, 'courses': cc_course},
                    'Web Development': {'keywords': web_keyword, 'recommended_skills': web_recommended_skills, 'courses': web_course},
                    'Database Management and Systems':{'keywords':database_keyword,'recommended_skills':database_recommended_skills, 'courses': database_course},
                    'Android Development':{'keywords':android_keyword,'recommended_skills':android_recommended_skills, 'courses': android_course},
                    'IOS Development':{'keywords':ios_keyword,'recommended_skills':ios_recommended_skills, 'courses': ios_course},
                    'UI-UX Development':{'keywords':uiux_keyword,'recommended_skills':uiux_recommended_skills, 'courses': uiux_course},
                    'Cybersecurity and Network Security':{'keywords':cyber_keyword,'recommended_skills':cyber_recommended_skills, 'courses': cyber_course},
                    'Software Engineering and Development':{'keywords':software_keyword,'recommended_skills':software_recommended_skills, 'courses': software_course},
                    'Human-Computer Interaction':{'keywords':hci_keyword,'recommended_skills':hci_recommended_skills, 'courses': hci_course},
                    'Robotics and Control Systems':{'keywords':robot_keyword,'recommended_skills':robot_recommended_skills, 'courses': robot_course},
                    'Game Development':{'keywords':game_keyword,'recommended_skills':game_recommended_skills, 'courses': game_course},
                    'Bioinformatics':{'keywords':bio_keyword,'recommended_skills':bio_recommended_skills, 'courses': bio_course}
                }
                def identify_domains(doc):
                    reco_fields = []
                    predicted_domains = []

                    for domain_label, domain_data in domain_info.items():
                        # Convert keywords to lowercase and strip whitespace
                        keywords = [kw.strip().lower() for kw in domain_data['keywords']]
                        # Create patterns for each keyword
                        patterns = [nlp(keyword) for keyword in keywords]
                        # Iterate over each skill in the resume
                        for skill in resume_data['skills']:
                            # Process the skill using spaCy's nlp pipeline
                            skill_doc = nlp(skill)
                            
                            # Check if the skill matches any keyword in the domain
                            if any(skill_doc.similarity(pattern) > 0.7 for pattern in patterns) and domain_label not in predicted_domains:
                                reco_fields.append(domain_label)
                                predicted_domains.append(domain_label)
                                print(f"Skill: {skill}, Domain: {domain_label}")
                                # st.success(f"**Our analysis says you are looking for {domain_label} Jobs.**")
                    return reco_fields

                # def identify_domains(doc):
                #     reco_fields = []
                #     predicted_domains = []

                #     for domain_label, domain_data in domain_info.items():
                #         # Convert keywords to lowercase and strip whitespace
                #         keywords = [kw.strip().lower() for kw in domain_data['keywords']]

                #         # Iterate over each skill in the resume
                #         for skill in resume_data['skills']:
                #             # Convert skill to lowercase and strip whitespace
                #             skill_lower = skill.strip().lower()

                #             # Check if the skill matches any keyword in the domain
                #             if any(keyword in skill_lower for keyword in keywords) and domain_label not in predicted_domains:
                #                 reco_fields.append(domain_label)
                #                 predicted_domains.append(domain_label)
                #                 print(f"Skill: {skill_lower}, Domain: {domain_label}")
                #                 # st.success(f"**Our analysis says you are looking for {domain_label} Jobs.**")

                #     # Add similar print statements elsewhere in your code to identify potential issues.

                #     return reco_fields

                # def identify_domains(doc):
                #     matcher = PhraseMatcher(nlp.vocab)
                #     reco_fields = []
                #     predicted_domains = []

                #     for domain_label, domain_data in domain_info.items():
                #         keywords = domain_data['keywords']
                #         patterns = [nlp(keyword) for keyword in keywords]
                #         matcher.add(domain_label, None, *patterns)

                #     matches = matcher(doc)

                #     # Inside identify_domains function
                #     for _, start, end in matches:
                #         matched_text = doc[start:end].text.lower()
                #         print(f"Matched: {matched_text}")

                #         for domain_label, domain_data in domain_info.items():
                #             if matched_text in [kw.strip().lower() for kw in domain_data['keywords']] and domain_label not in predicted_domains:
                #                 reco_fields.append(domain_label)
                #                 predicted_domains.append(domain_label)
                #                 print(f"Domain: {domain_label}")
                #                 # st.success(f"**Our analysis says you are looking for {domain_label} Jobs.**")

                #     # Add similar print statements elsewhere in your code to identify potential issues.

                #     return reco_fields
                # def identify_domains(doc):
                #     reco_fields = []
                #     predicted_domains = []

                #     for domain_label, domain_data in domain_info.items():
                #         # Convert keywords to lowercase and strip whitespace
                #         keywords = [kw.strip().lower() for kw in domain_data['keywords']]
                #         # Create patterns for each keyword
                #         patterns = [nlp(keyword) for keyword in keywords]

                #         # Iterate over each skill in the resume
                #         for skill in resume_data['skills']:
                #             # Process the skill using spaCy's nlp pipeline
                #             skill_doc = nlp(skill)
                            
                #             # Check if the skill matches any keyword in the domain
                #             if any(skill_doc.similarity(pattern) > 0.7 for pattern in patterns) and domain_label not in predicted_domains:
                #                 reco_fields.append(domain_label)
                #                 predicted_domains.append(domain_label)
                #                 print(f"Skill: {skill}, Domain: {domain_label}")
                #                 # st.success(f"**Our analysis says you are looking for {domain_label} Jobs.**")

                #     # Add similar print statements elsewhere in your code to identify potential issues.

                #     return reco_fields
                st.markdown("<h1 style='text-decoration: underline; font-size: 30px;'>Analysis and Predictions 🤔</h1>", unsafe_allow_html=True)
                # st.subheader("**Skills Recommendation💡**")
                recommended_skills = None
                key_counter = 2
                data_saved = False
                rec_course = None  
                doc = nlp(" ".join(resume_data['skills']))

                # Identify relevant domains
                reco_fields = identify_domains(doc)
                if not reco_fields:
                    st.error("No relevant domains identified.")
                    reco_field = ""  # Assign an empty string to reco_field
                else:
                    reco_field = reco_fields[0]  # Use the first predicted domain
                for reco_field in reco_fields:
                    key_counter += 1  # Reset the key counter for each domain
                    st.success(f"**_Our analysis says you are looking for {reco_field} Jobs._**")
                    # Display recommended skills using st_tags
                    domain_data = domain_info[reco_field]
                    # Main Streamlit app
                    st.markdown("<h1 style='text-decoration: underline; font-size: 25px;'>Skills Recommendation💡</h1>", unsafe_allow_html=True)
                    recommended_keywords = st_tags(label=f'##### Recommended skills for you in {reco_field}.',
                                                text='Recommended skills generated from System',
                                                value=domain_data['recommended_skills'], key=str(key_counter))

                    st.markdown(
                        f'''<h4 style='text-align: left; color: #7E92F3;font-size: 22px;'>Adding these skills to your resume will boost🚀 the chances of getting a {reco_field} Job💼</h4>''',
                        unsafe_allow_html=True)

                    # Get course recommendations for the specific domain
                    rec_course = course_recommender(domain_data.get('courses', []), unique_key=f"{reco_field}_{key_counter}")
                    # rec_course = course_recommender(domain_data['courses'], unique_key=f"{reco_field}_{key_counter}")
                    st.write(" \n\n")
                    st.write(" \n\n")
                    st.write(" \n\n")
                    st.write(" \n\n")
                    # if key_counter == 3 and not data_saved:  # Change the condition to key_counter == 3 for the first prediction
                    #     insert_data(
                    #         resume_data['name'],
                    #         resume_data['email'],
                    #         resume_data['no_of_pages'],
                    #         reco_fields[0],  # Use the first predicted domain
                    #         cand_level,
                    #         resume_data['skills'],
                    #         recommended_skills,
                    #         rec_course
                    #     )
                    #     data_saved = True
                    # Now, you can save the prediction using the save_prediction_to_database function
                    # save_prediction_to_database(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, rec_course)





                # def identify_domains(doc):
                #     matcher = PhraseMatcher(nlp.vocab)
                #     reco_fields = []
                #     predicted_domains = []

                #     print(f"SpaCy Version: {spacy.__version__}")
                #     print(f"Loaded SpaCy Model: {nlp.meta['name']}")

                #     for domain_label, domain_data in domain_info.items():
                #         keywords = domain_data['keywords']
                #         patterns = [nlp(keyword) for keyword in keywords]
                #         matcher.add(domain_label, None, *patterns)

                #     matches = matcher(doc)

                #     # Inside identify_domains function
                #     for _, start, end in matches:
                #         matched_text = doc[start:end].text.lower()
                #         print(f"Matched: {matched_text}")

                #         for domain_label, domain_data in domain_info.items():
                #             if matched_text in [kw.strip().lower() for kw in domain_data['keywords']] and domain_label not in predicted_domains:
                #                 reco_fields.append(domain_label)
                #                 predicted_domains.append(domain_label)
                #                 print(f"Domain: {domain_label}")
                #                 st.success(f"**Our analysis says you are looking for {domain_label} Jobs.**")

                #     # Add similar print statements elsewhere in your code to identify potential issues.

                #     return reco_fields


                # def identify_domains(doc):
                #     matcher = PhraseMatcher(nlp.vocab)
                #     reco_field = ''
                #     predicted_domains = []

                #     for domain_label, domain_data in domain_info.items():
                #         keywords = domain_data['keywords']
                #         patterns = [nlp(keyword) for keyword in keywords]
                #         matcher.add(domain_label, None, *patterns)

                #     matches = matcher(doc)

                #     for _, start, end in matches:
                #         matched_text = doc[start:end].text.lower()
                #         for domain_label, domain_data in domain_info.items():
                #             if matched_text in domain_data['keywords'] and domain_label not in predicted_domains:
                #                 reco_field = domain_label
                #                 predicted_domains.append(domain_label)
                #                 st.success(f"** Our analysis says you are looking for {domain_label} Jobs.**")
                #                 # Additional operations with reco_field if needed

                #     return reco_field

                # recommended_skills = []
                # # reco_fields = []
                # rec_courses = []
                # # key_counter = 2
                # # predicted_domains = []
                

                # doc = nlp(" ".join(resume_data['skills']))  # Assuming skills are stored in a list

                # # Identify relevant domains
                # reco_fields = identify_domains(doc)
                # # print(f"Final reco_field: {reco_fields}")


                # # Display all recommended courses
                # for rec_course in rec_courses:
                #     for domain, courses in rec_course.items():
                #         st.write(f"Recommended Courses for {domain}: {courses}")

                # for reco_field in reco_fields:
                #     key_counter = 2  # Reset the key counter for each domain

                #     if reco_field in domain_info:
                #         key_counter += 1  # Increment the key counter for each widget
                #         st.success(f"** Our analysis says you are looking for {reco_field} Jobs.**")

                #         # Get the information for the specific domain
                #         domain_data = domain_info[reco_field]

                #         # Display recommended skills using st_tags
                #         recommended_keywords = st_tags(label=f'#### Recommended skills for you in {reco_field}.',
                #                                     text='Recommended skills generated from System',
                #                                     value=domain_data['recommended_skills'], key=str(key_counter))

                #         st.markdown(
                #             f'''<h4 style='text-align: left; color: #7E92F3;'>Adding these skills to your resume will boost🚀 the chances of getting a {reco_field} Job💼</h4>''',
                #             unsafe_allow_html=True)

                #         # Get course recommendations for the specific domain
                #         rec_course = course_recommender(domain_data['courses'], unique_key=reco_field)
                #         rec_courses.append({reco_field: rec_course})



                # # Perform domain-specific operations
                # for reco_field in reco_fields:
                #     st.markdown("<h1 style='text-decoration: underline; font-size: 30px;'>Skills Recommendation💡</h1>",
                #                 unsafe_allow_html=True)
                #     st.subheader(f"**Skills Recommendation for {reco_field} 💡**")
                #     key_counter = 2  # Reset the key counter for each domain

                #     if reco_field in domain_info:
                #         st.success(f"** Our analysis says you are looking for {reco_field} Jobs.**")

                #         # Get the information for the specific domain
                #         domain_data = domain_info[reco_field]

                #         # Display recommended skills using st_tags
                #         recommended_keywords = st_tags(label=f'#### Recommended skills for you in {reco_field}.',
                #                                     text='Recommended skills generated from System',
                #                                     value=domain_data['recommended_skills'], key=reco_field)

                #         st.markdown(
                #             f'''<h4 style='text-align: left; color: #7E92F3;'>Adding these skills to your resume will boost🚀 the chances of getting a {reco_field} Job💼</h4>''',
                #             unsafe_allow_html=True)

                #         # Get course recommendations for the specific domain
                #         rec_course = course_recommender(domain_data['courses'])
                #         rec_courses.append({reco_field: rec_course})

                # # Display all recommended courses
                # for rec_course in rec_courses:
                #     for domain, courses in rec_course.items():
                #         st.write(f"Recommended Courses for {domain}: {courses}")
                # domain_keywords = [(ds_keyword, 'Data Science'), (web_keyword, 'Web Development'),(android_keyword,'Android Development'),(ios_keyword,'IOS Development'),(uiux_keyword,'UI-UX Development'),(cyber_keyword,'Cybersecurity and Network Security'),(software_keyword,'Software Engineering and Development'),(database_keyword,'Database Management and Systems'),(hci_keyword,'Human-Computer Interaction'),(robot_keyword,'Robotics and Control Systems'),(cc_keyword,'Cloud Computing and Distributed Systems'),(game_keyword,'Game Development'),(bio_keyword,'Bioinformatics')]
                # def identify_domains(doc):
                #     matcher = PhraseMatcher(nlp.vocab)
                #     reco_field = ''
                #     predicted_domains = []

                #     for keywords, domain_label in domain_keywords:
                #         patterns = [nlp(keyword) for keyword in keywords]
                #         matcher.add(domain_label, None, *patterns)

                #     matches = matcher(doc)

                #     for _, start, end in matches:
                #         matched_text = doc[start:end].text.lower()
                #         for keywords, domain_label in domain_keywords:
                #             if matched_text in keywords and domain_label not in predicted_domains:
                #                 reco_field = domain_label
                #                 predicted_domains.append(domain_label)
                #                 st.success(f"** Our analysis says you are looking for {domain_label} Jobs.**")
                #                 # Additional operations with reco_field if needed

                #     return reco_field
                # recommended_skills = []
                # reco_field = ''
                # rec_course = ''
                # key_counter = 2
                # predicted_domains = []
                # for i in resume_data['skills']:
                #     relevant_domains = []

                #     for keywords, domain_label in domain_keywords:
                #         if i.lower() in keywords and domain_label not in predicted_domains:
                #             relevant_domains.append(domain_label)
                #             predicted_domains.append(domain_label)

                #     if relevant_domains:
                #         for domain_label in relevant_domains:
                #             key_counter += 1  # Increment the key counter for each widget
                #             reco_field = domain_label
                #             st.success(f"** Our analysis says you are looking for {domain_label} Jobs.**")



                # # Replace the dummy course data with your actual course data
                # ds_course = {'ds_course': [('Data Science Course 1', 'https://course-link-1.com'), ('Data Science Course 2', 'https://course-link-2.com')]}
                # web_course = {'web_course': [('Web Development Course 1', 'https://course-link-1.com'), ('Web Development Course 2', 'https://course-link-2.com')]}
                # # Add other domain course data...
                
                # Function to recommend courses for a specific domain

                # Function to identify domains based on skills
                # ## Define a list of tuples, where each tuple contains the keywords and the domain label
                # domain_keywords = [(ds_keyword, 'Data Science'), (web_keyword, 'Web Development'),(android_keyword,'Android Development'),(ios_keyword,'IOS Development'),(uiux_keyword,'UI-UX Development'),(cyber_keyword,'Cybersecurity and Network Security'),(software_keyword,'Software Engineering and Development'),(database_keyword,'Database Management and Systems'),(hci_keyword,'Human-Computer Interaction'),(robot_keyword,'Robotics and Control Systems'),(cc_keyword,'Cloud Computing and Distributed Systems'),(game_keyword,'Game Development'),(bio_keyword,'Bioinformatics')]
                # # Add tuples for other domains...

                # recommended_skills = []
                # reco_field = ''
                # rec_course = ''
                # key_counter = 2
                # predicted_domains = []

                # for i in resume_data['skills']:
                #     relevant_domains = []
                #     # Iterate through the list of domain keywords and labels
                #     # for keywords, domain_label in domain_keywords:
                #     #     if i.lower() in keywords:
                #     #         print(i.lower())
                #     #         reco_field = domain_label
                #     #         st.success(f"** Our analysis says you are looking for {domain_label} Jobs.**")
                #     for keywords, domain_label in domain_keywords:
                #         if i.lower() in keywords and domain_label not in predicted_domains:
                #             print(i.lower())
                #             relevant_domains.append(domain_label)
                #             predicted_domains.append(domain_label) 

                    # if relevant_domains:
                    #     for domain_label in relevant_domains:
                    #         key_counter += 1  # Increment the key counter for each widget
                    #         reco_field = domain_label
                    #         st.success(f"** Our analysis says you are looking for {domain_label} Jobs.**")

                    #         # Generate recommendations for the specific domain
                    #         if domain_label == 'Data Science':
                    #             recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                    #                                 'Data Mining', 'Clustering & Classification', 'Data Analytics',
                    #                                 'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                    #                                 'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                    #                                 'Streamlit']
                    #         elif domain_label == 'Web Development':
                    #             recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento','wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                    #         elif domain_label == 'Android Development':
                    #             recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java','Kivy', 'GIT', 'SDK', 'SQLite']
                    #         elif domain_label == 'IOS Development':
                    #             recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode','Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation','Auto-Layout']
                    #         elif domain_label == 'UI-UX Development':
                    #             recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq','Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing','Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe','Solid', 'Grasp', 'User Research']
                    #         elif domain_label == 'Cybersecurity and Network Security':
                    #             recommended_skills = ["Ethical hacking","Network security protocols","Intrusion detection systems","Cryptography","Security risk management"]
                    #         elif domain_label == 'Software Engineering and Development':
                    #             recommended_skills = ["Software development methodologies","Version control systems","Testing and debugging","Agile/Scrum methodologies"]
                    #         elif domain_label == 'Database Management and Systems':
                    #             recommended_skills = ["Database design","SQL","NoSQL","Database administration","Data modeling","Query optimization"]
                    #         elif domain_label == 'Human-Computer Interaction':
                    #             recommended_skills = ["User experience (UX) design","User interface (UI) design","Usability testing","Interaction design","Psychology and human behavior understanding"]
                    #         elif domain_label == 'Robotics and Control Systems':
                    #             recommended_skills = ["Robotics programming","Control systems theory","Kinematics and dynamics","Sensor integration","Motion planning","Robot control"]
                    #         elif domain_label == 'Cloud Computing and Distributed Systems':
                    #             recommended_skills = ["Cloud platforms (AWS, Azure, Google Cloud)","Distributed computing","Virtualization","Scalability","Fault tolerance"]
                    #         elif domain_label == 'Game Development':
                    #             recommended_skills = ["Game design","Game engine programming","Game physics","Artificial intelligence in games","Game asset creation"]
                    #         elif domain_label == 'Bioinformatics':
                    #             recommended_skills = ["Genomic data analysis","Computational biology","Sequence alignment algorithms","Biostatistics","Bioinformatics tools and databases"]


                            # # Display recommended skills using st_tags
                            # recommended_keywords = st_tags(label=f'#### Recommended skills for you in {domain_label}.',
                            #                             text='Recommended skills generated from System',
                            #                             value=recommended_skills, key=str(key_counter))

                            # st.markdown(
                            #     f'''<h4 style='text-align: left; color: #7E92F3;'>Adding these skills to your resume will boost🚀 the chances of getting a {domain_label} Job💼</h4>''',
                            #     unsafe_allow_html=True)

                            # # Get course recommendations for the specific domain
                            # # rec_course = course_recommender(ds_course) if domain_label == 'Data Science' else course_recommender(web_course)
                            # if domain_label == 'Data Science':
                            #     rec_course = course_recommender(ds_course, unique_key='ds_course')
                            # elif domain_label == 'Web Development':
                            #     rec_course = course_recommender(web_course, unique_key='web_course')
                            # elif domain_label == 'Android Development':
                            #     rec_course = course_recommender(android_course, unique_key='android_course')
                            # elif domain_label == 'IOS Development':
                            #     rec_course = course_recommender(ios_course, unique_key='ios_course')
                            # elif domain_label == 'UI-UX Development':
                            #     rec_course = course_recommender(uiux_course, unique_key='uiux_course')
                            # elif domain_label == 'Cybersecurity and Network Security':
                            #     rec_course = course_recommender(cyber_course, unique_key='cyber_course')
                            # elif domain_label == 'Software Engineering and Development':
                            #     rec_course = course_recommender(software_course, unique_key='software_course')
                            # elif domain_label == 'Database Management and Systems':
                            #     rec_course = course_recommender(database_course, unique_key='database_course')
                            # elif domain_label == 'Human-Computer Interaction':
                            #     rec_course = course_recommender(hci_course, unique_key='hci_course')
                            # elif domain_label == 'Robotics and Control Systems':
                            #     rec_course = course_recommender(robot_course, unique_key='robot_course')
                            # elif domain_label == 'Cloud Computing and Distributed Systems':
                            #     rec_course = course_recommender(cc_course, unique_key='cc_course')
                            # elif domain_label == 'Game Development':
                            #     rec_course = course_recommender(game_course, unique_key='game_course')
                            # elif domain_label == 'Bioinformatics':
                            #     rec_course = course_recommender(bio_course, unique_key='bio_course')

                            # # If there are multiple domains relevant to the resume, this loop will handle them all
                            # break

                # Display course recommendations based on rec_course
                # ...

                # recommended_skills = []
                # reco_field = ''
                # rec_course = ''
                # ## Courses recommendation
                # for i in resume_data['skills']:
                #     ## Data science recommendation
                #     if i.lower() in ds_keyword:
                #         print(i.lower())
                #         reco_field = 'Data Science'
                #         st.success("** Our analysis says you are looking for Data Science Jobs.**")
                #         recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                #                               'Data Mining', 'Clustering & Classification', 'Data Analytics',
                #                               'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                #                               'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                #                               'Streamlit']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='2')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ds_course)
                #         break

                #     ## Web development recommendation
                #     elif i.lower() in web_keyword:
                #         print(i.lower())
                #         reco_field = 'Web Development'
                #         st.success("** Our analysis says you are looking for Web Development Jobs **")
                #         recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                #                               'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='3')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(web_course)
                #         break

                #     ## Android App Development
                #     elif i.lower() in android_keyword:
                #         print(i.lower())
                #         reco_field = 'Android Development'
                #         st.success("** Our analysis says you are looking for Android App Development Jobs **")
                #         recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                #                               'Kivy', 'GIT', 'SDK', 'SQLite']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='4')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(android_course)
                #         break

                #     ## IOS App Development
                #     elif i.lower() in ios_keyword:
                #         print(i.lower())
                #         reco_field = 'IOS Development'
                #         st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                #         recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                #                               'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                #                               'Auto-Layout']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='5')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break

                #     ## Ui-UX Recommendation
                #     elif i.lower() in uiux_keyword:
                #         print(i.lower())
                #         reco_field = 'UI-UX Development'
                #         st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                #         recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                #                               'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                #                               'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                #                               'Solid', 'Grasp', 'User Research']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='6')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(uiux_course)
                #         break

                #     # Cybersecurity and Network Security
                #     elif i.lower() in cyber_keyword:
                #         print(i.lower())
                #         reco_field = 'Cybersecurity and Network Security'
                #         st.success("** Our analysis says you are looking for  Cybersecurity and Network Security Jobs **")
                #         recommended_skills = ["Ethical hacking","Network security protocols","Intrusion detection systems","Cryptography","Security risk management"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='7')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break
                    
                #     # Software Engineering and Development
                #     elif i.lower() in software_keyword:
                #         print(i.lower())
                #         reco_field = 'Software Engineering and Development'
                #         st.success("** Our analysis says you are looking for Software Engineering and Development Jobs **")
                #         recommended_skills = ["Software development methodologies","Version control systems","Testing and debugging","Agile/Scrum methodologies"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='8')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break
                    
                #     # Database Management and Systems
                #     elif i.lower() in database_keyword:
                #         print(i.lower())
                #         reco_field = 'Database Management and Systems'
                #         st.success("** Our analysis says you are looking for Database Management and Systems Jobs **")
                #         recommended_skills = ["Database design","SQL","NoSQL","Database administration","Data modeling","Query optimization"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='9')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break
                    
                #     # Human-Computer Interaction (HCI)
                #     elif i.lower() in hci_keyword:
                #         print(i.lower())
                #         reco_field = 'Human-Computer Interaction'
                #         st.success("** Our analysis says you are looking for Human-Computer Interaction (HCI) Jobs **")
                #         recommended_skills = ["User experience (UX) design","User interface (UI) design","Usability testing","Interaction design","Psychology and human behavior understanding"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='10')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break


                #     # Robotics and Control Systems
                #     elif i.lower() in robot_keyword:
                #         print(i.lower())
                #         reco_field = 'Robotics and Control Systems'
                #         st.success("** Our analysis says you are looking for Robotics and Control Systems Jobs **")
                #         recommended_skills = ["Robotics programming","Control systems theory","Kinematics and dynamics","Sensor integration","Motion planning","Robot control"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='11')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break


                #     # Cloud Computing and Distributed Systems
                #     elif i.lower() in cc_keyword:
                #         print(i.lower())
                #         reco_field = 'Cloud Computing and Distributed Systems'
                #         st.success("** Our analysis says you are looking for Cloud Computing and Distributed Systems Jobs **")
                #         recommended_skills = ["Cloud platforms (AWS, Azure, Google Cloud)","Distributed computing","Virtualization","Scalability","Fault tolerance"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='12')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break

                #     # Game Developments
                #     elif i.lower() in game_keyword:
                #         print(i.lower())
                #         reco_field = 'Game Development'
                #         st.success("** Our analysis says you are looking for Game Development Jobs **")
                #         recommended_skills = ["Game design","Game engine programming","Game physics","Artificial intelligence in games","Game asset creation"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='13')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break                    

                #     # Bioinformatics
                #     elif i.lower() in bio_keyword:
                #         print(i.lower())
                #         reco_field = 'Bioinformatics'
                #         st.success("** Our analysis says you are looking for Bioinformatics Jobs **")
                #         recommended_skills = ["Genomic data analysis","Computational biology","Sequence alignment algorithms","Biostatistics","Bioinformatics tools and databases"]

                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #                                        text='Recommended skills generated from System',
                #                                        value=recommended_skills, key='14')
                #         st.markdown(
                #             '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                #             unsafe_allow_html=True)
                #         rec_course = course_recommender(ios_course)
                #         break  
                    

                
                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                ### Resume writing recommendation
                st.markdown("<h1 style='text-decoration: underline; font-size: 30px;'>Resume Tips & Ideas💡</h1>", unsafe_allow_html=True)
                # st.subheader("**Resume Tips & Ideas💡**")
                resume_score = 0
                if 'Objective' or 'Summary' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h5>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h5 style='text-align: left; color: #F17878;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h5>''',
                        unsafe_allow_html=True)

                if 'Declaration' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration✍/h5>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h5 style='text-align: left; color: #F17878;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h5>''',
                        unsafe_allow_html=True)

                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies⚽</h5>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h5 style='text-align: left; color: #F17878;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h5>''',
                        unsafe_allow_html=True)

                if 'Achievements' or 'Extra Curricular' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h5>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h5 style='text-align: left; color: #F17878;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h5>''',
                        unsafe_allow_html=True)

                if 'Projects' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects👨‍💻 </h5>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h5 style='text-align: left; color: #F17878;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h5>''',
                        unsafe_allow_html=True)
                st.markdown("<h1 style='text-decoration: underline; font-size: 30px;'>Resume Score📝</h1>", unsafe_allow_html=True)
                # st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)

                st.success('** Your Resume Writing Score: ' + str(score) + '**')
                st.warning(
                    "** Note: This score is calculated based on the content that you have added in your Resume. **")
                st.balloons()
                # saved_first(str(resume_score), timestamp)
                # update_data_in_database(resume_data['name'], str(resume_score), timestamp)
                insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                            str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
                            str(recommended_keywords), str(rec_course))

                ## Resume writing video
                # st.header("**Bonus Video for Resume Writing Tips💡**")
                # resume_vid = random.choice(resume_videos)
                # res_vid_title = fetch_yt_video(resume_vid)
                # st.subheader("✅ **" + res_vid_title + "**")
                # st.video(resume_vid)
                
            
                # ## Interview Preparation Video
                # st.header("**Bonus Video for Interview👨‍💼 Tips💡**")
                # interview_vid = random.choice(interview_videos)
                # int_vid_title = fetch_yt_video(interview_vid)
                # st.subheader("✅ **" + int_vid_title + "**")
                # st.video(interview_vid)

                connection.commit()
            else:
                st.error('Something went wrong..')
    else:
        ## Admin Side
        st.success('Welcome to Admin Side')
        # st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'pari' and ad_password == 'pari123':
                st.success("Welcome Pari")
                # Display Data
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)
                # print("hello",plot_data)

                # Pie chart for predicted field recommendations
                labels = plot_data.Predicted_Field.unique()
                # print(labels)
                values = plot_data.Predicted_Field.value_counts()
                # print(values)
                st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                fig = px.pie(values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                # Pie chart for User's👨‍💻 Experienced Level
                labels = plot_data.User_level.unique()
                values = plot_data.User_level.value_counts()
                st.subheader("**📈  Pie-Chart for User's👨‍💻 Experienced Level**")
                fig = px.pie(values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)


            else:
                st.error("Wrong ID & Password Provided")


run()
