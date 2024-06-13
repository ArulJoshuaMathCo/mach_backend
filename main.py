from fastapi import FastAPI
from middleware.middleware import add_middlewares
from api.api_v1.api import api_router



app = FastAPI()
add_middlewares(app)

app.include_router(api_router)
'''
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.Employee import MACH_Employee,Base
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Load the CSV file
csv_file_path = 'mach_employee_202406132135.csv'
df = pd.read_csv(csv_file_path)

from db.session import engine
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

logger.info(f"CSV loaded with {len(df)} rows.")

# Update records with values from the CSV
try:
    for index, row in df.iterrows():
        
        # Assuming the CSV has 'user_id' and 'latest' columns
        user_id = row['user_id']
        latest_value = row['latest']

        # Log the current operation
        # logger.info(f"Processing row {index + 1}: user_id={user_id}, latest={latest_value}")

        # Find the employee by user_id
        employee = session.query(MACH_Employee).filter(MACH_Employee.user_id == user_id).one_or_none()

        if employee:
            # Update the 'latest' column
            employee.latest = latest_value
            # logger.info(f"Updated user_id={user_id} with latest={latest_value}.")
        else:
            logger.warning(f"No employee found with user_id={user_id}")

        # Commit after every update to avoid locking issues
    session.commit()
    logger.info("All changes committed successfully.")

except Exception as e:
    # Log the exception
    logger.error(f"Error processing row {index + 1}: {e}")
    # Rollback in case of error
    session.rollback()

# Close the session
finally:
    session.close()
logger.info("Database update completed.")
'''


#
# from fastapi import FastAPI, APIRouter, Request, Depends
# from sqlalchemy.orm import Session
# import crud
# from api import deps
# from models.skills import Base
# from db.session import engine
# Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()

# # Read data from CSV and insert into the database
# # with open('users.csv', 'r') as file:
# #     reader = csv.DictReader(file)
# #     for row in reader:
# #         employee = MACH_Employee(
# #             name=row['name'],
# #             designation=row['designation'],
# #             account=row['account'],
# #             lead=row['mathco_lead'],
# #             manager_name=row['manager_name']
# #         )
# #         session.add(employee)

# session.commit()
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# employees = session.query(MACH_Employee).all()
# employee_iter = iter(employees)

