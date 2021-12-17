"""
Stores Global Variables that ALL scripts that are running can access.
"""
import python.logger as logger
import python.database as database
import python.scraper as scraper
import python.download_rate_limit as rateLimiter
import python.db_commons as commons
import python.plugin as plugin
import python.threads as threads

accessCheck = "YES"

scraperHandler = None
databaseRef = None
pluginManager = None
ThreadManager = None

#Variables
verbose = False
