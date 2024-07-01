import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.session import SessionLocal
import uuid
from models.Employee import MACH_Employee
from models.skills import Skills1

# def load_csv_to_db(csv_file: str, model, db_session: Session):
#     df = pd.read_csv(csv_file)
#     for index, row in df.iterrows():
#         row_dict = row.to_dict()
        
#         # Ensure user_id is a UUID
#         if 'user_id' in row_dict:
#             row_dict['user_id'] = uuid.UUID(row_dict['user_id'])
        
#         # Adjust column names to match the model's attributes
#         adjusted_row_dict = {}
#         for key, value in row_dict.items():
#             if key.lower() in model.__dict__:
#                 adjusted_row_dict[key.lower()] = value
#             else:
#                 # Find the matching column property name
#                 for prop in model.__mapper__.iterate_properties:
#                     if hasattr(prop, 'columns'):
#                         column = prop.columns[0]
#                         if column.name == key:
#                             adjusted_row_dict[prop.key] = value
#                             break
        
#         # Check for existing record to avoid unique constraint violations
#         existing_instance = db_session.query(model).filter_by(user_id=adjusted_row_dict['user_id']).first()
#         if existing_instance:
#             print(f"Record with user_id {adjusted_row_dict['user_id']} already exists in {model.__tablename__}. Skipping insertion.")
#             continue
        
#         # Create model instance and add to session
#         try:
#             instance = model(**adjusted_row_dict)
#             db_session.add(instance)
#         except TypeError as e:
#             print(f"An error occurred when creating an instance of {model.__name__}: {e}")
#             continue
    
#     try:
#         db_session.commit()
#     except IntegrityError as e:
#         db_session.rollback()
#         print(f"An error occurred during commit: {e}")

# # Usage example
# if __name__ == "__main__":
#     db_session = SessionLocal()
#     load_csv_to_db('employees.csv', MACH_Employee, db_session)

#     # Load Skills1 data
#     load_csv_to_db("skills1.csv", Skills1, db_session)

#     db_session.close()
def load_csv_to_db(csv_file: str, model, db_session: Session):
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        
        # Ensure user_id is a UUID
        if 'EMP ID' in row_dict:
            row_dict['user_id'] = row_dict['EMP ID']
        
        # Default submitter_id to 1 if not present
        if 'submitted_by' not in row_dict:
            row_dict['submitter_id'] = "user"
        
        # Adjust column names to match the model's attributes
        adjusted_row_dict = {}
        for key, value in row_dict.items():
            if key.lower() in model.__dict__:
                adjusted_row_dict[key.lower()] = value
            else:
                # Find the matching column property name
                for prop in model.__mapper__.iterate_properties:
                    if hasattr(prop, 'columns'):
                        column = prop.columns[0]
                        if column.name == key:
                            adjusted_row_dict[prop.key] = value
                            break
        
        # Check for existing record to avoid unique constraint violations
        existing_instance = db_session.query(model).filter_by(user_id=adjusted_row_dict['user_id']).first()
        if existing_instance:
            print(f"Record with user_id {adjusted_row_dict['user_id']} already exists in {model.__tablename__}. Skipping insertion.")
            continue
        
        # Create model instance and add to session
        try:
            instance = model(**adjusted_row_dict)
            db_session.add(instance)
        except TypeError as e:
            print(f"An error occurred when creating an instance of {model.__name__}: {e}")
            continue
    
    try:
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        print(f"An error occurred during commit: {e}")

# Usage example
if __name__ == "__main__":
    db_session = SessionLocal()
    load_csv_to_db('new_data3.csv', MACH_Employee, db_session)

    # Load Skills1 data
    load_csv_to_db("new_data1.csv", Skills1, db_session)

    db_session.close()
