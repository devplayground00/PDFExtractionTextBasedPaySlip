import re
from datetime import datetime
from Class.baseClass import BasePaySlipFormat

class PaySlipAsolute(BasePaySlipFormat):
    def  __init__(self,file_path: str, raw_text_lines: str):
        super().__init__(file_path,raw_text_lines)

    def read_header(self):
        for i in range(len(self.raw_text_lines)):
            if "Payslip" in self.raw_text_lines[i]:

                raw_item = None

                if i  >= 0:
                    companynamedatesplit = self.raw_text_lines[i].split(" ")
                    # year = str(datetime.now().year)
                    self.CompanyName  = f"{re.sub(r'\d{4}','',companynamedatesplit[3]).strip()} {companynamedatesplit[4]} {companynamedatesplit [5]}"



                    companynamedateregex = self.raw_text_lines[i]
                    match_companynamedateregex = re.search(r"([A-Za-z]+)\s+(\d{4})",companynamedateregex)
                    if match_companynamedateregex:
                        self.SalaryDate =f"{match_companynamedateregex.group(1)} {match_companynamedateregex.group(2)}"
                    else:
                        self.SalaryDate = ""

                if i + 3 >=0:
                    self.JobTitle = self.raw_text_lines[i +3]

                self.items.append(self)



