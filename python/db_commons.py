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
        tmp = universal.databaseRef.pull_file(each[0])
        rawtag = universal.databaseRef.search_relationships_file(tmp[0][0])
        fintag = []
        for rtag in rawtag:
            fintag.append(universal.databaseRef.search_tagid(int(rtag[1]))[0][1])
        #print("./" + universal.db_dir + "Files/" + tmp[0][1][0] + tmp[0][1][1] + "/" + tmp[0][1][2] + tmp[0][1][3] + "/" + tmp[0][2], str(fintag))
        print()
        print(fintag)
       
