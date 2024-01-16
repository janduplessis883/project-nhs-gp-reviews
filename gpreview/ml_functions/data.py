import pandas as pd


def preprocess_dataframe(df):
    df.rename(
        columns={
            "Vaccination type": "vaccine",
            "Event date": "timestamp",
            "Patient ID": "pt_id",
            "Date of birth": "dob",
            "Event done at ID": "location",
            "Patient Count": "pt_count",
        },
        inplace=True,
    )
    df.dropna(subset="location", inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d-%b-%Y")
    df["dob"] = pd.to_datetime(df["dob"], format="%d-%b-%Y")
    df["age_at_vaccine"] = df["timestamp"].dt.year - df["dob"].dt.year
    df = df[df["age_at_vaccine"] > 0]
    # Update the ODE code to the most frequent
    df.drop(columns=["dob", "vaccine"], inplace=True)
    return df
