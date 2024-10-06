# Ecommerce app

## Overview

**Ecommerce app** is an e-commerce platform designed to sell items. It provides a user-friendly interface that allows people to buy their stuffs and pay online.

**Note**: This repository contains both the **frontend** and **backend** of the application, but I only worked on the **backend** portion. The frontend was developed by another individual.

## Features (Backend)

- **Item Listings**: Admin interface is implemented for the app owner to upload product.

- **Search and Filter**: API endpoints for searching and filtering items based on categories, price, and keywords.

- **Cart & Checkout**: Backend logic to manage the shopping cart and process purchases.

- **Payment Integration**: Secure payment processing via [Stripe] with webhook integration.


## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: [ HTML, CSS, javascript ] (Developed by another team/individual)
- **Database**: dbsqlite
- **Payment Processing**: Stripe
- **Webhooks**: Used for real-time updates from the payment gateway.

## Setup & Installation

### Prerequisites

- Python 3.x
- Django 5.1.1
- Pillow for image handling, Gettext for marking language for translation, etc

### Steps to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/student-marketplace.git
   cd student-marketplace
   
2. **Install the requirement.txt**
   ```bash
   pip install -r requirements.txt

3. **Setup**
   create a .env file and set up your env variable
    SECRET_KEY=NULL
    STRIPE_PUBLISH_KEY=NULL
    STRIPE_SECRET_KEY= NULL
    STRIPE_API_VERSION= NULL
    STRIPE_WEBHOOK_SECRET=NULL

4. **Run your Server**
   ```bash
   Python3 manage.py runserver
