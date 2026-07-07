import sqlite3
conn = sqlite3.connect("cinema.db")
cursor = conn.cursor()
cursor.execute("""
INSERT INTO Films (Title, Genre, AgeRating, duration, Description) VALUES
('anaconda', 'Comedy', 'R', 95, 'A documentary film crew is hunted by a giant snake while exploring the Amazon rainforest.'),
('grown ups 1', 'Comedy', 'PG-13', 102, 'Five childhood friends reunite for a weekend after the death of their basketball coach.'),
('grown ups 2', 'Comedy', 'PG-13', 101, 'Lenny and his friends enjoy another chaotic summer filled with family and hilarious adventures.'),
('22 jumpstreet', 'Comedy', 'R', 112, 'Two undercover police officers go to college to investigate a new drug ring.'),

('gladiator 1', 'Action', 'R', 155, 'A betrayed Roman general fights as a gladiator to seek revenge against a corrupt emperor.'),
('gladiator 2', 'Action', 'R', 148, 'Years after the fall of Rome, a new gladiator rises to challenge the empire.'),
('maze runner', 'Action', 'PG-13', 113, 'A teenager wakes up trapped in a mysterious maze with no memory of his past.'),
('the working man', 'Action', '15', 116, 'A former soldier is forced back into action to rescue a missing young woman.'),

('annabelle comes home', 'Horror', '15', 106, 'The possessed Annabelle doll unleashes supernatural terror inside the Warrens'' home.'),
('get out', 'Horror', '15', 104, 'A young man uncovers a disturbing secret while visiting his girlfriend''s family.'),
('US', 'Horror', '15', 116, 'A family is hunted by terrifying versions of themselves during a vacation.'),
('conjuring', 'Horror', '15', 112, 'Paranormal investigators Ed and Lorraine Warren help a family haunted by an evil presence.'),

('predator badlands', 'Sci-Fi', '15', 120, 'A lone survivor battles a deadly Predator on a dangerous alien frontier.'),
('avengers endgame', 'Sci-Fi', '12A', 181, 'The Avengers make one final attempt to reverse the devastation caused by Thanos.'),
('hunger games part 1 mockingbird', 'Sci-Fi', '12A', 123, 'Katniss becomes the symbol of rebellion against the Capitol.'),
('hunger games part 2 mocking bird', 'Sci-Fi', '12A', 137, 'Katniss leads the rebels into the final battle against President Snow.'),

('after the hunt', 'Thriller', '15', 140, 'A respected professor faces accusations that threaten her career and personal life.'),
('prisoners', 'Thriller', '15', 153, 'A desperate father searches for his missing daughter when the police run out of leads.'),
('inception', 'Thriller', '12A', 148, 'A skilled thief enters dreams to steal secrets but is given one impossible mission.'),
('carry on', 'Thriller', '15', 119, 'An airport security officer becomes entangled in a dangerous criminal conspiracy.');
""")
# cursor.execute(
#     "UPDATE Customers SET password = ? WHERE CustomerID = ?",
# )
# cursor.execute("DELETE FROM films WHERE Title = ?", ('Inception',))

cursor.execute(
    "UPDATE Customers SET password = ? WHERE CustomerID = ?",
    ("123456", 1)
)
cursor.execute(
    "SELECT username FROM Customers WHERE CustomerID = ?",
    (1,)
)
user = cursor.fetchone()
print(user[0])
cursor.execute(
    "SELECT * FROM films WHERE Genre = ?",
    ("comedy",)
)
comedy_movies = cursor.fetchall()
print(comedy_movies)
[(6, 'anaconda', 'comedy', 'R', 95, 'A documentary film crew is hunted by a giant snake while on a remote island in the Amazonrainforest.'), (7, '22 jumpstreet', 'comedy', 'R', 112, 'Two underachieving cops are sent back to a local high school to blendin and bring down a synthetic drug ring.'), (8, 'grown ups 1', 'comedy', 'R', 102, 'After their high school basketball coach passes away, five good friends reunite for a Fourth of July holiday weekend.'), (9, 'grown ups 2', 'comedy', 'R', 101, 'The fivefriends return to their hometown for a reunion with their families and old friends.'), (11, 'anaconda', 'comedy', 'R', 95, 'A documentary film crew is hunted by a giant snake while on a remote island in the Amazon rainforest.'), (12, '22 jumpstreet', 'comedy', 'R', 112, 'Two underachieving cops are sent back to a local high school to blend in and bring down a synthetic drug ring.'), (13, 'grown ups 1', 'comedy', 'R', 102, 'After their high school basketball coach passes away, five good friends reunite for a Fourth of July holiday weekend.'), (14, 'grown ups 2', 'comedy', 'R', 101, 'The five friends return to their hometown fora reunion with their families and old friends.')]
conn.commit()
conn.close()