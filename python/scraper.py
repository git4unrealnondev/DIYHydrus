"""
Handler For Loading and Deploying Scrapers
"""
import python.globals as globals

class ScraperClass():
	_scrapersdb = {}
	def __init__(self):
		"""
		Loads and Initlizes the scrapers into Memory.
		"""
		for each in globals.databaseRef.pull_scrapers():
			
