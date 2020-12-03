import python.global_vars as universal

def search_handler(tags):
    result = universal.databaseRef.search_tags(tags)
    pulled_fileids = []
    for each in result:
        pulled_fileids = []
        pulled_relations = universal.databaseRef.search_relationships(each[0])
        print("I Pulled", len(pulled_relations), " Relations From DB")
        #for ec in pulled_relations:
        #    print(universal.databaseRef.pull_file(ec[0]))
