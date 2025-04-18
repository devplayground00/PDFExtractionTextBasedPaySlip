import asyncio
import os
import shutil
from typing import Dict, List

from Class.Company2 import PaySlipCompany2
from Helper import PdfHelper
from Helper.DatabaseHelper import DatabaseHelper
from Helper.EmailHelper import EmailHelper
from Helper.PdfHelper import extract_text_from_pdf
from Class.baseClass import BasePaySlipFormat


class Program:

    def __init__(self, email_user, email_pass):
        self.email_user = email_user
        self.email_pass = email_pass

    async def run_async(self):
        working_folder = r""
        history_folder = r""
        fault_folder = r""
        pdf_text = extract_text_from_pdf(working_folder)
        if pdf_text:
            await self.process_text(working_folder, working_folder, history_folder)


        ## Load settings from the database
        # settings: Dict[str, str] = await DatabaseHelper.get_settings()

        # working_folder = settings.get("working_folder", "")
        # history_folder = settings.get("history_folder", "")
        # email = settings.get("email", "")
        # password = settings.get("password", "")
        #
        # email_helper = EmailHelper(email, password)
        #
        # read_email = email_helper.read_emails_from_inbox()

        # for email in read_email:
        #     # print(email)
        #     pdf_files_with_senders = (email_helper.download_pdfs_from_email(working_folder))
        #
        #     for pdf_file_path, (sender_email, email_id) in pdf_files_with_senders.items():
        #         try:
        #             # Extract text from the PDF
        #             pdf_text = extract_text_from_pdf(pdf_file_path)
        #
        #             if pdf_text:
        #                 await self.process_text(pdf_file_path, working_folder, history_folder, sender_email, email_id)
        #
        #                 # Delete the email after processing
        #                 email_helper.delete_email(email_id)
        #
        #         except Exception as e:
        #             print(f"Error processing file {pdf_file_path}: {e}")


    # async def process_text(self, pdf_file_path: str, working_folder: str, history_folder: str, sender_email: str, email_id: bytes):
    async def process_text(self, working_folder: str, pdf_file_path: str, history_folder: str):
        pdf_text = PdfHelper.extract_text_from_pdf(pdf_file_path)
        pdf_lines = [line for line in pdf_text.splitlines() if line.strip()]

        PaySlip_format = self.get_PaySlip_format(pdf_file_path, pdf_text, pdf_lines)

        if PaySlip_format:
            csv_file_path = PaySlip_format.write_csv(working_folder)

            if os.path.exists(csv_file_path):
                try:
                    customer_name = PaySlip_format.customer_name
                    customer_ref_no = PaySlip_format.customer_ref_no
                    await asyncio.sleep(0.5)

                    # Send email
                    email_helper = EmailHelper(self.email_user, self.email_pass)
                    if sender_email and "@" in sender_email:
                        email_helper.send_email_with_attachments(sender_email, pdf_file_path, csv_file_path , customer_name , customer_ref_no)

                    # Move CSV file to history folder
                    csv_destination_path = os.path.join(history_folder, os.path.basename(csv_file_path))
                    shutil.move(csv_file_path, csv_destination_path)
                    # print(f"Moved CSV file to: {csv_destination_path}")

                except Exception as e:
                    print(f"Error moving CSV file: {e}")

            if os.path.exists(pdf_file_path):
                try:
                    pdf_destination_path = os.path.join(history_folder, os.path.basename(pdf_file_path))
                    shutil.move(pdf_file_path, pdf_destination_path)

                    # print(f"Moved PDF file to: {pdf_destination_path}")
                except Exception as e:
                    print(f"Error moving PDF file: {e}")

            # email_helper.delete_email(email_id)

    def get_PaySlip_format(self, file_name: str, pdf_text: str, lines: List[str]) -> BasePaySlipFormat:
        for line in lines:
            if "Payslip" in line:
                return PaySlipCompany2(file_name, pdf_text)

        return None


if __name__ == "__main__":
    async def main():
        settings = await DatabaseHelper.get_settings()
        email_user = settings.get("email", "")
        email_pass = settings.get("password", "")

        program = Program(email_user, email_pass)
        await program.run_async()

    asyncio.run(main())

