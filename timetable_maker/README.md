# Timetable as YAML

## Development Environment

- Python 3.8.6
- Using `venv`

```
(venv) $ pip install -r requirements.txt
```

If you want to dump to Google Spreadsheet, you have to setup Sheets API.  
Get *service account* referring to https://gspread.readthedocs.io/en/latest/oauth2.html.

## Usage

For detail, type `python main.py -h`.

```
(venv) $ python main.py sample.yml \
    --step_min 5 \
    to_sheet <spreadsheet ID> \
    <service account JSON path> \
    --output_worksheet_name awesome_timetable
```

If you want to dump to csv file, specify `to_csv` instead of `to_sheet`.
