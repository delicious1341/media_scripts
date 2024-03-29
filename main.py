from tracker_processor import Tracker

# testing
current_tracker = Tracker("media_tracker_6_testing.csv")

current_tracker.scrape()
current_tracker.write_csv_data()