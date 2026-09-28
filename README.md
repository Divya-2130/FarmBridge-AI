# FarmBridge AI — Django Marketplace

A farmer-to-customer digital marketplace with AI-powered demand & price
recommendation. Built as a Django project — you build, migrate, and run it
entirely from the terminal, and it serves a fully styled website.

## Tech Stack
- **Backend:** Python, Django
- **Database:** SQLite by default (zero setup) — swap to MySQL in `farmbridge/settings.py`
- **Frontend:** Django templates, HTML/CSS (custom design system, no framework needed)
- **AI/ML:** Scikit-learn (Linear Regression) for demand prediction + price recommendation
- **Payments:** Razorpay (test mode)
- **Auth:** Django's built-in session auth with a custom `role` field (Farmer/Customer/Admin)

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # for /admin/ and the Admin dashboard

# (optional) train the AI models yourself instead of using the bundled .pkl files
python ai_engine/train_model.py

python manage.py runserver
```

Visit http://127.0.0.1:8000/

- Register as a **Farmer** → submit KYC → (approve it via `/admin-dashboard/`
  using a superuser, or Django admin) → add a Farm via Django admin → add products.
- Register as a **Customer** → browse `/products/` → add to cart → checkout →
  pay (use Razorpay's test keys and test card `4111 1111 1111 1111`).

## Switching to MySQL
1. `pip install mysqlclient`
2. In `farmbridge/settings.py`, comment out the `sqlite3` `DATABASES` block and
   uncomment the MySQL block, filling in your credentials.
3. Create the database: `CREATE DATABASE farmbridge_db;`
4. `python manage.py migrate`

## Project Structure
See the accompanying explanation for what each file does and the pseudocode
behind each module.
