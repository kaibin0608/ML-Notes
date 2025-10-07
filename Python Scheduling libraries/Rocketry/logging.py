from rocketry import Rocketry
from rocketry.log import MinimalRecord
from redbird.repos import CSVFileRepo

repo = CSVFileRepo(filename="tasks.csv", model=MinimalRecord)
app = Rocketry(logger_repo=repo)