# expected_columns = [
#      "Python","SQL","Excel","Storyboarding","Business Communication","Deck Making","R","Java","Javascript","Shell scripting","Ruby","Scala","Go","Rust","Exploratory Data Analysis","Statistics","Bayesian Statistics","Feature Engineering","Feature Selection","Modelling Process","Causal Analysis & Design of Experiments","Probability","Linear Algebra","Hyperparameters Tuning","Dimensionality Reduction","Regression","Clustering","Time Series Analysis","Classification","NLP","Neural Networks","Computer Vision","Reinforcement Learning","Operations Research","Self-Supervised Learning","Graph Machine Learning","Ethics in AI & ML","Information Extraction","Anomaly detection","Clustering theory","Knowledge Graphs","Optimization","Tableau","PowerBi","Looker","Rshiny","Microstrategy","Grafana","QlikView","QlikSense","AWS QuickSight","AWS","Azure","GCP","Design Thinking","SDLC process","Testing LifeCycle","Project Management","Requirements Gathering","Rally","Agile model of development","FAST API","Flask","Angular","HTML/CSS","NodeJS","Go Lang","Django","Next JS","Vue JS","React JS","ArgoCD","Azure DevOps","GitHub","GitLab","GoCD","GCP Cloud Build","Jenkins","AWS (CodePipeline, CodeBuild, CodeDeploy)","Informatica","Talend","Pentaho","SSIS","AirByte","NiFi2","Fivetran","Matillion","Airflow","AWS Glue","AWS Step Functions","Azure Data Factory","Google Cloud Composer","Nifi","Oozie","Data Modelling","System Architecture Design","Network Architecture Design","Databricks","Datalake (S3, ADLS, GCS)","Batch Data pipeline","Streaming Data Pipeline","Data Storage","Azure SQL DB","DB2","MySQL","Oracle","SQL Server","PostgreSQL","Hive2","Azure Synapse Analysis","Google BigQuery","AWS Redshift","Snowflake","MongoDB","CouchBase","Azure Cosmos DB","AWS DynamoDB","GCP Firestore/BigTable","Hbase","Hadoop","Hive","Pig","Kafka","PySpark","Sqoop","IOT","Docker","Terraform","Kubernetes","Podman","Ansible","Chef","Azure Bicep","Azure ARM","Adobe Analytics","Matomo","Google Analytics","Azure ML Studio","AWS Sagemaker","Dataiku","DataRobot","GCP Vertex AI","MLFlow","Kubeflow","Seldon Core","Fiddler","BentoML","BDD","TDD","Postman","SonarQube","Jmeter","Cucumber","TestRail","Pytest/unittest","Mocha/Chai","Jasmine","Alation","Atlan","Azure Purview","Great Expectations","Collibra","ADLS Gen2","AWS S3","HDFS","GCP Cloud Storage","Redis","Memcached","Apache Beam","Apache Flink","Spark Streaming","GCP Dataflow","GCP Pub-Sub","Azure Event Hub","AWS Kinesis","Azure Stream Analytics","Apache Kafka","UX research","UX design","UI design","Prototyping","Video creation","UX writing","Graphic Design","Value Communication Design","Figma","Adobe Illustrator","Adobe Photoshop","Adobe Premier Pro","Adobe After Effects","Automobile","Banking","CPG","Hospitality","Insurance","Healthcare & Pharma","Retail","Technology","Renewable Energy","Telecom","Strategy & Planning","Pricing & Revenue Management","Growth, Marketing & Sales","Logistics & Supply Chain","Merchandising & Store Ops","Digital","Consumer Insights","Deep Learning","Agile: Scrum","Agile: Kanban","PM Tools: JIRA","GCP Pub/Sub","scrum","Application CI/CD","ETL / ELT","asp_skills","Discipline & Integrity","Initiative & Ownership","Adaptability","Teamwork","Innovative Thinking","Curiosity & Learning Agility","Problem Solving","Result Orientation","Quality Focus","Effective Communication","Work Management and effectiveness","ClientCentric","GenAI","NucliOS"
# ]

# # # Read skills data from CSV and insert into the database
# with open('skills1.csv', 'r') as file:
#     reader = csv.DictReader(file)
    
#     # Ensure the CSV has the expected columns
#     if not all(column in reader.fieldnames for column in expected_columns):
#         logger.error("CSV file does not contain the expected columns")
#         exit(1)
    
#     for row in reader:
#         # Assign user_id from employees if not present in CSV
#         user_id = row.get('user_id')
#         if not user_id:
#             try:
#                 user_id = next(employee_iter).user_id
#             except StopIteration:
#                 logger.error("Not enough employees to assign user_id")
#                 continue

#         skill = Skill(user_id=user_id)  # Use UUID directly if provided, otherwise assigned from employee
#         for column in expected_columns:
#             if column == 'user_id':
#                 continue  # Skip user_id as it's already set
#             if hasattr(skill, column):
#                 value = row.get(column)
#                 try:
#                     # Convert value to float
#                     float_value = float(value) if value else 0.0
#                     setattr(skill, column, float_value)
#                 except ValueError as e:
#                     logger.error(f"Invalid value for {column}: {value} ({e})")
#                     setattr(skill, column, 0.0)
#                     # continue  # Skip setting this attribute
#         session.add(skill)

# session.commit()
# session.close()
# app.include_router(user_router, prefix="/users")






# @app.get("/")
# async def root():
#     return {"message": "Welcome to the FastAPI application!"}
    