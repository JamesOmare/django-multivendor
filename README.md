# Django Multivendor Site

Welcome to the Django Multivendor Site project! This is a web application that enables multiple vendors to sell their products on a single platform. The project is built using Django and is hosted on Heroku at [my_site.com](https://my_site.com). Check out the [live demo](https://my_site.com)!

## Features
- Multivendor Support
- Product Management
- User Authentication
- Shopping Cart
- Order Management
- Payment Integration

## Installation
1. Clone the repository: `git clone https://github.com/your-username/django-multivendor-site.git`
2. Navigate to the project directory: `cd django-multivendor-site`
3. Install the dependencies: `pip install -r requirements.txt`
4. Set up the database: `python manage.py migrate`
5. Create a superuser account: `python manage.py createsuperuser`
6. Start the development server: `python manage.py runserver`
7. Access the site locally: `http://localhost:8000`

## Deployment
Deployed on Heroku. To deploy:
1. Install Heroku CLI
2. Create a Heroku app: `heroku create my-multivendor-site`
3. Set up environment variables
4. Push code to Heroku: `git push heroku main`
5. Run database migrations: `heroku run python manage.py migrate`
6. Create a superuser account: `heroku run python manage.py createsuperuser`
7. Open the deployed site: `heroku open`

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
