from fastapi import FastAPI
from middleware.middleware import add_middlewares
from api.api import api_router
from core.config import settings
from models.token import Base
# from db.session import engine
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="MACH API")
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