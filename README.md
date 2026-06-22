# YDA Cleaning — Static Website Scaffold

This folder contains a simple static website scaffold for a cleaning company.

Files added:

- `index.html` — homepage
- `about.html`, `services.html`, `contact.html`, `privacy.html` — pages
- `css/style.css` — styles
- `assets/logo.svg` — placeholder logo

To view the site locally, open `index.html` in your browser. For a simple local server run:

```bash
# from this folder
python3 -m http.server 8000
# then open http://localhost:8000 in your browser
```

This folder now also contains a minimal Django project. To run the Django site locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# open http://127.0.0.1:8000
```

Notes:
- The Django app `core` serves the same pages as the static scaffold.
- Contact form logs submissions to the console; configure an email backend for production.

Next steps: customize copy, replace logo/images, and configure a real contact backend or form provider.

Database & Admin
-----------------
- Create migrations and apply them:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Email configuration
-------------------
By default the project uses Django's console email backend (prints to console). To send real email set environment variables before running:

```bash
export DJANGO_SECRET_KEY="your-secret"
export DJANGO_DEBUG=0
export DJANGO_ALLOWED_HOSTS=yourdomain.com
export DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
export EMAIL_HOST=smtp.example.com
export EMAIL_PORT=587
export EMAIL_HOST_USER=your-smtp-user
export EMAIL_HOST_PASSWORD=your-smtp-pass
export EMAIL_USE_TLS=True
export DJANGO_DEFAULT_FROM="no-reply@yourdomain.com"
```

SendGrid Web API (optional)
---------------------------
The project will automatically use the SendGrid Web API if you set `SENDGRID_API_KEY` in the environment. No further code changes are required; the SendGrid path is a best-effort fallback and otherwise the configured Django email backend is used.

```bash
export SENDGRID_API_KEY="SG.xxxxx"
export DJANGO_DEFAULT_FROM="no-reply@yourdomain.com"
```

Exporting enquiries
-------------------
- From the admin UI select enquiries and choose **Export selected enquiries as CSV** to download a CSV file.
- Or run the management command to export all enquiries:

```bash
python manage.py export_enquiries --output all-enquiries.csv
```

Spam protection & client validation
----------------------------------
- The contact form includes a hidden "honeypot" field named `phone`. If that field is filled the submission is silently dropped as likely spam.
- Basic client-side validation is included in `static/js/form.js`. It validates required fields and a simple email pattern before submitting.

Continuous Integration
----------------------
- A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run migrations and tests on pushes and pull requests. Configure the repository and branch names as needed.

Deployment
----------
- To deploy on Render/Heroku or most PaaS providers, set the environment variables above and use the provided `Procfile` or `Dockerfile`.
- For Docker-based deploys:

```bash
docker build -t ydauto .
docker run -p 8000:8000 \
	-e DJANGO_SECRET_KEY=... -e DJANGO_DEBUG=0 -e DJANGO_ALLOWED_HOSTS=... \
	ydauto
```

Docker Compose (Postgres)
-------------------------
You can run the application locally with Postgres using `docker-compose`:

```bash
docker-compose build
docker-compose up -d
# then open http://localhost:8000
```

The compose file creates a `db` Postgres service and a `web` service. In production, override the secrets and use a managed Postgres.

