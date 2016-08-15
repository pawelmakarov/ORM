
UPDATE article SET article_text = 'Very content', article_title = 'New title' WHERE article_id = 2;

UPDATE article SET article_text = 'luxury', article_title = 'Mercedes-Benz' WHERE article_id = 3;

DELETE FROM article WHERE article_id = 3;

UPDATE article SET article_text = 'Very interesting content', article_title = 'New lololo' WHERE article_id = 3;
update article set article_title=? where article_id = ?

CREATE TABLE article (article_id INTEGER PRIMARY KEY, article_title varchar(50), article_text varchar(50), category_id INTEGER);
INSERT OR IGNORE INTO article (article_title, article_text, category_id) VALUES ("BMW", "real", 1);
INSERT OR IGNORE INTO article (article_title, article_text, category_id) VALUES ("Audi", "for everyone", 2);
INSERT OR IGNORE INTO article (article_title, article_text, category_id) VALUES ("Mercedes-Benz", "luxury", 1);

CREATE TABLE category (category_id INTEGER PRIMARY KEY, category_title varchar(50));
INSERT OR IGNORE INTO category (category_title) VALUES ("Car");
INSERT OR IGNORE INTO category (category_title) VALUES ("Motorad");
INSERT OR IGNORE INTO category (category_title) VALUES ("Fahrrad");

CREATE TABLE tag (tag_id INTEGER PRIMARY KEY, tag_value varchar(50));
INSERT OR IGNORE INTO tag (tag_value) VALUES ("tag_one");
INSERT OR IGNORE INTO tag (tag_value) VALUES ("tag_two");
INSERT OR IGNORE INTO tag (tag_value) VALUES ("tag_three");

CREATE TABLE article_tag (article_tag_id INTEGER PRIMARY KEY, article_id INTEGER, tag_id INTEGER);
INSERT OR IGNORE INTO article_tag (article_id, tag_id) VALUES (1, 2);
INSERT OR IGNORE INTO article_tag (article_id, tag_id) VALUES (2, 1);
INSERT OR IGNORE INTO article_tag (article_id, tag_id) VALUES (2, 1);

UPDATE article SET {1} WHERE {0}_id = {2}
update article set article_title="BMW", article_text="real" where article_id = 1;

INSERT INTO article VALUES ('green', 'red', 2);
INSERT INTO article (article_title, article_text, category_id) VALUES ('green', 'red', 2);

