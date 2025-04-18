import pyodbc
import asyncio

class DatabaseHelper:
    CONNECTION_STRING = (
        "DRIVER={SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=TEST;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    @staticmethod
    async def get_settings():
        settings = {}
        try:
            loop = asyncio.get_running_loop()
            conn = await loop.run_in_executor(None, pyodbc.connect, DatabaseHelper.CONNECTION_STRING)
            cursor = conn.cursor()
            query = "SELECT setting_key, setting_value FROM SystemSettings"
            cursor.execute(query)

            for row in cursor.fetchall():
                settings[row.setting_key] = row.setting_value

            cursor.close()
            conn.close()
        except Exception as ex:
            print(f"Error retrieving settings from database: {ex}")

        return settings