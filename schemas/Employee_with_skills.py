from uuid import UUID
from typing import List
from pydantic import BaseModel
from schemas.employee import EmployeeBase


class SkillBase(BaseModel):
    # id:int
    Python: int
    SQL: int
    Excel: int
    Storyboarding: int
    # Business_Communication: int
    # Deck_Making: int
    # R: int
    # Java: int
    # Javascript: int
    # Shell_scripting: int
    # Ruby: int
    # Scala: int
    # Go: int
    # Rust: int
    # Exploratory_Data_Analysis: int
    # Statistics: int
    # Bayesian_Statistics: int
    # Feature_Engineering: int
    # Feature_Selection: int
    # Modelling_Process: int
    # Causal_Analysis_and_Design_of_Experiments: int
    # Probability: int
    # Linear_Algebra: int
    # Hyperparameters_Tuning: int
    # Dimensionality_Reduction: int
    # Regression: int
    # Clustering: int
    # Time_Series_Analysis: int
    # Classification: int
    # NLP: int
    # Neural_Networks: int
    # Computer_Vision: int
    # Reinforcement_Learning: int
    # Operations_Research: int
    # Self_Supervised_Learning: int
    # Graph_Machine_Learning: int
    # Ethics_in_AI_and_ML: int
    # Information_Extraction: int
    # Anomaly_detection: int
    # Clustering_theory: int
    # Knowledge_Graphs: int
    # Optimization: int
    # Tableau: int
    # PowerBi: int
    # Looker: int
    # Rshiny: int
    # Microstrategy: int
    # Grafana: int
    # QlikView: int
    # QlikSense: int
    # AWS_QuickSight: int
    # AWS: int
    # Azure: int
    # GCP: int
    # Design_Thinking: int
    # SDLC_process: int
    # Testing_LifeCycle: int
    # Project_Management: int
    # Requirements_Gathering: int
    # Rally: int
    # Agile_model_of_development: int
    # FAST_API: int
    # Flask: int
    # Angular: int
    # HTML_CSS: int
    # NodeJS: int
    # Go_Lang: int
    # Django: int
    # Next_JS: int
    # Vue_JS: int
    # React_JS: int
    # ArgoCD: int
    # Azure_DevOps: int
    # GitHub: int
    # GitLab: int
    # GoCD: int
    # GCP_Cloud_Build: int
    # Jenkins: int
    # AWS_CodePipeline_CodeBuild_CodeDeploy: int
    # Informatica: int
    # Talend: int
    # Pentaho: int
    # SSIS: int
    # AirByte: int
    # NiFi2: int
    # Fivetran: int
    # Matillion: int
    # Airflow: int
    # AWS_Glue: int
    # AWS_Step_Functions: int
    # Azure_Data_Factory: int
    # Google_Cloud_Composer: int
    # Nifi: int
    # Oozie: int
    # Data_Modelling: int
    # System_Architecture_Design: int
    # Network_Architecture_Design: int
    # Databricks: int
    # Datalake_S3_ADLS_GCS: int
    # Batch_Data_pipeline: int
    # Streaming_Data_Pipeline: int
    # Data_Storage: int
    # Azure_SQL_DB: int
    # DB2: int
    # MySQL: int
    # Oracle: int
    # SQL_Server: int
    # PostgreSQL: int
    # Hive2: int
    # Azure_Synapse_Analysis: int
    # Google_BigQuery: int
    # AWS_Redshift: int
    # Snowflake: int
    # MongoDB: int
    # CouchBase: int
    # Azure_Cosmos_DB: int
    # AWS_DynamoDB: int
    # GCP_Firestore_BigTable: int
    # Hbase: int
    # Hadoop: int
    # Hive: int
    # Pig: int
    # Kafka: int
    # PySpark: int
    # Sqoop: int
    # IOT: int
    # Docker: int
    # Terraform: int
    # Kubernetes: int
    # Podman: int
    # Ansible: int
    # Chef: int
    # Azure_Bicep: int
    # Azure_ARM: int
    # Adobe_Analytics: int
    # Matomo: int
    # Google_Analytics: int
    # Azure_ML_Studio: int
    # AWS_Sagemaker: int
    # Dataiku: int
    # DataRobot: int
    # GCP_Vertex_AI: int
    # MLFlow: int
    # Kubeflow: int
    # Seldon_Core: int
    # Fiddler: int
    # BentoML: int
    # BDD: int
    # TDD: int
    # Postman: int
    # SonarQube: int
    # Jmeter: int
    # Cucumber: int
    # TestRail: int
    # Pytest_unittest: int
    # Mocha_Chai: int
    # Jasmine: int
    # Alation: int
    # Atlan: int
    # Azure_Purview: int
    # Great_Expectations: int
    # Collibra: int
    # ADLS_Gen2: int
    # AWS_S3: int
    # HDFS: int
    # GCP_Cloud_Storage: int
    # Redis: int
    # Memcached: int
    # Apache_Beam: int
    # Apache_Flink: int
    # Spark_Streaming: int
    # GCP_Dataflow: int
    # GCP_Pub_Sub: int
    # Azure_Event_Hub: int
    # AWS_Kinesis: int
    # Azure_Stream_Analytics: int
    # Apache_Kafka: int
    # UX_research: int
    # UX_design: int
    # UI_design: int
    # Prototyping: int
    # Video_creation: int
    # UX_writing: int
    # Graphic_Design: int
    # Value_Communication_Design: int
    # Figma: int
    # Adobe_Illustrator: int
    # Adobe_Photoshop: int
    # Adobe_Premier_Pro: int
    # Adobe_After_Effects: int
    # Automobile: int
    # Banking: int
    # CPG: int
    # Hospitality: int
    # Insurance: int
    # Healthcare_Pharma: int
    # Retail: int
    # Technology: int
    # Renewable_Energy: int
    # Telecom: int
    # Strategy_Planning: int
    # Pricing_Revenue_Management: int
    # Growth_Marketing_Sales: int
    # Logistics_Supply_Chain: int
    # Merchandising_Store_Ops: int
    # Digital: int
    # Consumer_Insights: int
    # Deep_Learning: int
    # Agile_Scrum: int
    # Agile_Kanban: int
    # PM_Tools_JIRA: int
    # GCP_Pub_Sub2: int
    # Scrum: int
    # Application_CI_CD: int
    # ETL_ELT: int
    # asp_skills: int
    # Discipline_Integrity: int
    # Initiative_Ownership: int
    # Adaptability: int
    # Teamwork: int
    # Innovative_Thinking: int
    # Curiosity_Learning_Agility: int
    # Problem_Solving: int
    # ResultOrientation: int
    # QualityFocus: int
    # EffectiveCommunication: int
    # WorkManagementAndEffectiveness: int
    # ClientCentric: int
    # GenAI: int
    # NucliOS: int


    class Config:
        orm_mode = True


class EmployeeWithSkills(BaseModel):
    user_id:UUID 
    name: str
    designation: str
    account: str
    lead: str
    manager_name: str
    skills: List[SkillBase]