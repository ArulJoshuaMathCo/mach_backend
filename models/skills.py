from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, column_property
from db.base_class import Base
class Skills1(Base):
    # __tablename__ = 'skills'
    user_id = Column(UUID(as_uuid=True), ForeignKey('mach_employee.user_id'), primary_key=True)
    python = column_property(Column("Python", Integer, nullable=False))     
    sql = column_property(Column("SQL", Integer, nullable=False))     
    excel = column_property(Column("Excel", Integer, nullable=False))     
    storyboarding = column_property(Column("Storyboarding", Integer, nullable=False))     
    business_communication = column_property(Column("Business Communication", Integer, nullable=False))     
    deck_making = column_property(Column("Deck Making", Integer, nullable=False))     
    r = column_property(Column("R", Integer, nullable=False))     
    java = column_property(Column("Java", Integer, nullable=False))     
    javascript = column_property(Column("Javascript", Integer, nullable=False))     
    shell_scripting = column_property(Column("Shell scripting", Integer, nullable=False))     
    ruby = column_property(Column("Ruby", Integer, nullable=False))     
    scala = column_property(Column("Scala", Integer, nullable=False))     
    go = column_property(Column("Go", Integer, nullable=False))     
    rust = column_property(Column("Rust", Integer, nullable=False))     
    exploratory_data_analysis = column_property(Column("Exploratory Data Analysis", Integer, nullable=False))    
    statistics = column_property(Column("Statistics", Integer, nullable=False))     
    bayesian_statistics = column_property(Column("Bayesian Statistics", Integer, nullable=False))     
    feature_engineering = column_property(Column("Feature Engineering", Integer, nullable=False))     
    feature_selection = column_property(Column("Feature Selection", Integer, nullable=False))     
    modelling_process = column_property(Column("Modelling Process", Integer, nullable=False))     
    causal_analysis_and_design_of_experiments = column_property(Column("Causal Analysis & Design of Experiments", Integer, nullable=False))     
    probability = column_property(Column("Probability", Integer, nullable=False))     
    linear_algebra = column_property(Column("Linear Algebra", Integer, nullable=False))     
    hyperparameters_tuning = column_property(Column("Hyperparameters Tuning", Integer, nullable=False))     
    dimensionality_reduction = column_property(Column("Dimensionality Reduction", Integer, nullable=False))     
    regression = column_property(Column("Regression", Integer, nullable=False))     
    clustering = column_property(Column("Clustering", Integer, nullable=False))     
    time_series_analysis = column_property(Column("Time Series Analysis", Integer, nullable=False))     
    classification = column_property(Column("Classification", Integer, nullable=False))     
    nlp = column_property(Column("NLP", Integer, nullable=False))     
    neural_networks = column_property(Column("Neural Networks", Integer, nullable=False))     
    computer_vision = column_property(Column("Computer Vision", Integer, nullable=False))     
    reinforcement_learning = column_property(Column("Reinforcement Learning", Integer, nullable=False))     
    operations_research = column_property(Column("Operations Research", Integer, nullable=False))     
    self_supervised_learning = column_property(Column("Self-Supervised Learning", Integer, nullable=False))     
    graph_machine_learning = column_property(Column("Graph Machine Learning", Integer, nullable=False))     
    ethics_in_ai_and_ml = column_property(Column("Ethics in AI & ML", Integer, nullable=False))     
    information_extraction = column_property(Column("Information Extraction", Integer, nullable=False))     
    anomaly_detection = column_property(Column("Anomaly detection", Integer, nullable=False))     
    clustering_theory = column_property(Column("Clustering theory", Integer, nullable=False))     
    knowledge_graphs = column_property(Column("Knowledge Graphs", Integer, nullable=False))     
    optimization = column_property(Column("Optimization", Integer, nullable=False))     
    tableau = column_property(Column("Tableau", Integer, nullable=False))    
    powerbi = column_property(Column("PowerBi", Integer, nullable=False))     
    looker = column_property(Column("Looker", Integer, nullable=False))     
    rshiny = column_property(Column("Rshiny", Integer, nullable=False))     
    microstrategy = column_property(Column("Microstrategy", Integer, nullable=False))     
    grafana = column_property(Column("Grafana", Integer, nullable=False))     
    qlikview = column_property(Column("QlikView", Integer, nullable=False))     
    qliksense = column_property(Column("QlikSense", Integer, nullable=False))     
    aws_quicksight = column_property(Column("AWS QuickSight", Integer, nullable=False))    
    aws = column_property(Column("AWS", Integer, nullable=False))     
    azure = column_property(Column("Azure", Integer, nullable=False))     
    gcp = column_property(Column("GCP", Integer, nullable=False))     
    design_thinking = column_property(Column("Design Thinking", Integer, nullable=False))     
    sdlc_process = column_property(Column("SDLC process", Integer, nullable=False))     
    testing_lifecycle = column_property(Column("Testing LifeCycle", Integer, nullable=False))     
    project_management = column_property(Column("Project Management", Integer, nullable=False))     
    requirements_gathering = column_property(Column("Requirements Gathering", Integer, nullable=False))     
    rally = column_property(Column("Rally", Integer, nullable=False))     
    agile_model_of_development = column_property(Column("Agile model of development", Integer, nullable=False))     
    fast_api = column_property(Column("FAST API", Integer, nullable=False))     
    flask = column_property(Column("Flask", Integer, nullable=False))     
    angular = column_property(Column("Angular", Integer, nullable=False))     
    html_css = column_property(Column("HTML/CSS", Integer, nullable=False))     
    nodejs = column_property(Column("NodeJS", Integer, nullable=False))     
    go_lang = column_property(Column("Go Lang", Integer, nullable=False))     
    django = column_property(Column("Django", Integer, nullable=False))     
    next_js = column_property(Column("Next JS", Integer, nullable=False))    
    vue_js = column_property(Column("Vue JS", Integer, nullable=False))     
    react_js = column_property(Column("React JS", Integer, nullable=False))     
    argocd = column_property(Column("ArgoCD", Integer, nullable=False))     
    azure_devops = column_property(Column("Azure DevOps", Integer, nullable=False))     
    github = column_property(Column("GitHub", Integer, nullable=False))     
    gitlab = column_property(Column("GitLab", Integer, nullable=False))     
    gocd = column_property(Column("GoCD", Integer, nullable=False))     
    gcp_cloud_build = column_property(Column("GCP Cloud Build", Integer, nullable=False))     
    jenkins = column_property(Column("Jenkins", Integer, nullable=False))     
    aws_codepipeline_codebuild_codedeploy = column_property(Column("AWS (CodePipeline, CodeBuild, CodeDeploy)", Integer, nullable=False))     
    informatica = column_property(Column("Informatica", Integer, nullable=False))     
    talend = column_property(Column("Talend", Integer, nullable=False))     
    pentaho = column_property(Column("Pentaho", Integer, nullable=False))     
    ssis = column_property(Column("SSIS", Integer, nullable=False))     
    airbyte = column_property(Column("AirByte", Integer, nullable=False))     
    nifi2 = column_property(Column("NiFi2", Integer, nullable=False))     
    fivetran = column_property(Column("Fivetran", Integer, nullable=False))     
    matillion = column_property(Column("Matillion", Integer, nullable=False))     
    airflow = column_property(Column("Airflow", Integer, nullable=False))     
    aws_glue = column_property(Column("AWS Glue", Integer, nullable=False))     
    aws_step_functions = column_property(Column("AWS Step Functions", Integer, nullable=False))     
    azure_data_factory = column_property(Column("Azure Data Factory", Integer, nullable=False))     
    google_cloud_composer = column_property(Column("Google Cloud Composer", Integer, nullable=False))     
    nifi = column_property(Column("Nifi", Integer, nullable=False))     
    oozie = column_property(Column("Oozie", Integer, nullable=False))     
    data_modelling = column_property(Column("Data Modelling", Integer, nullable=False))     
    system_architecture_design = column_property(Column("System Architecture Design", Integer, nullable=False))     
    network_architecture_design = column_property(Column("Network Architecture Design", Integer, nullable=False))     
    databricks = column_property(Column("Databricks", Integer, nullable=False))     
    datalake_s3_adls_gcs = column_property(Column("Datalake (S3, ADLS, GCS)", Integer, nullable=False))     
    batch_data_pipeline = column_property(Column("Batch Data pipeline", Integer, nullable=False))     
    streaming_data_pipeline = column_property(Column("Streaming Data Pipeline", Integer, nullable=False))     
    data_storage = column_property(Column("Data Storage", Integer, nullable=False))     
    azure_sql_db = column_property(Column("Azure SQL DB", Integer, nullable=False))     
    db2 = column_property(Column("DB2", Integer, nullable=False))     
    mysql = column_property(Column("MySQL", Integer, nullable=False))     
    oracle = column_property(Column("Oracle", Integer, nullable=False))     
    sql_server = column_property(Column("SQL Server", Integer, nullable=False))     
    postgresql = column_property(Column("PostgreSQL", Integer, nullable=False))     
    hive2 = column_property(Column("Hive2", Integer, nullable=False))     
    azure_synapse_analysis = column_property(Column("Azure Synapse Analysis", Integer, nullable=False))     
    google_bigquery = column_property(Column("Google BigQuery", Integer, nullable=False))     
    aws_redshift = column_property(Column("AWS Redshift", Integer, nullable=False))     
    snowflake = column_property(Column("Snowflake", Integer, nullable=False))     
    mongodb = column_property(Column("MongoDB", Integer, nullable=False))     
    couchbase = column_property(Column("CouchBase", Integer, nullable=False))     
    azure_cosmos_db = column_property(Column("Azure Cosmos DB", Integer, nullable=False))     
    aws_dynamodb = column_property(Column("AWS DynamoDB", Integer, nullable=False))     
    gcp_firestore_bigtable = column_property(Column("GCP Firestore/BigTable", Integer, nullable=False))     
    hbase = column_property(Column("Hbase", Integer, nullable=False))     
    hadoop = column_property(Column("Hadoop", Integer, nullable=False))     
    hive = column_property(Column("Hive", Integer, nullable=False))     
    pig = column_property(Column("Pig", Integer, nullable=False))     
    kafka = column_property(Column("Kafka", Integer, nullable=False))     
    pyspark = column_property(Column("PySpark", Integer, nullable=False))     
    sqoop = column_property(Column("Sqoop", Integer, nullable=False))     
    iot = column_property(Column("IOT", Integer, nullable=False))     
    docker = column_property(Column("Docker", Integer, nullable=False))     
    terraform = column_property(Column("Terraform", Integer, nullable=False))     
    kubernetes = column_property(Column("Kubernetes", Integer, nullable=False))     
    podman = column_property(Column("Podman", Integer, nullable=False))     
    ansible = column_property(Column("Ansible", Integer, nullable=False))     
    chef = column_property(Column("Chef", Integer, nullable=False))     
    azure_bicep = column_property(Column("Azure Bicep", Integer, nullable=False))     
    azure_arm = column_property(Column("Azure ARM", Integer, nullable=False))     
    adobe_analytics = column_property(Column("Adobe Analytics", Integer, nullable=False))     
    matomo = column_property(Column("Matomo", Integer, nullable=False))     
    google_analytics = column_property(Column("Google Analytics", Integer, nullable=False))     
    azure_ml_studio = column_property(Column("Azure ML Studio", Integer, nullable=False))     
    aws_sagemaker = column_property(Column("AWS Sagemaker", Integer, nullable=False))     
    dataiku = column_property(Column("Dataiku", Integer, nullable=False))     
    datarobot = column_property(Column("DataRobot", Integer, nullable=False))     
    gcp_vertex_ai = column_property(Column("GCP Vertex AI", Integer, nullable=False))     
    mlflow = column_property(Column("MLFlow", Integer, nullable=False))     
    kubeflow = column_property(Column("Kubeflow", Integer, nullable=False))     
    seldon_core = column_property(Column("Seldon Core", Integer, nullable=False))     
    fiddler = column_property(Column("Fiddler", Integer, nullable=False))     
    bentoml = column_property(Column("BentoML", Integer, nullable=False))     
    bdd = column_property(Column("BDD", Integer, nullable=False))     
    tdd = column_property(Column("TDD", Integer, nullable=False))     
    postman = column_property(Column("Postman", Integer, nullable=False))     
    sonarqube = column_property(Column("SonarQube", Integer, nullable=False))     
    jmeter = column_property(Column("Jmeter", Integer, nullable=False))     
    cucumber = column_property(Column("Cucumber", Integer, nullable=False))     
    testrail = column_property(Column("TestRail", Integer, nullable=False)) 
    pytest_unittest = column_property(Column("Pytest/unittest", Integer, nullable=False)) 
    mocha_chai = column_property(Column("Mocha/Chai", Integer, nullable=False)) 
    jasmine = column_property(Column("Jasmine", Integer, nullable=False)) 
    alation = column_property(Column("Alation", Integer, nullable=False)) 
    atlan = column_property(Column("Atlan", Integer, nullable=False)) 
    azure_purview = column_property(Column("Azure Purview", Integer, nullable=False)) 
    great_expectations = column_property(Column("Great Expectations", Integer, nullable=False)) 
    collibra = column_property(Column("Collibra", Integer, nullable=False)) 
    adls_gen2 = column_property(Column("ADLS Gen2", Integer, nullable=False)) 
    aws_s3 = column_property(Column("AWS S3", Integer, nullable=False)) 
    hdfs = column_property(Column("HDFS", Integer, nullable=False)) 
    gcp_cloud_storage = column_property(Column("GCP Cloud Storage", Integer, nullable=False)) 
    redis = column_property(Column("Redis", Integer, nullable=False)) 
    memcached = column_property(Column("Memcached", Integer, nullable=False)) 
    apache_beam = column_property(Column("Apache Beam", Integer, nullable=False)) 
    apache_flink = column_property(Column("Apache Flink", Integer, nullable=False)) 
    spark_streaming = column_property(Column("Spark Streaming", Integer, nullable=False)) 
    gcp_dataflow = column_property(Column("GCP Dataflow", Integer, nullable=False)) 
    gcp_pub_sub = column_property(Column("GCP Pub-Sub", Integer, nullable=False)) 
    azure_event_hub = column_property(Column("Azure Event Hub", Integer, nullable=False)) 
    aws_kinesis = column_property(Column("AWS Kinesis", Integer, nullable=False)) 
    azure_stream_analytics = column_property(Column("Azure Stream Analytics", Integer, nullable=False)) 
    apache_kafka = column_property(Column("Apache Kafka", Integer, nullable=False)) 
    ux_research = column_property(Column("UX research", Integer, nullable=False)) 
    ux_design = column_property(Column("UX design", Integer, nullable=False)) 
    ui_design = column_property(Column("UI design", Integer, nullable=False)) 
    prototyping = column_property(Column("Prototyping", Integer, nullable=False)) 
    video_creation = column_property(Column("Video creation", Integer, nullable=False)) 
    ux_writing = column_property(Column("UX writing", Integer, nullable=False)) 
    graphic_design = column_property(Column("Graphic Design", Integer, nullable=False)) 
    value_communication_design = column_property(Column("Value Communication Design", Integer, nullable=False)) 
    figma = column_property(Column("Figma", Integer, nullable=False)) 
    adobe_illustrator = column_property(Column("Adobe Illustrator", Integer, nullable=False)) 
    adobe_photoshop = column_property(Column("Adobe Photoshop", Integer, nullable=False)) 
    adobe_premier_pro = column_property(Column("Adobe Premier Pro", Integer, nullable=False)) 
    adobe_after_effects = column_property(Column("Adobe After Effects", Integer, nullable=False)) 
    automobile = column_property(Column("Automobile", Integer, nullable=False)) 
    banking = column_property(Column("Banking", Integer, nullable=False)) 
    cpg = column_property(Column("CPG", Integer, nullable=False)) 
    hospitality = column_property(Column("Hospitality", Integer, nullable=False)) 
    insurance = column_property(Column("Insurance", Integer, nullable=False)) 
    healthcare_and_pharma = column_property(Column("Healthcare & Pharma", Integer, nullable=False)) 
    retail = column_property(Column("Retail", Integer, nullable=False)) 
    technology = column_property(Column("Technology", Integer, nullable=False)) 
    renewable_energy = column_property(Column("Renewable Energy", Integer, nullable=False)) 
    telecom = column_property(Column("Telecom", Integer, nullable=False)) 
    strategy_and_planning = column_property(Column("Strategy & Planning", Integer, nullable=False)) 
    pricing_and_revenue_management = column_property(Column("Pricing & Revenue Management", Integer, nullable=False)) 
    growth_marketing_and_sales = column_property(Column("Growth, Marketing & Sales", Integer, nullable=False)) 
    logistics_and_supply_chain = column_property(Column("Logistics & Supply Chain", Integer, nullable=False)) 
    merchandising_and_store_ops = column_property(Column("Merchandising & Store Ops", Integer, nullable=False)) 
    digital = column_property(Column("Digital", Integer, nullable=False)) 
    consumer_insights = column_property(Column("Consumer Insights", Integer, nullable=False)) 
    deep_learning = column_property(Column("Deep Learning", Integer, nullable=False)) 
    agile_scrum = column_property(Column("Agile: Scrum", Integer, nullable=False)) 
    agile_kanban = column_property(Column("Agile: Kanban", Integer, nullable=False)) 
    pm_tools_jira = column_property(Column("PM Tools: JIRA", Integer, nullable=False)) 
    gcp_pub_sub = column_property(Column("GCP Pub/Sub", Integer, nullable=False)) 
    scrum = column_property(Column("scrum", Integer, nullable=False)) 
    application_ci_cd = column_property(Column("Application CI/CD", Integer, nullable=False)) 
    etl___elt = column_property(Column("ETL / ELT", Integer, nullable=False)) 
    asp_skills = column_property(Column("asp_skills", Integer, nullable=False)) 
    discipline_and_integrity = column_property(Column("Discipline & Integrity", Integer, nullable=False)) 
    initiative_and_ownership = column_property(Column("Initiative & Ownership", Integer, nullable=False)) 
    adaptability = column_property(Column("Adaptability", Integer, nullable=False)) 
    teamwork = column_property(Column("Teamwork", Integer, nullable=False)) 
    innovative_thinking = column_property(Column("Innovative Thinking", Integer, nullable=False)) 
    curiosity_and_learning_agility = column_property(Column("Curiosity & Learning Agility", Integer, nullable=False)) 
    problem_solving = column_property(Column("Problem Solving", Integer, nullable=False)) 
    result_orientation = column_property(Column("Result Orientation", Integer, nullable=False)) 
    quality_focus = column_property(Column("Quality Focus", Integer, nullable=False)) 
    effective_communication = column_property(Column("Effective Communication", Integer, nullable=False)) 
    work_management_and_effectiveness = column_property(Column("Work Management and effectiveness", Integer, nullable=False)) 
    clientcentric = column_property(Column("ClientCentric", Integer, nullable=False)) 
    genai = column_property(Column("GenAI", Integer, nullable=False)) 
    nuclios = column_property(Column("NucliOS", Integer, nullable=False))