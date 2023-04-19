import stations as st
import stationscraper as ss

url = "http://reg.bom.gov.au/qld/observations/brisbane.shtml"
file = 'brisbane_stations.json'

allstations = st.Stations()
allstations.get_stations(url)
station_url = allstations.link_by_station_name("Archerfield")

station = ss.StationScraper()
station.get_url(station_url)
# station.refresh_data()
station.min = 2
station.threaded_scheduled_scraping()
