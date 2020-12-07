'''
A Test Scraper to parse data from a website.
By Default scrips have access to universal.
'''
# Parameters to be passed into fileDownloaderRateLimited.py when instantiated
USER_AGENT = "DIYHydrus/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 DIYHydrus/10.0"
RATE_LIMIT = 15
class FunctionHandler():

    def __init__(self, web_data):
        self.web_data = web_data

    def handle_data(self, init_url):
        '''
        Parses data from website
        '''
    #print(init_url)
        json_response = self.parent.normal_requests(init_url).json()
        to_strip = ["id", "created_at", "sources", "relationships"]
        pull = ["tags"]
        stored_data_temp = {}

        #Data Pulled from website
        #print("json",json_response)

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

    #Custom scripts to parse data
    def web_data_check(self):

        init_url = self.web_data[0]
        rate_limiter = self.web_data[1]
        self.parent = self.web_data[2]

        if init_url is None:
            front_pass = "https://e621.net/posts.json"
            front = "https://e621.net/posts.json?limit=1?tags="
            back = ''
            tags_store = "?tags="
            page = "&page="
            parent_url = self.parent.search_term.replace(" ", "+")
            init_url =  front + str(parent_url) + back

            data = self.parent.normal_requests(init_url).json()
            before_id = data["posts"][0]["id"]
            #print(init_url, )

            loop = True
            counter = 1
            storage = {}
            while loop:
                #print("L", counter)
                #self.handle_data("y")
                url = front_pass + tags_store + parent_url + page + str(counter)
                #print(url)
                gained_data = self.handle_data(url)
                storage.update(gained_data)
                counter += 1
                print(counter, len(storage), len(gained_data))
                #This is needed because e6 returns NONE if pages are greater then 750.
                if counter > 750:
                    loop = False
                if len(gained_data) <= 5:
                    loop = False


            #Removes and duplicate postings :d
            #FROM https://w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-17.php
            cleaned = {}
            for key, value in storage.items():
                if value not in cleaned.values():
                    cleaned[key] = value


            return cleaned
        else:
            print("A")
            return handle_data()

if 'web_data' in globals():
    print("I am getting called from fileDownloaderRateLimited")
    func_storage = FunctionHandler(web_data)
    stored_data = func_storage.web_data_check()
else:
    print("I am getting called from scraper.py . My variables are getting read.")
    # Empty Pass back for laziness
    stored_data = ''
