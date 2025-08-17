# `seed.py` - Database Seeder for Listings App

This file (`seed.py`) contains a custom Django management command designed to populate your database with sample `Listing` data. It's an essential tool for development, testing, and demonstrating the `alx_travel_app_0x00` project without manually entering data.

## Location

The `seed.py` file is located at:
`alx_travel_app_0x00/listings/management/commands/seed.py`

## Purpose

The primary purpose of this script is to:
* **Populate Listings:** Create a set number of fictional `Listing` entries in your database.
* **Clear Existing Data:** By default, it first deletes all existing `Listing` objects to ensure a clean slate upon each execution. This prevents data duplication when the command is run multiple times.

## How it Works

The `seed.py` script implements a Django `BaseCommand` with a `handle` method that performs the following actions:

1.  **Imports:** It imports `BaseCommand` from Django's management utilities and the `Listing` model from `listings.models`. The `random` module is used for generating varied sample data.
2.  **`handle` Method:** This is the entry point for the command.
    * It prints a warning before deleting all current `Listing` objects from the database.
    * It defines lists of sample titles and descriptions.
    * It then iterates a fixed number of times (currently 10, but can be adjusted), creating a new `Listing` object in each iteration.
    * For each new listing, it randomly selects a title and description, generates a random price, and sets a random availability status (`True` or `False`).
    * It uses `Listing.objects.create()` to save the new listing to the database.
    * Success messages are printed to the console for each created listing and upon completion.

## Usage

To run this database seeder, navigate to the root directory of your Django project (`alx_travel_app_0x00`, where `manage.py` is located) in your terminal and execute the following command:

```bash
python manage.py seed