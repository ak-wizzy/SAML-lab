saml-lab/
├── app/
│   ├── app.py
│   ├── config.py              # centralised env parsing (new)
│   ├── saml/
│   │   ├── settings.json      # structural SAML config (no secrets)
│   │   └── advanced_settings.json
│   ├── templates/
│   │   ├── base.html          # shared layout (new)
│   │   ├── index.html
│   │   └── claims.html
│   ├── static/                # optional UI assets (future-proof)
│   │   └── styles.css
│   └── requirements.txt
├── .env                      
├── Dockerfile
├── .dockerignore              
└── README.md
