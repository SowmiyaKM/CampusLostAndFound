# CampusConnect — Lost & Found Management System

A complete, production-ready campus Lost & Found platform built with Django. Students report lost or found items, browse and search the campus feed, get automatic potential-match notifications, and manage everything from a personal dashboard. Staff get a customized Django Admin plus an in-app Admin Dashboard with analytics.

## Tech Stack

- **Backend:** Python 3, Django 5.0
- **Database:** SQLite (default, zero-config)
- **Frontend:** Django Templates + vanilla CSS/JavaScript (no build step)
- **Images:** Pillow (for `ImageField` uploads)

## Features

- **Authentication** — student registration/login with custom fields (Student ID, Department, Year, Phone), hashed passwords, editable profile with avatar.
- **Dashboard** — total lost/found/returned stats, recent activity feed, quick-action cards.
- **Report Lost / Found Items** — full forms with category, description, location, date, optional image, optional reward (lost only), contact info. Owners can edit, delete, or mark items as Found/Returned.
- **Search & Filter** — search by name/description, filter by category/location/date, status tabs (Active / Resolved / All), real-time AJAX search in the navbar.
- **Item Details** — large image, full description, posted-by, contact button, "Report Match" button.
- **Matching Engine** — `items/matching.py` compares category + item-name similarity (difflib) between lost and found items and surfaces "Potential Match Found" on detail pages, plus auto-notifications when a new found item matches an existing lost report (and vice versa).
- **Admin Panel** — customized Django Admin (`/admin/`) with list filters, search, bulk "mark as found/returned" actions, plus a branded **Admin Dashboard** (`/admin-dashboard/`) for staff with live analytics tables.
- **Notifications** — toast notifications (success/error/info) for every user action, plus a persistent notification center with unread badges for match alerts, "item returned" confirmations, and admin announcements.
- **Design** — university-themed UI using the specified palette (`#2563EB` / `#0F172A` / `#38BDF8` / `#F8FAFC`), glassmorphism cards, hover animations, responsive navbar with mobile hamburger menu, empty states, and skeleton/spinner loading treatments.

## Project Structure

```
campusconnect/
├── manage.py
├── requirements.txt
├── campusconnect/          # project settings, root urls
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── accounts/                # custom User model, auth, profile
│   ├── models.py  forms.py  views.py  urls.py  admin.py
├── items/                    # lost/found items, matching, notifications
│   ├── models.py  forms.py  views.py  urls.py  admin.py
│   ├── matching.py           # lightweight matching engine
│   ├── context_processors.py # navbar notification badge
├── templates/
│   ├── base.html
│   ├── accounts/ (login, register, profile)
│   └── items/ (home, about, contact, dashboard, lost/found lists,
│               item form, item detail, notifications, admin dashboard, ...)
├── static/
│   ├── css/style.css
│   └── js/main.js
└── media/                     # uploaded images (created at runtime)
```

## Setup & Run Locally

```bash
# 1. Create & activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Create an admin account
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** for the app and **http://127.0.0.1:8000/admin/** for the Django Admin.

> Note: when creating a superuser via `createsuperuser`, Django will only prompt for username/email/password. Log in to `/admin/` afterward and fill in the required `student_id`, `department`, `year`, and `phone` fields on that user, or set them via `python manage.py shell`.

## Database Models

| Model | Key Fields |
|---|---|
| `accounts.User` (extends `AbstractUser`) | `student_id`, `department`, `year`, `phone`, `avatar` |
| `items.LostItem` | `title`, `category`, `description`, `image`, `location`, `date_lost`, `reward`, `contact_info`, `status`, `owner` |
| `items.FoundItem` | `title`, `category`, `description`, `image`, `location`, `date_found`, `contact_info`, `status`, `finder` |
| `items.Notification` | `user`, `message`, `notif_type`, `link`, `is_read`, `created_at` |

## Matching Logic

`items/matching.py` finds candidates in the opposite table with the **same category**, then scores title similarity with Python's `difflib.SequenceMatcher`. Matches above a 0.45 ratio are shown on the item detail page as "Potential Match Found" (with a percentage score) and trigger a notification to the relevant user(s).

## Deployment Notes

- Set `DEBUG = False` and a real `SECRET_KEY` (environment variable) before deploying.
- Set `ALLOWED_HOSTS` to your domain.
- Run `python manage.py collectstatic` and serve `STATIC_ROOT` / `MEDIA_ROOT` via your web server or a storage backend (e.g. WhiteNoise, S3) in production, since SQLite + local media are best suited to small deployments or a persistent disk.
- Swap SQLite for Postgres/MySQL for multi-user production traffic by updating `DATABASES` in `settings.py`.

## Default Test Login

No demo accounts are seeded. Register a new student account from `/accounts/register/`, or create a superuser as shown above to access `/admin/` and the in-app Admin Dashboard at `/admin-dashboard/`.
