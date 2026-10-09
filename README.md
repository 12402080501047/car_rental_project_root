# SarthiGo – Car Rental Project (Django + Tailwind)

"Your Journey, Our Chariot" – search available cars by dates and seats, book them,
view your bookings, and let the owner manage every booking from an admin dashboard.

**Stack:** Python / Django · HTML + Tailwind CSS (CDN) + JavaScript · SQLite

## Run it (Windows)

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations rentals
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_cars      (optional – adds 6 demo cars)
python manage.py runserver
```
(macOS/Linux: activate with `source venv/bin/activate`.)

Open http://127.0.0.1:8000/

## Pages
| URL | Who | What |
|---|---|---|
| `/` | everyone | Home + "Find Your Ride" search |
| `/register/`, `/login/`, `/logout/` | everyone | Auth (login with username OR email) |
| `/cars/` | everyone | Available cars for the searched dates/seats |
| `/confirm-booking/<id>/` | logged in | Driver info, terms, total bill |
| `/dashboard/` | logged in | My Bookings (cancel up to 2 days before start) |
| `/admin-dashboard/` | staff | All bookings, cancel any booking |
| `/admin/` | staff | Django admin: add cars, see bookings |

## Add cars
Log in at `/admin/` with your superuser -> Cars -> Add. `image_url` is a normal image link
(paste any direct image URL). Leave blank to show a placeholder.

## Folder structure
```
car_rental_project_root/
├── manage.py
├── car_rental_project/   (settings.py, urls.py, wsgi.py, asgi.py)
└── rentals/
    ├── models.py  views.py  forms.py  urls.py  admin.py  backends.py
    ├── management/commands/load_sample_cars.py
    └── templates/rentals/
        base.html  home.html  login.html  register.html  car_list.html
        confirm_booking.html  booking_confirmation.html
        dashboard.html  admin_dashboard.html
```
