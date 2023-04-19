import pandas as pd
import urllib.request
import schedule
import time
import math
import threading


class StationScraper:
    def __init__(self):
        self.data = pd.DataFrame()
        self.min = 10
        self.output_name = "data.csv"

    def get_url(self, url):
        self.url = url

    def scrape_data(self):
        with urllib.request.urlopen(self.url) as response:
            data = response.read().decode('utf-8')

        # Find the start and end of the data section
        start = data.find('[data]') + len('[data]\n')
        end = len(data)

        # Extract the data section and split it into rows
        rows = [line.strip().split(',')
                for line in data[start:end].split('\n')]
        data = pd.DataFrame(rows[1:147], columns=rows[0])
        data = data[[
            'local_date_time_full[80]', 'rain_trace[80]', 'air_temp']]

        # preprocess the data
        data = data.replace(to_replace='"', value='', regex=True)
        data['local_date_time_full[80]'] = data[
            'local_date_time_full[80]'].astype(int)
        data[['rain_trace[80]', 'air_temp']] = data[[
            'rain_trace[80]', 'air_temp']].astype(float)
        data['local_date_time_full[80]'] = data[
            'local_date_time_full[80]'].astype(str)
        data['local_date_time_full[80]'] = pd.to_datetime(
            data['local_date_time_full[80]'], format='%Y%m%d%H%M%S')

        return data

    def refresh_data(self):
        data = self.scrape_data()
        if self.data.empty:
            self.data = data
            self.data.to_csv(self.output_name, index=False)
        else:
            top_row = self.data.iloc[0]
            data = data[data['local_date_time_full[80]'] >
                        top_row['local_date_time_full[80]']]
            if not data.empty:
                self.data = pd.concat([data, self.data], ignore_index=True)
                self.data.to_csv(self.output_name, index=False)

    def schedule_scraping(self):
        self.refresh_data()
        schedule.every(self.min).minutes.do(self.refresh_data)

        while True:
            schedule.run_pending()
            tmp = math.ceil(schedule.idle_seconds())
            if (tmp % 60) == 0:
                print("Data will be reloaded in ", tmp/60, " mins")
            time.sleep(1)

    def threaded_scheduled_scraping(self):
        task_thread = threading.Thread(target=self.schedule_scraping)
        task_thread.start()
