import os
import pandas as pd
from abc import ABC, abstractmethod
import csv

class BasePaySlipFormat(ABC):
    def __init__(self, file_path, raw_text_lines):
        self.file_path = file_path
        self.raw_text = raw_text_lines.strip()
        self.raw_text_lines = [line.strip() for line in self.raw_text.split("\n") if line.strip()]

        self._CompanyName = ""
        self._JobTitle = ""
        self._Department = ""
        self._SalaryDate = ""
        self._SalaryBasicAmount = ""

        self._Allowance1 = ""
        self._Allowance1Amount = ""
        self._Allowance2 = ""
        self._Allowance2Amount = ""
        self._Allowance3 = ""
        self._Allowance3Amount = ""
        self._OvertimeAmount = ""
        self._Bonus = ""

        self._EmployeeEPF = ""
        self._EmployeeSOCSO = ""
        self._EmployeeEIS = ""
        self._EmployeeTAX = ""

        self._EmployerEPF = ""
        self._EmployerSOCSO = ""
        self._EmployerEIS = ""
        self._EmployerTAX = ""
        self._EmployerHDRF = ""

        self._NetPay = ""
        self._Currency = ""

        self.items = []

        if self.raw_text_lines:
            self.read_header()

    @property
    def CompanyName(self):
        return self._CompanyName

    @CompanyName.setter
    def CompanyName(self, value):
        self._CompanyName = value

    @property
    def JobTitle(self):
        return self._JobTitle

    @JobTitle.setter
    def JobTitle(self,value):
        self._JobTitle = value

    @property
    def Department(self):
        return self._Department

    @Department.setter
    def Department(self,value):
        self._Department = value

    @property
    def SalaryDate(self):
        return self._SalaryDate

    @SalaryDate.setter
    def SalaryDate(self,value):
        self._SalaryDate = value

    @property
    def SalaryBasicAmount(self):
        return self._SalaryBasicAmount

    @SalaryBasicAmount.setter
    def SalaryBasicAmount(self,value):
        self._SalaryBasicAmount =value

    @property
    def Allowance1(self):
        return self._Allowance1

    @Allowance1.setter
    def Allowance1(self,value):
        self._Allowance1 =value

    @property
    def Allowance1Amount(self):
        return self._Allowance1Amount

    @Allowance1Amount.setter
    def Allowance1Amount(self,value):
        self._Allowance1Amount = value

    @property
    def Allowance2(self):
        return self._Allowance2

    @property
    def Allowance2Amount(self):
        return self._Allowance2Amount

    @property
    def Allowance3(self):
        return self._Allowance3

    @property
    def Allowance3Amount(self):
        return self._Allowance3Amount

    @property
    def OvertimeAmount(self):
        return self._OvertimeAmount

    @property
    def Bonus(self):
        return self._Bonus

    @property
    def EmployeeEPF(self):
        return self._EmployeeEPF

    @property
    def EmployeeSOCSO(self):
        return self._EmployeeSOCSO

    @property
    def EmployeeEIS(self):
        return self._EmployeeEIS

    @property
    def EmployeeTAX(self):
        return self._EmployeeTAX

    @property
    def EmployerEPF(self):
        return self._EmployerEPF

    @property
    def EmployerSOCSO(self):
        return self._EmployerSOCSO

    @property
    def EmployerEIS(self):
        return self._EmployerEIS

    @property
    def EmployerTAX(self):
        return self._EmployerTAX

    @property
    def EmployerHDRF(self):
        return self._EmployerHDRF

    @property
    def NetPay(self):
        return self._NetPay

    @property
    def Currency(self):
        return self._Currency

    @abstractmethod
    def read_header(self):
        pass


    def write_csv(self, working_folder):
        # Sanitize filename
        csv_file_name = f"{self.CompanyName} {self.SalaryDate}.csv"
        csv_file_path = os.path.join(working_folder, csv_file_name)

        if not self.items:
            raise ValueError("No items to write to CSV.")

        data = []
        for item in self.items:
            row = [self.CompanyName, self.JobTitle,self.Department,self.SalaryDate,self.SalaryBasicAmount,self.Allowance1,self.Allowance1Amount,self.Allowance2,
                   self.Allowance2Amount,self.Allowance3,self.Allowance3Amount,self.OvertimeAmount,self.Bonus,self.EmployeeEPF,self.EmployeeSOCSO,self.EmployeeEIS,
                   self.EmployeeTAX,self.EmployerEPF,self.EmployerSOCSO,self.EmployerEIS,self.EmployerTAX,self.EmployerHDRF,self.NetPay,self.Currency
            ]
            data.append(row)



        columns = [
            "Company Name", "Job Title", "Department", "Salary Date", "Salary Basic Amount","Allowance 1", "Allowance 1 Amount", "Allowance 2",
            "Allowance 2 Amount", "Allowance 3","Allowance 3 Amount", "Overtime Amount", "Bonus", "Employee EPF","Employee SOCSO", "Employee EIS",
            "Employee TAX", "Employer EPF", "Employer SOCSO","Employer EIS", "Employer TAX", "Employer HDRF","Net Pay","Currency"
        ]

        try:
            df = pd.DataFrame(data, columns=columns)
            df.to_csv(csv_file_path, sep=',', index=False, quoting=csv.QUOTE_ALL, quotechar='"')
            # print(f"CSV saved successfully to {csv_file_path}")
        except Exception as e:
            print(f"Error writing CSV: {e}")

        return csv_file_path

