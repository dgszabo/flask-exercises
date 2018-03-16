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
    select title from movies;

1.  All information on the G-rated movies.
    select * from movies where rating = 'G';

1.  The title and release year of every movie, ordered with the oldest movie first.
    select title, release_year from movies order by release_year;

1.  All information on the 5 longest movies.
    select * from movies order by runtime desc limit 5;

1.  A table with columns of `rating` and `total`, tabulating the total number of G, PG, PG-13, and R-rated movies.
    select rating, count(rating) as total from movies group by rating;

1.  A table with columns of `release_year` and `average_runtime`, tabulating the average runtime by year for every movie in the database. The data should be in reverse chronological order (i.e. the most recent year should be first).
    select release_year, round(avg(runtime)) as average_runtime from movies group by release_year order by release_year DESC;

### Part 2

In the terminal, let's now add the `stars` data:

```sh
psql < stars.sql
```

As another warmup, write the queries that will show you the following information:

1.  The first and last name of the five oldest stars.
    select first_name, last_name from stars order by birth_date limit 5;

1.  The first and last name of the five youngest stars.
    select first_name, last_name from stars order by birth_date desc limit 5;

1.  A table of first names along with the number of stars having that first name, provided that this number is greater than 1.
    select first_name, case when count(first_name) > 1 then count(first_name) end from stars group by first_name;
    select first_name, case when count(first_name) > 1 then count(first_name) end from stars group by first_name order by count(first_name) desc limit 3;
    select first_name, count(first_name) from stars group by first_name HAVING count(first_name) > 1;

1.  A table of years along with the number of stars born in that year, sorted chronologically.
    SELECT EXTRACT(year FROM birth_date) AS birth_year,
    COUNT(EXTRACT(year FROM birth_date))
    FROM stars
    GROUP BY birth_year
    ORDER BY birth_year;

### Part 3

Now let's explore some basic joins with a 1 to many association!

```
psql < studios.sql
```

Write the queries that will show you the following information:

1.  The movie title and studio name for every movie in the database.
    select movies.title, studios.name from movies join studios on studios.id = movies.studio_id;


2.  The names of all studios that have no movie in the database (try to do this with two different queries!)
    select studios.name, count(studios.name) from movies join studios on studios.id = movies.studio_id group by studios.name; -> this is the opposite
    select movies.title, studios.name from movies right join studios on studios.id = movies.studio_id where movies.title is null; -> this has a movies.title column too
    select studios.name from movies right join studios on studios.id = movies.studio_id where movies.title is null;
    elect studios.name from studios left join movies on studios.id = movies.studio_id where movies.title is null;

### Part 4

Once you've learned about many-to-many associations, let's add the `roles` join table:

```sh
psql < roles.sql
```

As an exercise, write the queries that will show you the following information:

1.  The star first name, star last name, and movie title for every matching movie and star pair in the database.
    select stars.first_name, stars.last_name, movies.title from roles inner join stars on stars.id = roles.star_id inner join movies on movies.id = roles.movie_id;

1.  The first and last names of every star who has been in a G-rated movie.
    select stars.first_name, stars.last_name from roles inner join stars on stars.id = roles.star_id inner join movies on movies.id = roles.movie_id where movies.rating = 'G';

1.  The first and last names of every star along with the number of movies they have been in, in descending order by the number of movies.
    select stars.first_name, stars.last_name, count(roles.star_id) from roles inner join stars on stars.id = roles.star_id inner join movies on movies.id = roles.movie_id group by stars.id order by count(stars.id) desc;

1.  The title of every movie along with the number of stars in that movie, in descending order by the number of stars.
    SELECT movies.title, count(roles.star_id) AS number_of_stars FROM roles INNER JOIN stars ON stars.id = roles.star_id INNER JOIN movies ON movies.id = roles.movie_id GROUP BY movies.title ORDER BY count(roles.movie_id) DESC;

1.  The first and last names of the five stars whose movies have the longest average.
    SELECT stars.first_name, stars.last_name FROM roles INNER JOIN stars ON stars.id = roles.star_id INNER JOIN movies ON movies.id = roles.movie_id group by stars.id order by avg(movies.runtime) desc LIMIT 5;

1.  The first and last names of the five stars whose movies have the longest average, among stars who have more than one movie in the database.
    SELECT stars.first_name, stars.last_name FROM roles INNER JOIN stars ON stars.id = roles.star_id INNER JOIN movies ON movies.id = roles.movie_id group by stars.id HAVING count(roles.star_id) > 1 order by avg(movies.runtime) DESC LIMIT 5;

### Part 5

Try writing the following queries using a join that isn't an inner join:

1.  The titles of all movies that don't feature any stars in our database.
    SELECT movies.title FROM roles FULL JOIN stars ON stars.id = roles.star_id FULL JOIN movies ON movies.id = roles.movie_id WHERE stars.id is null;

2.  The first and last names of all stars that don't appear in any movies in our database.
    SELECT stars.first_name, stars.last_name FROM roles FULL JOIN stars ON stars.id = roles.star_id FULL JOIN movies ON movies.id = roles.movie_id WHERE movies.title is null;

3.  The first names, last names, and titles corresponding to every role in the database, along with every movie title that doesn't have a star, and the first and last names of every star not in a movie.
    SELECT stars.first_name, stars.last_name, movies.title FROM roles FULL JOIN stars ON stars.id = roles.star_id FULL JOIN movies ON movies.id = roles.movie_id;
