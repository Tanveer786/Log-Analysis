#!/usr/bin/env python
"""
This python script analyses newspaper database.

It displays
1. Top3 most popular articles of all time.
2. Most popular authors of all time.
3. Days where more than 1% of requests led to errors.
"""

import psycopg2


def executeQuery(cursor, query):
    """
    executeQuery returns the results of an SQL Query.

    executeQuery takes an SQL query, database cursor as parameters,
    executes the query using the cursor and returs as a list of tuples.

    args:
    query - an SQL query statement to be executed.
    cursor - cursor of a database to execute query with.

    returns:
    A list of tuples containing the results of the query.
    """
    cursor.execute(query)
    return cursor.fetchall()


def printQueryResult(result, heading, appendString):
    """
    printQueryResult method displays the given Heading and Query Results.

    printQueryResult takes heading, result and appendString as parameter. It
    displays the heading and then displays the result by looping through them
    row-by-row and appending the given string at the end of each line(row).

    args:
    result - Query result to loop through row-by-row and print.
    heading - Heading of the results to be displayed.
    appendString - String that needs to be appended to each row of result.

    returns:
    None
    """
    print(heading + "\n" + len(heading)*"-")
    for index, row in enumerate(results, 1):
        print('{}. {} - {} {}'.format(index, row[0], row[1], appendString))
    print("\n")


if __name__ == "__main__":

    print("\nLOG ANALYSIS RESULTS\n" + "="*20 + "\n")

    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()

    query = """
            SELECT title, views
            FROM articles
            INNER JOIN(
              SELECT path, COUNT(*) as views
              FROM log
              GROUP BY log.path
            ) AS log
            ON log.path = ('/article/' || slug)
            ORDER BY views DESC
            LIMIT 3
            """
    # Executing Query to obtain Top 3 Most popular articles of all time.
    results = executeQuery(
        cursor, query)

    printQueryResult(results, "Top 3 most popular articles of all time",
                     "views")

    query = """
            SELECT name, SUM(views)
            FROM (
                SELECT name, title
                FROM authors
                JOIN articles
                ON author = authors.id
            ) AS AuthorArticles,
            (
                SELECT title, views
                FROM articles
                INNER JOIN (
                    SELECT path, COUNT(*) AS views
                    FROM log
                    GROUP BY log.path
                ) AS log
                ON ('/article/' || slug) = path
            ) AS ArticleViews
            WHERE AuthorArticles.title = articleViews.title
            GROUP BY name
            ORDER BY sum DESC;
            """
    # Executing Query to obtain Most popular article authors of all time.
    results = executeQuery(
        cursor, query)

    printQueryResult(results, "Most popular article authors of all time",
                     "views")

    query = """
            SELECT to_char(Date, 'Mon dd, yyyy') AS Date, ROUND(CAST((CAST(
                errors AS float)/CAST(requests AS float))*100 AS numeric), 2)
                AS errorpercent
            FROM (
                SELECT date(time) AS Date, COUNT(*) AS requests, COUNT(*)
                    FILTER(WHERE status = '404 NOT FOUND') AS errors
                FROM log
                GROUP BY Date
            ) AS logStats
            WHERE CAST(errors AS float) > (CAST(requests AS float)/100);
            """
    # Executing Query to obtain Days where > 1% of requests led to errors
    results = executeQuery(
        cursor, query)

    printQueryResult(
        results, "Days where more than 1% request led to errors",
        "% errors")

    conn.close()
