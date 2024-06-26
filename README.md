Make sure your directory looks like this for full functionality

receipt_manager/
├── app.py
├── database.py
├── instance/
│   └── receipts.db  # Automatically created by Flask when using SQLite
├── static/
│   └── styles.css
└── templates/
    ├── home.html
    └── receipt/
        ├── create.html
        ├── detail.html
        ├── list.html
        └── delete.html
