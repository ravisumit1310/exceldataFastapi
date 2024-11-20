from starlette.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import io

app = FastAPI()

#Route to upload CSV and extract employee names

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile= File(...)):
    if not (file.filename.endswith(".csv") or file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Only .csv, .xls, and .xlsx files are allowed.")

    try:
        #reading file
        contents = await file.read()

        #condition for csv and excel files
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(".xls") or file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="File not supported.")

        #converting to JSON format
        data_json = df.to_dict(orient="records")
        return data_json
        # return JSONResponse(content=data_json)

    except ImportError as e:
        raise HTTPException(
            status_code=500,
            detail="Missing dependency for Excel files: 'openpyxl'. Install it using `pip install openpyxl`."
        )

    except Exception as err:
        raise HTTPException(status_code = 500, detail=f"Error processing the file: {str(err)}")
