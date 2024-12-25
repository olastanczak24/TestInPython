# TestInPython

This repository contains Python scripts for testing and demonstrating functionalities related to REST APIs, DynamoDB integration, and other utilities.

## Scripts Overview

### 1. `test.py`
The `test.py` script demonstrates how to fetch random images from a public API based on an animal type and save the metadata to a database. This script provides foundational functionality for interacting with REST APIs.

### 2. `function.py`
The `function.py` script builds upon the functionality in `test.py` and adds the following features:

#### Features:
1. **Fetching Images**:
   - Fetches images from a public API (`https://place.dog/`) based on a specified count.
   - Designed to work with any API providing animal images.

2. **Saving Images to DynamoDB**:
   - Saves metadata of fetched images into an AWS DynamoDB table named `AnimalPictures`.
   - Metadata includes:
     - `AnimalType`: The type of animal (e.g., dog, cat).
     - `Timestamp`: The time the image was saved, stored as a UNIX timestamp (in milliseconds).
     - `ImageURL`: The URL of the fetched image.
     - `ImageID`: A unique identifier for the image.

3. **Fetching the Latest Picture**:
   - Provides a REST API endpoint `/get_last_picture` that queries the DynamoDB table and retrieves the `Timestamp` of the most recently saved picture for a specified `AnimalType`.

