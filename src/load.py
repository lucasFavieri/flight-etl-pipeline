import os
from datetime import datetime
import pandas as pd
import boto3
from dotenv import load_dotenv

# Loads the environment variables from the .env file.
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# ------------------------ Load -------------------------- #

# ------------- Local -------------- #

def save_to_parquet(df, base_path="data/processed"):
    
    # 1. Validation: Ensure the input is a non-empty Pandas DataFrame
    if not isinstance(df, pd.DataFrame) or df.empty:
        print("Warning: Empty or invalid DataFrame. Nothing to save.")
        return None

    try:
        # 2. Folder Creation: Create target directory if it does not exist
        os.makedirs(base_path, exist_ok=True)

        # 3. Path & Naming: Generate a unique, timestamped filename
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"flights_{now}.parquet"
        complete_path = os.path.join(base_path, file_name)

        # 4. Save & Convert: Write the DataFrame to Parquet using PyArrow
        df.to_parquet(complete_path, engine="pyarrow", index=False)

        print(f"Success! File saved in: {complete_path}")
        return complete_path

    except Exception as e:
        print(f"Error saving Parquet file: {e}")
        return None

# ------------- Local -------------- #


# ------------- AWS -------------- #

def upload_to_s3(file_path: str, object_name: str = None) -> bool:
    """Uploads a local file to an AWS S3 bucket."""
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Cria o cliente de ligação à AWS usando boto3
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    try:
        print(f"Uploading {file_path} to s3 (bucket: {AWS_BUCKET_NAME})...")
        s3_client.upload_file(file_path, AWS_BUCKET_NAME, object_name)
        print(f"File successfully uploaded to s3://{AWS_BUCKET_NAME}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading file to s3: {e}")
        return False

# ------------- AWS -------------- #

# ------------------------ Load -------------------------- #

# ------------------------ Entrypoint -------------------------- #

if __name__ == "__main__":
    print("Testing load module...")
    sample_data = pd.DataFrame(
        [{"icao24": "abc123", "callsign": "TAP123", "origin_country": "Portugal"}]
    )

    # 1. Test local save
    saved_path = save_to_parquet(sample_data)

    # 2. Test S3 upload using the generated local file
    if saved_path:
        upload_to_s3(saved_path)