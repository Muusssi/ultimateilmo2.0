
CREATE TABLE person(
    id serial PRIMARY KEY,
    name text UNIQUE
);


CREATE TABLE answer(
    id serial PRIMARY KEY,
    person_id integer references person(id) not null,
    given_on timestamp default now(),
    time01 varchar(10),
    time02 varchar(10),
    time03 varchar(10),
    time04 varchar(10),
    time05 varchar(10),
    time06 varchar(10),
    time07 varchar(10),
    time08 varchar(10),
    time09 varchar(10),
    time10 varchar(10),
    time11 varchar(10),
    time12 varchar(10),
    notes text
);


INSERT INTO answer(person_id, time01, time02, time03, time04, time05, time06,
    time07, time08, time09, time10, time11, time12, notes)
VALUES(1, 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', NULL),
(2, 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'ei pääse'),
(3, 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'ehkä');
