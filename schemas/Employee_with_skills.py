from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel
from schemas.employee import EmployeeBase


class SkillBase(BaseModel):
    Python: Optional[int] = None
    SQL: Optional[int]= None
    Excel:Optional[int]= None
    Storyboarding:Optional[int]= None
    BusinessCommunication: Optional[int]= None
    # Deck_Making: Optional[int] = None
    # R: Optional[int] = None
    # Java: Optional[int] = None
    # Javascript: Optional[int] = None
    # Shell_scripting: Optional[int] = None
    # Ruby: Optional[int] = None
    # Scala: Optional[int] = None
    # Go: Optional[int] = None
    # Rust: Optional[int] = None
    # Exploratory_Data_Analysis: Optional[int] = None
    # Statistics: Optional[int] = None
    # Bayesian_Statistics: Optional[int] = None
    # Feature_Engineering: Optional[int] = None
    # Feature_Selection: Optional[int] = None
    # Modelling_Process: Optional[int] = None
    # Causal_Analysis_Design_of_Experiments: Optional[int] = None
    # Probability: Optional[int] = None
    # Linear_Algebra: Optional[int] = None
    # Hyperparameters_Tuning: Optional[int] = None
    # Dimensionality_Reduction: Optional[int] = None
    # Regression: Optional[int] = None
    # Clustering: Optional[int] = None
    # Time_Series_Analysis: Optional[int] = None
    # Classification: Optional[int] = None
    # NLP: Optional[int] = None
    # Neural_Networks: Optional[int] = None
    # Computer_Vision: Optional[int] = None
    # Reinforcement_Learning: Optional[int] = None
    # Operations_Research: Optional[int] = None
    # Self_Supervised_Learning: Optional[int] = None
    # Graph_Machine_Learning: Optional[int] = None
    # Ethics_in_AI_ML: Optional[int] = None
    # Information_Extraction: Optional[int] = None
    # Anomaly_detection: Optional[int] = None
    # Clustering_theory: Optional[int] = None
    # Knowledge_Graphs: Optional[int] = None
    # Optimization: Optional[int] = None
    # Tableau: Optional[int] = None
    # PowerBi: Optional[int] = None
    # Looker: Optional[int] = None
    # Rshiny: Optional[int] = None
    # Microstrategy: Optional[int] = None
    # Grafana: Optional[int] = None
    # QlikView: Optional[int] = None
    # QlikSense: Optional[int] = None
    # AWS_QuickSight: Optional[int] = None
    # AWS: Optional[int] = None
    # Azure: Optional[int] = None
    # GCP: Optional[int] = None
    # Design_Thinking: Optional[int] = None
    # SDLC_process: Optional[int] = None
    # Testing_LifeCycle: Optional[int] = None
    # Project_Management: Optional[int] = None
    # Requirements_Gathering: Optional[int] = None
    # Rally: Optional[int] = None
    # Agile_model_of_development: Optional[int] = None
    # FAST_API: Optional[int] = None
    # Flask: Optional[int] = None
    # Angular: Optional[int] = None
    # HTML_CSS: Optional[int] = None
    # NodeJS: Optional[int] = None
    # Go_Lang: Optional[int] = None
    # Django: Optional[int] = None
    # Next_JS: Optional[int] = None
    # Vue_JS: Optional[int] = None
    # React_JS: Optional[int] = None
    # ArgoCD: Optional[int] = None
    # Azure_DevOps: Optional[int] = None
    # GitHub: Optional[int] = None
    # GitLab: Optional[int] = None
    # GoCD: Optional[int] = None
    # GCP_Cloud_Build: Optional[int] = None
    # Jenkins: Optional[int] = None
    # AWS_CodePipeline_CodeBuild_CodeDeploy: Optional[int] = None
    # Informatica: Optional[int] = None
    # Talend: Optional[int] = None
    # Pentaho: Optional[int] = None
    # SSIS: Optional[int] = None
    # AirByte: Optional[int] = None
    # NiFi2: Optional[int] = None
    # Fivetran: Optional[int] = None
    # Matillion: Optional[int] = None
    # Airflow: Optional[int] = None
    # AWS_Glue: Optional[int] = None
    # AWS_Step_Functions: Optional[int] = None
    # Azure_Data_Factory: Optional[int] = None
    # Google_Cloud_Composer: Optional[int] = None
    # Nifi: Optional[int] = None
    # Oozie: Optional[int] = None
    # Data_Modelling: Optional[int] = None
    # System_Architecture_Design: Optional[int] = None
    # Network_Architecture_Design: Optional[int] = None
    # Databricks: Optional[int] = None
    # Datalake_S3_ADLS_GCS: Optional[int] = None
    # Batch_Data_pipeline: Optional[int] = None
    # Streaming_Data_Pipeline: Optional[int] = None
    # Data_Storage: Optional[int] = None
    # Azure_SQL_DB: Optional[int] = None
    # DB2: Optional[int] = None
    # MySQL: Optional[int] = None
    # Oracle: Optional[int] = None
    # SQL_Server: Optional[int] = None
    # PostgreSQL: Optional[int] = None
    # Hive2: Optional[int] = None
    # Azure_Synapse_Analysis: Optional[int] = None
    # Google_BigQuery: Optional[int] = None
    # AWS_Redshift: Optional[int] = None
    # Snowflake: Optional[int] = None
    # MongoDB: Optional[int] = None
    # CouchBase: Optional[int] = None
    # Azure_Cosmos_DB: Optional[int] = None
    # AWS_DynamoDB: Optional[int] = None
    # GCP_Firestore_BigTable: Optional[int] = None
    # Hbase: Optional[int] = None
    # Hadoop: Optional[int] = None
    # Hive: Optional[int] = None
    # Pig: Optional[int] = None
    # Kafka: Optional[int] = None
    # PySpark: Optional[int] = None
    # Sqoop: Optional[int] = None
    # IOT: Optional[int] = None
    # Docker: Optional[int] = None
    # Terraform: Optional[int] = None
    # Kubernetes: Optional[int] = None
    # Podman: Optional[int] = None
    # Ansible: Optional[int] = None
    # Chef: Optional[int] = None
    # Azure_Bicep: Optional[int] = None
    # Azure_ARM: Optional[int] = None
    # Adobe_Analytics: Optional[int] = None
    # Matomo: Optional[int] = None
    # Google_Analytics: Optional[int] = None
    # Azure_ML_Studio: Optional[int] = None
    # AWS_Sagemaker: Optional[int] = None
    # Dataiku: Optional[int] = None
    # DataRobot: Optional[int] = None
    # GCP_Vertex_AI: Optional[int] = None
    # MLFlow: Optional[int] = None
    # Kubeflow: Optional[int] = None
    # Seldon_Core: Optional[int] = None
    # Fiddler: Optional[int] = None
    # BentoML: Optional[int] = None
    # BDD: Optional[int] = None
    # TDD: Optional[int] = None
    # Postman: Optional[int] = None
    # SonarQube: Optional[int] = None
    # Jmeter: Optional[int] = None
    # Cucumber: Optional[int] = None
    # TestRail: Optional[int] = None
    # Pytest_unittest: Optional[int] = None
    # Mocha_Chai: Optional[int] = None
    # Jasmine: Optional[int] = None
    # Alation: Optional[int] = None
    # Atlan: Optional[int] = None
    # Azure_Purview: Optional[int] = None
    # Great_Expectations: Optional[int] = None
    # Collibra: Optional[int] = None
    # ADLS_Gen2: Optional[int] = None
    # AWS_S3: Optional[int] = None
    # HDFS: Optional[int] = None
    # GCP_Cloud_Storage: Optional[int] = None
    # Redis: Optional[int] = None
    # Memcached: Optional[int] = None
    # Apache_Beam: Optional[int] = None
    # Apache_Flink: Optional[int] = None
    # Spark_Streaming: Optional[int] = None
    # GCP_Dataflow: Optional[int] = None
    # GCP_Pub_Sub: Optional[int] = None
    # Azure_Event_Hub: Optional[int] = None
    # AWS_Kinesis: Optional[int] = None
    # Azure_Stream_Analytics: Optional[int] = None
    # Apache_Kafka: Optional[int] = None
    # UX_research: Optional[int] = None
    # UX_design: Optional[int] = None
    # UI_design: Optional[int] = None
    # Prototyping: Optional[int] = None
    # Video_creation: Optional[int] = None
    # UX_writing: Optional[int] = None
    # Graphic_Design: Optional[int] = None
    # Value_Communication_Design: Optional[int] = None
    # Figma: Optional[int] = None
    # Adobe_Illustrator: Optional[int] = None
    # Adobe_Photoshop: Optional[int] = None
    # Adobe_Premier_Pro: Optional[int] = None
    # Adobe_After_Effects: Optional[int] = None
    # Automobile: Optional[int] = None
    # Banking: Optional[int] = None
    # CPG: Optional[int] = None
    # Hospitality: Optional[int] = None
    # Insurance: Optional[int] = None
    # Healthcare_Pharma: Optional[int] = None
    # Retail: Optional[int] = None
    # Technology: Optional[int] = None
    # Renewable_Energy: Optional[int] = None
    # Telecom: Optional[int] = None
    # Strategy_Planning: Optional[int] = None
    # Pricing_Revenue_Management: Optional[int] = None
    # Growth_Marketing_Sales: Optional[int] = None
    # Logistics_Supply_Chain: Optional[int] = None
    # Merchandising_Store_Ops: Optional[int] = None
    # Digital: Optional[int] = None
    # Consumer_Insights: Optional[int] = None
    # Deep_Learning: Optional[int] = None
    # Agile_Scrum: Optional[int] = None
    # Agile_Kanban: Optional[int] = None
    # PM_Tools_JIRA: Optional[int] = None
    # GCP_Pub_Sub: Optional[int] = None
    # scrum: Optional[int] = None
    # Application_CI_CD: Optional[int] = None
    # ETL_ELT: Optional[int] = None
    # asp_skills: Optional[int] = None
    # Discipline_Integrity: Optional[int] = None
    # Initiative_Ownership: Optional[int] = None
    # Adaptability: Optional[int] = None
    # Teamwork: Optional[int] = None
    # Innovative_Thinking: Optional[int] = None
    # Curiosity_Learning_Agility: Optional[int] = None
    # Problem_Solving: Optional[int] = None
    # Result_Orientation: Optional[int]
    # Quality_Focus: Optional[int]
    # Effective_Communication: Optional[int]
    # Work_Management_effectiveness: Optional[int]
    # ClientCentric: Optional[int]
    GenAI: Optional[int]= None
    NucliOS: Optional[int]= None


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