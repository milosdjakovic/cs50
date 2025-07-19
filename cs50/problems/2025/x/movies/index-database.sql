-- Indexes for the directors table (foreign keys)
CREATE INDEX idx_directors_movie_id ON directors (movie_id);
CREATE INDEX idx_directors_person_id ON directors (person_id);

-- Indexes for the movies table (potential search and order by columns)
CREATE INDEX idx_movies_title ON movies (title);
CREATE INDEX idx_movies_year ON movies (year);

-- Index for the people table (potential search column)
CREATE INDEX idx_people_name ON people (name);
CREATE INDEX idx_people_birth ON people (birth); -- Added index on birth if you filter by it

-- Indexes for the ratings table (foreign key and potential order by column)
CREATE INDEX idx_ratings_movie_id ON ratings (movie_id);
CREATE INDEX idx_ratings_rating ON ratings (rating DESC); -- Index for sorting by rating

-- Indexes for the stars table (foreign keys)
CREATE INDEX idx_stars_movie_id ON stars (movie_id);
CREATE INDEX idx_stars_person_id ON stars (person_id);

-- Composite indexes (consider if these match your common query patterns)
-- Index for finding directors of a specific movie
CREATE INDEX idx_directors_movie_person ON directors (movie_id, person_id);

-- Index for finding movies a specific person starred in
CREATE INDEX idx_stars_person_movie ON stars (person_id, movie_id);

-- Index that might help with the specific join and order by query (though effectiveness may vary)
CREATE INDEX idx_movies_stars_ratings_order ON stars (movie_id, person_id);
CREATE INDEX idx_ratings_movie_rating ON ratings (movie_id, rating DESC);
