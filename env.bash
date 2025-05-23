#!/bin/bash
export DATABASE_URL="sqlite:///instance/securecart.db"
export SECRET_KEY="securecart_secret_key"
export STRIPE_PUBLIC_KEY="pk_test_51QjgpJP8JWjkpw7dT1NpHUjKJ4MxH0EeIOFTUJ4BoOPQCOzDe8e0SyXba8XrYRkQJKKZpJc1bfxca0OjSoqVErvf00opk9ULku"
export STRIPE_SECRET_KEY="sk_test_51QjgpJP8JWjkpw7dUt5AkFTbQOuCMqdrXm6Pex2iTbZH775wzG7ofdLuhsxGXD6Xms8VWiGft4FsWSlC1tbns5b000DAkR0xBs"
export RECAPTCHA_PUBLIC_KEY=""
export RECAPTCHA_PRIVATE_KEY=""
export DEBUG="True"

if [ ! -d "instance" ]; then
    mkdir -p instance
fi

if [ ! -f "instance/securecart.db" ]; then
    touch instance/securecart.db
    echo "Created empty database file at instance/securecart.db"
fi

echo "Environment variables set successfully for SecureCart application."
