# Python as MTG secretary

Include the following:

- script to schedule Zoom meetings

## Development environment

- macOS
- Python 3.8.6
- Using `venv`

```
(venv) $ pip install -r requirements.txt
```

## Settings in Zoom

Create a **JWT App** in Zoom.  
ref: https://marketplace.zoom.us/docs/guides/build/jwt-app

Please write down **API Key** and **API Secret** in the App Credentials.

## Precondition: Create `.env`

The contents of `.env` is the following:

```
export ZOOM_JWT_APP_API_KEY="<Your Zoom JWT App API Key>"
export ZOOM_JWT_APP_API_SECRET="<Your Zoom JWT App API Secret>"
```

Location:

```
.
├── .env  # 👈 DON'T FORGET TO CREATE
├── README.md
├── requirements.txt
├── schedule_zoom_mtg.py
└── venv
```

## Usage

Before running the script, do `source .env` to load environment variables.

For detail, type `python schedule_zoom_mtg.py -h`.

```
(venv) $ python schedule_zoom_mtg.py 03-15 19:30 2 'Awesome meeting'
```
