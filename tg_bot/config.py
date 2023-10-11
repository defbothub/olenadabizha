import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS").strip().split(',')]

    MAX_RECORDS_PER_USER = int(os.getenv("MAX_RECORDS_PER_USER"))
    RECORD_MONITORING_DELAY = float(os.getenv("RECORD_MONITORING_DELAY"))

    CONTACTS_FACEBOOK_URL = os.getenv("CONTACTS_FACEBOOK_URL")
    CONTACTS_INSTAGRAM_URL = os.getenv("CONTACTS_INSTAGRAM_URL")
    CONTACTS_PHONE_NUMBER = os.getenv("CONTACTS_PHONE_NUMBER")
    CONTACTS_FIRST_NAME = os.getenv("CONTACTS_FIRST_NAME")
    CONTACTS_OFFICE_LATITUDE = float(os.getenv("CONTACTS_OFFICE_LATITUDE"))
    CONTACTS_OFFICE_LONGITUDE = float(os.getenv("CONTACTS_OFFICE_LONGITUDE"))

    PAYMENT_URL = os.getenv("PAYMENT_URL")