def search_handler(universal, tags):
    try:
        result = universal.databaseRef.search_tags(tags)[0][0]
    except IndexError:
        print("Found no images with that tag.")
        return
    #print("result", result)
    result = universal.databaseRef.search_relationships(result)
    pulled_fileids = []
    #print(result)
    for each in result:
        pulled_fileids = []
        #pulled_relations = universal.databaseRef.search_relationships(each)
        #print("I Pulled", len(pulled_relations), " Relations From DB")
        print(universal.databaseRef.pull_file(each[0]))
        #for ec in pulled_relations:
        #    print(universal.databaseRef.pull_file(ec[0]))
