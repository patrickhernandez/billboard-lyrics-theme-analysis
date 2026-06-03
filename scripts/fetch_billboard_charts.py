from src.billboard.client import BillboardClient
from src.utils.dates import get_dates

billboard = BillboardClient()

dates = get_dates(start=19600101, end=20260430)
full_charts = billboard.get_hot100(dates)

full_charts.to_parquet('data/raw/full_charts.parquet')