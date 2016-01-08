CREATE TABLE Widgets(id INTEGER PRIMARY KEY, foo TEXT, bar TEXT);

INSERT INTO Widgets
(foo, bar)
SELECT "foo 1", "bar 1" UNION ALL
SELECT "foo 2", "bar 2" UNION ALL
SELECT "foo 3", "bar 3";