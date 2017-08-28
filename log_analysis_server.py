from log_analysis_db import get_most_visited_articles, get_most_popular_authors, get_dates_with_errors
from flask import Flask


app = Flask(__name__) # initialize Flask App

html_wrap = '''\
            <!DOCTYPE html>
            <html>
              <head>
                <title>Log Analysis Project</title>
              </head>
              <body>
                <h1>Log Analysis Project</h1>

                <h3>Three most visited articles</h3>

                  %s

                <h3>Most popular authors</h3>

                  %s

                <h3>Dates with more than 1 &#37; errors </h3>

                  %s

              </body>
            </html>
            '''

span_holder = '<span style="display: block;"> %s </span>'

@app.route('/', methods=['GET'])
def main():
    '''Main Page'''
    # add in the most visited websites
    first = get_most_visited_articles()
    first_text = ""
    for entry in first:
        first_text += span_holder % entry

    # add in the most popular authors
    second = get_most_popular_authors()
    second_text = ""
    for entry in second:
        second_text += span_holder % entry

    # add in the dates with more than 1% errors
    third =  get_dates_with_errors()
    third_text = ""
    for entry in third:
        third_text += span_holder % entry

    #print(third_text)
    # add these to the html wrapper
    html_page_to_serve = html_wrap % (first_text, second_text, third_text)

    return html_page_to_serve

if __name__ == '__main__':
    #print(main())
    app.run(host='0.0.0.0', port=8888)
