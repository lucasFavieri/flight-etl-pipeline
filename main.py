from src.extraction import fetch_flight_data
from src.transformation import transform_flight_data
from src.load import save_to_parquet, upload_to_s3


def run_pipeline():
    """Orchestrates the complete ETL pipeline for flight data over Portugal."""
    print("=" * 50)
    print("STARTING FLIGHT ETL PIPELINE")
    print("=" * 50)

    # 1. EXTRACT
    print("\n[1/4] Extracting raw flight data from OpenSky API...")
    raw_data = fetch_flight_data()

    if not raw_data:
        print("Pipeline aborted: Extraction failed to return data.")
        return

    # 2. TRANSFORM
    print(
        "\n[2/4] Transforming raw flight data into structured DataFrame..."
    )
    df_flights = transform_flight_data(raw_data)

    if df_flights.empty:
        print(
            "Pipeline aborted: Transformation resulted in an empty DataFrame."
        )
        return

    print(f"Transformation successful: {len(df_flights)} flights processed.")

    # 3. LOAD LOCAL
    print("\n[3/4] Saving transformed data to local Parquet storage...")
    saved_path = save_to_parquet(df_flights)

    if not saved_path:
        print("Pipeline failed during local Load step.")
        return

    # 4. LOAD CLOUD (AWS S3)
    print("\n[4/4] Uploading Parquet file to AWS S3...")
    s3_success = upload_to_s3(saved_path)

    if s3_success:
        print("\n" + "=" * 50)
        print("PIPELINE EXECUTED SUCCESSFULLY END-TO-END!")
        print(f"Local File: {saved_path}")
        print("Cloud Storage: AWS S3 Upload Complete")
        print("=" * 50)
    else:
        print("Pipeline failed during AWS S3 upload step.")


if __name__ == "__main__":
    run_pipeline()