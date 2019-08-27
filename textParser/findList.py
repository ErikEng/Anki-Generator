def findList(HTMLFile, leaves):
    #res = hp.feed(dynalistHTMLFile)
    test = HTMLParser()
    print(HTMLFile)
    print(test.feed('<!DOCTYPE html><html><body><ul><li>test<ul><li>ma</li><li>asd<ul><li>lksdfn</li></ul></li></ul></li></ul></body></html>'))
    #print(hp.get_starttag_text())
    print("ended coding here")
