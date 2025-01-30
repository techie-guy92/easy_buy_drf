# Easy Buy

This project is an online marketplace built using Django Rest Framework (DRF). In this project, people can buy and sell their products. Everyone is able to add products for selling, and everyone can see products. However, if someone wants to buy a product, they need to be a premium user. Those who pay can be premium for 90 days, and after that, their premium status will expire.

It consists of two main apps:

1. **Users App**: Manages user-related functionalities, including registration, profiles, and premium memberships.
2. **Main App**: Handles product-related functionalities, including adding, displaying, and detailed views of products.

## Features

- **User Management**: Allows users to register, log in, and manage their profiles.
- **Premium Membership**: Users can upgrade to premium membership to access additional features.
- **Product Management**: Authenticated users can add, update, and delete products.
- **Display Products**: View a list of all products with search, filtering, and pagination features.
- **Detailed Product Views**: Premium users can view additional details about products and sellers.
- **Authentication**: Secure authentication using JSON Web Tokens (JWT).

## Usage

- Access the API documentation at `http://127.0.0.1:8000/api-documents/` after starting the server.
- Use the provided endpoints to interact with the users and products apps.

## Celery Integration

The project utilizes Celery for handling background tasks and periodic tasks. Specifically, Celery is used to manage premium memberships by checking for expired subscriptions and updating the `is_premium` status of users.

## Clone the repository:

```bash
git clone https://github.com/techie-guy92/easy_buy_drf
```

## Installation Requirements

There are two requirements files: `requirements_linux.txt` and `requirements_windows.txt`.
Choose the one appropriate for your operating system and install the dependencies.
`pip install -r requirements_windows.txt`
`pip install -r requirements_linux.txt`

### Running Celery To handle background tasks, start the Celery worker and beat scheduler:

1. **Start the Celery worker (in a separate terminal):**
   `bash celery -A core worker --loglevel=info `

2. **Start the Celery beat (in another terminal):**
   `bash celery -A core.celery_config beat --loglevel=info `

## Contributing

Feel free to fork the repository and submit pull requests.
For major changes, please open an issue first to discuss what you would like to change.
