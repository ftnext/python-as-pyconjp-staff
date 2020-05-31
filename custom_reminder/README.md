Custom Slack Reminder which will **automatically stop**.

## Requirements

### Service account (Sheets API)

need to add editor of the target spreadsheet.

file placement at Lambda console (browser)

```
.
├── lambda_function.py
└── sa_pyconjp_auto_stuff.json
```

### Environment variables

- `SPREAD_ID`
- `SLACK_BOT_USER_TOKEN`
