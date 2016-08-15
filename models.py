from Entity import Entity

class Article(Entity):
    _fields = ['title', 'text']
    _parents = ['category']
    _children = []
    _siblings = ['tags']

class Category(Entity):
    _fields   = ['title']
    _parents  = []
    _children = ['articles']
    _siblings = []

class Tag(Entity):
    _fields   = ['value']
    _parents  = []
    _children = []
    _siblings = ['articles']

if __name__ == '__main__':
    # article = Article()
    # category = Category(2)

    # print type(category)

    # article.category = category
    # article.category = 2
    # article.title = 'dfhgfh'
    # article.text = 'dfhgfh'
    # article.save()

    category = Category(1)
    # for article in category.articles:
    #     pass
       # print(article.title)

    # article = Article(1)
    # for tag in article.tags:
    #     print(tag.value)

    # tag = Tag(1)
    # for article in tag.articles:
    #     print(article.text)

    # # for article in Article.all():
    # #     print(article.title)

    #print(article.title)
    #print(article.text)
    #print(article.nosuchfield)

    #print(article.title)
    #print(article.category.title)

    #print(article.category)
    #article.category.title

    #article.title = "New title"
    #article.text = 'Very interesting content'
    #article.save()

    #article.title = 'Another title'
    #article.text = 'Very interesting content'
    #article.save()

    #article.title = 'Bugs are wonderful'
    #article.save()

    # article = Article(1)
    # for tag in article.tags:
    #     print(tag.value)
    
    #article.delete()
    