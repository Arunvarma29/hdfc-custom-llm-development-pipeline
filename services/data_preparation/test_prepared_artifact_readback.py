from io import BytesIO

import pandas as pd

from services.database.app.config import settings
from services.data_preparation.app.artifacts.prepared_artifact import client


ARTIFACT_BASE = (
    "prepared/"
    "9afaef5e-cf87-42a6-9901-5b3693e3d418/"
    "1.0.0/"
    "65eb10bb-6f92-4f27-a1e1-2f5165f62ac6"
)


def read_parquet(object_key: str) -> pd.DataFrame:
    response = client.get_object(
        bucket_name=settings.minio_bucket,
        object_name=object_key,
    )

    try:
        data = response.read()
    finally:
        response.close()
        response.release_conn()

    return pd.read_parquet(
        BytesIO(data),
        engine="pyarrow",
    )


train = read_parquet(
    f"{ARTIFACT_BASE}/train.parquet"
)

validation = read_parquet(
    f"{ARTIFACT_BASE}/validation.parquet"
)

test = read_parquet(
    f"{ARTIFACT_BASE}/test.parquet"
)


print("Train records:", len(train))
print("Validation records:", len(validation))
print("Test records:", len(test))

print("\nTrain columns:")
print(list(train.columns))

print("\nFirst train record:")
print(train.iloc[0].to_dict())

print("\nPrivacy verification:")

for field in ["customer_name", "customer_contact"]:
    if field not in train.columns:
        raise ValueError(
            f"Sensitive field missing: {field}"
        )

    values = train[field].dropna().astype(str)

    if field == "customer_name":
        invalid = values[
            ~values.str.startswith("CUSTOMER_NAME_")
        ]
    else:
        invalid = values[
            ~values.str.startswith("CUSTOMER_CONTACT_")
        ]

    if not invalid.empty:
        raise ValueError(
            f"Privacy check failed for {field}: "
            f"{invalid.iloc[0]}"
        )

    print(f"{field}: PASS")

total = (
    len(train)
    + len(validation)
    + len(test)
)

print("\nTotal records:", total)
if len(train) != 800:
    raise ValueError("Train artifact count mismatch")

if len(validation) != 100:
    raise ValueError(
        "Validation artifact count mismatch"
    )

if len(test) != 100:
    raise ValueError("Test artifact count mismatch")

if total != 1000:
    raise ValueError(
        "Total artifact count mismatch"
    )

print("\nPrepared artifact read-back successful")