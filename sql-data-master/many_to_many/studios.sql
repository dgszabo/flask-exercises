\c movies_db
ALTER TABLE IF EXISTS movies 
  DROP COLUMN IF EXISTS studio_id;

DROP TABLE IF EXISTS studios;

CREATE TABLE studios
(
  id SERIAL PRIMARY KEY,
  name TEXT
);

INSERT INTO studios
  (name)
VALUES
  ('Buena Vista'),
  ('20th Century Fox'),
  ('Paramount'),
  ('Universal'),
  ('Warner Bros.'),
  ('Dreamworks SKG'),
  ('Lionsgate'),
  ('Sony / Columbia'),
  ('New Line'),
  ('Newmarket'),
  ('Summit Entertainment'),
  ('Orion Pictures'),
  ('Sony Classics');

ALTER TABLE movies
  ADD COLUMN studio_id INTEGER;

UPDATE movies 
  SET studio_id=1
WHERE id IN (1, 5, 6, 7, 9, 10, 11, 14, 19, 20, 21, 23, 24, 29, 31, 33, 40, 42, 47, 52, 53, 64, 67, 70, 77, 78, 82, 86, 95, 100);

UPDATE movies
  SET studio_id=2
WHERE id in (2, 12, 13, 34, 41, 66, 68, 69, 84, 87);

UPDATE movies
  SET studio_id=3
WHERE id in (3, 28, 44, 55, 58, 59, 60, 62, 65);

UPDATE movies
  SET studio_id=4
WHERE id in (4, 17, 27, 38, 39, 43, 50, 91, 94, 97);

UPDATE movies
  SET studio_id=5
WHERE id in (8, 15, 22, 32, 45, 54, 56, 57, 61, 72, 73, 76, 79, 81, 83, 85, 89, 92, 93, 99);

UPDATE movies
  SET studio_id=6
WHERE id in (16, 96);

UPDATE movies
  SET studio_id=7
WHERE id in (18, 25, 48, 80, 88);

UPDATE movies
  SET studio_id=8
WHERE id in (26, 30, 36, 49, 51, 71, 98);

UPDATE movies
  SET studio_id=9
WHERE id in (35, 46, 63);

UPDATE movies
  SET studio_id=10
WHERE id in (37);

UPDATE movies
  SET studio_id=11
WHERE id in (74, 75, 90);

ALTER TABLE movies
  ADD CONSTRAINT fk_studio
  FOREIGN KEY (studio_id)
  REFERENCES studios(id);