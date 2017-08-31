# log analysis
import psycopg2


# returns the 3 most visited articles
def get_most_visited_articles():

    # connect to database
    conn = psycopg2.connect("dbname=news")
    # get cursor
    c = conn.cursor()
    # run query
    query_title_counts = """SELECT articles.title, COUNT(*)
                    FROM log LEFT JOIN
                    articles ON log.path LIKE '%' || articles.slug || '%'
                    WHERE log.status = '200 OK' AND articles.title IS NOT NULL
                    GROUP BY articles.title
                    ORDER BY COUNT(*) DESC LIMIT 3;
                    """
    c.execute(query_title_counts)  # gets the count top 3 paths
    title_count_list = c.fetchall()
    # close connection
    c.close()
    conn.close()

    # replace the path slugs with the actual article title and
    # create a readable string from the retrieved results
    text_statements = []
    for title, count in title_count_list:
        return_text = '\"' + title + '\" -- ' + str(count)
        text_statements.append(return_text)

    return text_statements


# returns most popular authors
def get_most_popular_authors():
    # connect to database
    conn = psycopg2.connect("dbname=news")
    # get cursor
    c = conn.cursor()
    # run query
    # create a view which has the author name for each article
    # Make sure there isnt already a view called author_article in the database
    query_author_article = """CREATE VIEW author_article AS
                            SELECT au.name, art.slug
                            FROM authors as au, articles as art
                            WHERE au.id = art.author;
                            """
    c.execute(query_author_article)  # this will create the view

    query_author_counts = """SELECT aa.name, COUNT(*)
                        FROM log LEFT JOIN author_article AS aa
                        ON log.path LIKE '%' || aa.slug || '%'
                        WHERE log.status = '200 OK'
                        AND aa.name IS NOT NULL
                        GROUP BY aa.name
                        ORDER BY COUNT(*) DESC;
                        """
    c.execute(query_author_counts)
    author_count_list = c.fetchall()

    c.execute("DROP VIEW author_article;")  # delete the view
    conn.commit()

    # close connection
    c.close()
    conn.close()

    # create a readable string from the retrieved results
    text_statements = []
    for author, count in author_count_list:
        try:
            return_text = author + ' -- ' + str(count) + ' views'
        except TypeError:  # if author name doesnt exist
            continue  # skip to next entry
        text_statements.append(return_text)

    return text_statements


# returns the dates that had more than 1% of visits result in errors
def get_dates_with_errors():
    # connect to database
    conn = psycopg2.connect("dbname=news")
    # get cursor
    c = conn.cursor()
    # run query

    # create a view for count of all visits
    query_all_count = """CREATE VIEW all_date AS
                        SELECT date(log.time), COUNT(*) AS all
                        FROM log GROUP BY date(log.time);
                        """
    # create a view for only the bad visits
    query_bad_count = """CREATE VIEW bad_date AS
                        SELECT date(log.time), COUNT(*) AS bad
                        FROM log WHERE log.status LIKE '%404%'
                        GROUP BY date(log.time);
                        """
    # create both the views
    c.execute(query_all_count)
    c.execute(query_bad_count)

    # use the two views to get dates with greater than 1% bad visits
    query_ratio = """SELECT a.date, b.bad::decimal/a.all::decimal AS ratio
                    FROM all_date AS a LEFT JOIN
                    bad_date AS b ON a.date = b.date
                    WHERE b.bad::decimal/a.all::decimal > 0.01;
                    """

    c.execute(query_ratio)
    date_ratio_list = c.fetchall()

    c.execute("DROP VIEW all_date;")  # delete the view
    c.execute("DROP VIEW bad_date;")  # delete the view
    conn.commit()

    # close connection
    c.close()
    conn.close()

    # replace the path slugs with the actual article title
    text_statements = []
    for date, ratio in date_ratio_list:
        try:
            return_text = str(date) + ' -- ' + str(int(ratio*100)) + '% errors'
        except ValueError:  # if ratio is invalid
            continue  # skip to next entry
        text_statements.append(return_text)

    return text_statements
