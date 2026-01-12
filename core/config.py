import os
from dotenv import load_dotenv
import jdatetime
from datetime import datetime, date



load_dotenv(dotenv_path='.env')


class Settings:
    title: str = "Fahameh Main timetable"
    description: str = "API Powered by FastAPI"
    version: str = "1.0.0"
    DATABASE_URL: str = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1800
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = 'HS256'
    BACKEND_IP_ADDRESS: str = os.getenv("BACKEND_IP_ADDRESS")
    FRONTEND_IP_ADDRESS: str = os.getenv("FRONTEND_IP_ADDRESS")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT"))
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT"))



    @staticmethod
    def jalali_to_gregorian(jalali_date) -> date:
        """
        jalali_date باید به صورت 'YYYY-MM-DD' باشد
        خروجی: نوع datetime.date (میلادی)
        """
        year, month, day = map(int, jalali_date.split("/"))
        g_date = jdatetime.date(jalali_date.year, jalali_date.month, jalali_date.day).togregorian()
        return g_date

    @staticmethod
    def gregorian_to_jalali_str(g_date):
        """
        g_date: نوع datetime.date یا datetime.datetime
        خروجی: رشته به صورت 'روز/ماه/سال'
        """
        if isinstance(g_date, datetime):
            g_date = g_date.date()

        j_date = jdatetime.date.fromgregorian(date=g_date)
        # return f"{j_date.day}/{j_date.month}/{j_date.year}"
        return f"{j_date.year}/{j_date.month}/{j_date.day}"


settings: Settings = Settings()