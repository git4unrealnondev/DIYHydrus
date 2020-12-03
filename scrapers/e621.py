'''
A Test Scraper to parse data from a website.
By Default scrips have access to universal.
'''
# Parameters to be passed into fileDownloaderRateLimited.py when instantiated
USER_AGENT = "DIYHydrus/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 DIYHydrus/10.0"
RATE_LIMIT = 5

#Custom scripts to parse data
def web_data_check():
    '''
    Parses data from website
    '''

    init_url = web_data[0]
    rate_limiter = web_data[1]
    parent = web_data[2]

    if init_url is None:
        front = "https://e621.net/posts.json?tags="
        back = ''
        parent_url = parent.search_term.replace(" ", "+")
        init_url =  front + str(parent_url) + back

    #print(init_url)
    json_response = parent.normal_requests(init_url).json()
    to_strip = ["id", "created_at", "sources", "relationships"]
    pull = ["tags"]
    stored_data_temp = {}

    #Data Pulled from website
    print("json",json_response)

    if json_response is None:
        print("isnone")

    elif "posts" in json_response:

        for each in json_response["posts"]:
            keylist = {}
            #print(each)
            for every in to_strip:
                keylist[every] = each[every]
            for every in pull:
                for tag in each[every]:
    
                    if isinstance(each[every][tag], list):
                        keylist[tag] = each[every][tag]
            if not each["file"]["url"] is None:
                keylist["md5"] = each["file"]["md5"]
                keylist["size"] = each["file"]["size"]
        #print(each["file"]["url"], each['file'])
                keylist["filename"] = each["file"]["url"].split("/")[6]
                keylist["pic"] = each["file"]["url"]
                keylist["rating"] = each["rating"]
                keylist["sources"] = each["sources"]
                keylist["pools"] = each["pools"]
                
                if not each["relationships"]["parent_id"] is None:
                    keylist["parent_id"] = each["relationships"]["parent_id"]

                if len(each["relationships"]["children"]) > 0:
                    keylist["children"] = each["relationships"]["children"]
                
                stored_data_temp[keylist["id"]] = keylist
        print(stored_data_temp)
        return stored_data_temp
    elif "post" in json_response:
        keylist = {}
        for each in json_response["post"]["tags"]:
            keylist[each] = json_response["post"]["tags"][each]
        if "rating" in json_response["post"] and not json_response["post"]["file"]["url"] is None:
            keylist["id"] = json_response["post"]["id"]
            keylist["created_at"] = json_response["post"]["created_at"]
            keylist["rating"] = json_response["post"]["rating"]
            keylist["md5"]  = json_response["post"]["file"]["md5"]
            keylist["size"] = json_response["post"]["file"]["size"]
            keylist["filename"] = json_response["post"]["file"]["url"].split("/")[6]
            keylist["pic"] = json_response["post"]["file"]["url"]
            keylist["sources"] = json_response["post"]["sources"]
            keylist["pools"] = json_response["post"]["pools"]

        if not json_response["post"]["relationships"]["parent_id"] is None:
            keylist["parent_id"] = json_response["post"]["relationships"]["parent_id"]

        if len(json_response["post"]["relationships"]["children"]) > 0:
            keylist["children"] = json_response["post"]["relationships"]["children"]

        #print(keylist)
        stored_data_temp[keylist["id"]] = keylist
        return stored_data_temp

if 'web_data' in globals():
    print("I am getting called from fileDownloaderRateLimited")
    stored_data = web_data_check()
else:
    print("I am getting called from scraper.py . My variables are getting read.")
    # Empty Pass back for laziness
    stored_data = ''
