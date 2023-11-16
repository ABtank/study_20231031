class Article:
    id = 0
    def __init__(self, id, title, text, date, is_my, tegs, is_annon):
        self.title = title
        self.text = text
        self.date = date
        self.is_my = is_my
        self.tegs = tegs
        self.is_annon = is_annon
        Article.id += 1
        self.article_id = id

    def __str__(self):
        return f'{self.article_id}) {self.title}: {self.text}, {self.date}'
