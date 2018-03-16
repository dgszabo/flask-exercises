# Many To Many Sample Database

The SQL files in this directory feature an example of a many-to-many association. But before digging into many-to-manys, let's review some of the SQL queries we've seen before.

### Part 1

In the terminal, let's run a couple of files to put the `movies` data into a database:

```sh
psql < setup.sql
psql < movies.sql
psql movies_db
```

As a warmup, write the queries that will show you the following information:

1.  The title of every movie.
1.  All information on the G-rated movies.
1.  The title and release year of every movie, ordered with the oldest movie first.
1.  All information on the 5 longest movies.
1.  A table with columns of `rating` and `total`, tabulating the total number of G, PG, PG-13, and R-rated movies.
1.  A table with columns of `release_year` and `average_runtime`, tabulating the average runtime by year for every movie in the database. The data should be in reverse chronological order (i.e. the most recent year should be first).

### Part 2

In the terminal, let's now add the `stars` data:

```sh
psql < stars.sql
```

As another warmup, write the queries that will show you the following information:

1.  The first and last name of the five oldest stars.
1.  The first and last name of the five youngest stars.
1.  A table of first names along with the number of stars having that first name, provided that this number is greater than 1.
1.  A table of years along with the number of stars born in that year, sorted chronologically.

### Part 3

Now let's explore some basic joins with a 1 to many association!

```
psql < studios.sql
```

Write the queries that will show you the following information:

1.  The movie title and studio name for every movie in the database.
2.  The names of all studios that have no movie in the database (try to do this with two different queries!)

### Part 4

Once you've learned about many-to-many associations, let's add the `roles` join table:

```sh
psql < roles.sql
```

As an exercise, write the queries that will show you the following information:

1.  The star first name, star last name, and movie title for every matching movie and star pair in the database.
1.  The first and last names of every star who has been in a G-rated movie.
1.  The first and last names of every star along with the number of movies they have been in, in descending order by the number of movies.
1.  The title of every movie along with the number of stars in that movie, in descending order by the number of stars.
1.  The first and last names of the five stars whose movies have the longest average.
1.  The first and last names of the five stars whose movies have the longest average, among stars who have more than one movie in the database.

### Part 5

Try writing the following queries using a join that isn't an inner join:

1.  The titles of all movies that don't feature any stars in our database.
2.  The first and last names of all stars that don't appear in any movies in our database.
3.  The first names, last names, and titles corresponding to every role in the database, along with every movie title that doesn't have a star, and the first and last names of every star not in a movie.
