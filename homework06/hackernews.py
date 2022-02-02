from bottle import (
    route, run, template, request, redirect
)
from db import News, session
from homework06.scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label is None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    id_of_news = int(request.query.id)
    label_of_news = str(request.query.label)
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    s = session()
    s.query(News).filter_by(id=id_of_news).update({'label': label_of_news})
    # 4. Сохранить результат в БД
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    # 1. Получить данные с новостного сайта
    s = session()
    list_of_news = get_news('https://news.ycombinator.com/newest', 1)
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    for i in list_of_news:
        news = News(
            title=i['title'],
            author=i['author'],
            url=i['url'],
            comments=i['comments'],
            points=i['points']
        )
        already_in = False
        for item in s.query(News).all():
            if item.title == news.title and item.author == news.author:
                print('"{}" by {} is already in database'.format(item.title, item.author))
                already_in = True
                break
        if not already_in:
            s.add(news)
    s.commit()
    # 3. Сохранить в БД те новости, которых там нет
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    return redirect('/recommendations')


if __name__ == "__main__":
    run(host="localhost", port=8080)
