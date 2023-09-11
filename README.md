# Secure Messaging Web Application

This web app. allows users to create accounts, send and receive encrypted messages to other accounts, and enable Two-Factor Authentication (2FA). 

## Features

- **User Registration:** Users can create accounts with a unique username and password. They have the option to enable 2FA during registration.

- **2FA Setup:** Users can set up Two-Factor Authentication for their accounts using a Time-based One-Time Password (TOTP). The app generates a QR code that users can scan with their authenticator app.

- **Message Encryption:** Users can encrypt messages they want to send to other users. The encryption process uses recipient's public keys to ensure secure communication.

- **Message Decryption:** Users can decrypt messages they receive from others. The decryption process involves using the user's private key, which is securely stored.

## Getting Started

To run this web application locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/secure-messaging-app.git
   cd secure-messaging-app
   
2. Create a PostgreSQL Database:

You'll need to create a PostgreSQL database and update the ```SQLALCHEMY_DATABASE_URI``` in the ```setup.env``` file with the appropriate connection string.

Set Up Environment Variables:

Create a ```.env``` file with your secret key. You can use the ```setup.env``` file as a template.

## Usage

1. Run the App.

Start the application by running the following command:

```python app.py```

2. Access the App.

Navigate to http://localhost:5000 to access the app.

## Future Changes

Currently the encrypting and decrypting of messages is done via ```encrypt_decrypt.py``` and while from a user experience perspective, that is annoying - it is what I preferred when creating this. I plan on adding functionality to the website so everything is done on there.
