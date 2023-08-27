import pandas as pd
import io
from fastapi.responses import StreamingResponse, Response


def df_to_csv_response(df: pd.DataFrame, filename: str = "exported_data.csv"):
    csv_content = df.to_csv(index=False)
    # csv_bytes = io.BytesIO(csv_content.encode())

    response = StreamingResponse(
        io.StringIO(df.to_csv(index=False)), media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"

    # return StreamingResponse(
    #     csv_bytes,
    #     headers={"Content-Disposition": f"attachment; filename={filename}"},
    #     media_type="text/csv",
    # )

    return response
