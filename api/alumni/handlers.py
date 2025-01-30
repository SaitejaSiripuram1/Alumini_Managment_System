import pandas as pd
import re
from datetime import datetime
from django.core.exceptions import ValidationError

def handle_alumni_csv(file):
    # Read CSV file using pandas
    try:
        data = pd.read_csv(file)
        print(f"CSV Columns: {data.columns.tolist()}")  # Log the columns
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False  # Return False if CSV can't be read

    # Check for required columns
    required_columns = ['USN', 'Name', 'Phone', 'Email', 'Department', 'Year Join', 'Year Pass']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        print(f"CSV is missing required columns: {missing_columns}")
        return False  # Return False if any columns are missing

    # Continue with the rest of your function...
    try:
        for _, row in data.iterrows():
            print(f"Processing row: {row}")  # Log each row
            # Extract row data
            usn = row['USN']
            name = row['Name']
            phone = row['Phone']
            email = row['Email']
            branch = row['Department']
            year_joined = row['Year Join']
            year_passed = row['Year Pass']

            # Validate required fields
            if not usn or not name or not phone or not email:
                print(f"Missing required field for USN {usn}")
                continue  # Skip row if required fields are missing

            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print(f"Invalid email format for {email}")
                continue  # Skip row if email is invalid

            # Validate phone (assuming it should be numeric)
            if not str(phone).isnumeric():
                print(f"Invalid phone number for {usn}")
                continue  # Skip row if phone is invalid

            # Validate year format (should be a date)
            try:
                year_joined = datetime.strptime(str(year_joined), '%Y-%m-%d')
                year_passed = datetime.strptime(str(year_passed), '%Y-%m-%d')
            except ValueError:
                print(f"Invalid date format for USN {usn}. Expected YYYY-MM-DD.")
                continue  # Skip row if date format is incorrect

            # Continue with the rest of the process...
            # Ensure alumni group exists
            # (Assuming Group and User are imported and available)
            group = Group.objects.get(name='alumni')  # type: ignore

            # Create or update user based on email
            user, created = User.objects.get_or_create(email=email)  # type: ignore
            user.username = email[:len(email)-12]  # Set username from email (removes domain part)
            user.set_password('anteater')  # Default password, should be changed later
            user.groups.add(group)
            user.save()

            # Create or update alumni record
            alumnus, created = Alumni.objects.get_or_create(usn=usn)  # type: ignore
            alumnus.user = user
            alumnus.name = name
            alumnus.phone = phone
            alumnus.email = email
            alumnus.year_joined = year_joined
            alumnus.year_passed = year_passed
            alumnus.branch = branch
            alumnus.save()

        return True  # Return True if processing is successful
    except Exception as e:
        print(f"Error processing CSV row: {e}")
        return False  # Return False if there was an error
