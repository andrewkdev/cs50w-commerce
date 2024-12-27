# CS50W Commerce Project

An eBay-like e-commerce auction site built with Django as part of Harvard's CS50w course. This web application allows users to create auction listings, place bids, comment on listings, and manage a personalized watchlist.

## Features

- **User Registration and Authentication**: Users can register, log in, and log out securely.
- **Auction Listings**: Users can create and view auction listings, each with a title, description, image, category, and starting bid.
- **Bidding System**: Users can place bids on active listings, and the current price updates automatically.
- **Watchlist**: Users can add or remove listings from their personal watchlist.
- **Categories**: Browse listings by categories and filter auctions based on their type.
- **Comment System**: Users can comment on active listings, fostering engagement and discussion.
- **Auction Closure**: Listing creators can close auctions, declaring the highest bidder as the winner.

## Technologies Used

- **Django**: Web framework for building and managing the backend.
- **SQLite**: Database management for storing user, listing, and bid data.
- **HTML/CSS**: Frontend styling and layout.
- **Bootstrap**: Responsive design elements and styling.
- **JavaScript**: For interactive components.

## Installation

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/andrewkdev/cs50w-commerce.git
   ```

2. Navigate to the project directory:
   ```bash
   cd cs50w-commerce
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   On macOS/Linux: source venv/bin/activate
   On Windows: venv\Scripts\activate
   ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Make database migrations:
    ```bash
   python manage.py makemigrations auctions
   python manage.py migrate
    ```

6. Run the development server:
    ```bash
   python manage.py runserver
    ```

7. Open your browser and visit: http://127.0.0.1:8000/

## Usage

- **Register** a new user account.
- **Log in** with your credentials.
- **Create** auction listings by specifying a title, description, starting bid, image URL, and category.
- **Bid** on active listings as a logged-in user.
- **Add** or **remove** items from your watchlist.
- **Comment** on listings and engage with other users.
- **Close** auctions as the listing creator, declaring the highest bidder the winner.

## Screenshots

![image](https://github.com/user-attachments/assets/5a817a3d-3215-4a50-9ff7-828bfaf01d91)
![image](https://github.com/user-attachments/assets/04cbfe36-291d-44bc-a7b1-0493a2ba3909)
![image](https://github.com/user-attachments/assets/43529eac-ad7b-40d6-bc69-82dda74b6f37)
![image](https://github.com/user-attachments/assets/1d9b35d0-ec72-4107-9350-7e5bc7370c44)
![image](https://github.com/user-attachments/assets/6c05f7cf-138f-40e7-b837-540bd8a8a2b7)




