import pandas as pd
import io
from fastapi.responses import StreamingResponse


def df_to_csv_response(df: pd.DataFrame, filename: str = "exported_data.csv"):
    csv_content = df.to_csv(index=False)
    csv_bytes = io.BytesIO(csv_content.encode())

    return StreamingResponse(
        csv_bytes,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
        media_type="text/csv",
    )
