from main import GoogleAPIClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

class GoogleSheets(GoogleAPIClient):
    def __init__(self) -> None:
        # 呼叫 GoogleAPIClient.__init__()，並提供 serviceName, version, scope
        super().__init__(
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets'],
        )

    def getWorkSheet(self, spreadsheetId: str, range: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId = spreadsheetId,
            range = range
        )
        
        response = request.execute()['values']

        del response[0]
        header = response[0]
        del response[0]
        
        result = pd.DataFrame(response, columns=header)
        return result

# for test gsheet, initial range = car1
if __name__ == '__main__':

    search_name = argv[1]
    car_num = 1
    
    for i in range(car_num):

        myWorksheet = GoogleSheets()
        data = myWorksheet.getWorkSheet(
            spreadsheetId='1ZXtRzYFYUQeDhz1e9SBg1bNcc9n9eCvdfPD5fw2w1BU',
            #range=str(f"'car{i + 1}'")
            range=str("'car4'")
        )

        data.index = data['']
        del data['']
        #print(data)

        if not data.loc[data['P1'].str.contains(search_name) | data['P2'].str.contains(search_name) | data['P3'].str.contains(search_name) | data['P4'].str.contains(search_name) | data['P5'].str.contains(search_name)].empty:

            print(f'\t[car {i+1}]')
            print(data.loc[data['P1'].str.contains(search_name) | 
                           data['P2'].str.contains(search_name) |
                           data['P3'].str.contains(search_name) |
                           data['P4'].str.contains(search_name) |
                           data['P5'].str.contains(search_name)])