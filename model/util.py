class Client():
    
    def year_month_day(self, date):
        try:
            return date.split('-')
        except:
            print("Error: date is not a string")