def dynalistCardGenerator(dynalistHTMLFile, outputName, separatedBy, tag):
    #Todos
    #look into how to use either the raw text or OPML to automatically create ankis from dynalist lists
    #Ideally it can look at the entire structure and break it up pseudo recursively
    #ie it will ask you about what the n top structures are and then what the n entries of each structure is

    #dynaListAllSteps: takes in html file and picks a list and outputs cards with front being the head and number of elements in list. Back is the list
    dynaListAllSteps(dynalistHTMLFile)
    #things i do with dyna anki: paste lists. take
    #htmlParser(dynalistHTMLFile)
