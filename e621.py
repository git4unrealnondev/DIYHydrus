'''
A Test Scraper to parse data from a website.
By Default scrips have access to universal.
'''
# Parameters to be passed into fileDownloaderRateLimited.py when instantiated
USER_AGENT = "DIYHydrus/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 DIYHydrus/10.0"
RATE_LIMIT = 1

#Custom scripts to parse data
def web_data_check():

    jsonResponse = web_data.json()
    to_strip = ["id", "created_at", "tags", "sources", "relationships"]

    stored_data = {}

    for each in jsonResponse["posts"]:
        keylist = {}
        for every in to_strip:
            keylist[every] = each[every]
        keylist["md5"] = each["file"]["md5"]
        keylist["size"] = each["file"]["size"]
        keylist["filename"] = each["file"]["url"].split("/")[6]
        keylist["pic"] = each["file"]["url"]
        stored_data[keylist["id"]] = keylist
    return stored_data
    
if 'web_data' in globals():
    print("I am getting called from fileDownloaderRateLimited")
    stored_data = web_data_check()
else:
    print("I am getting called from scraper.py . My variables are getting read.")
    # Empty Pass back for laziness
    stored_data = ''

