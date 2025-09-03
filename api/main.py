from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional, List
import os 
import uvicorn
    
# Connect to the correct SQLite database
DATABASE_URL = "sqlite:///./moviesDB.db"
print("Looking for DB at:", os.path.abspath("moviesDB.db"))  # 👈 Add this right after
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# SQLAlchemy model for movies
class Movie(Base):
    __tablename__ = "final_dataset"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    duration = Column(String)
    MPA = Column(String)
    rating = Column(Float)
    votes = Column(String)
    meta_score = Column(Float)
    description = Column(String)
    movie_link = Column(String)
    writers = Column(String)
    directors = Column(String)
    stars = Column(String)
    budget = Column(String)
    opening_weekend_gross = Column(String)
    gross_worldwide = Column(String)
    gross_us_canada = Column(String)
    release_date = Column(Float)
    countries_origin = Column(String)
    filming_locations = Column(String)
    production_companies = Column(String)
    awards_content = Column(String)
    genres = Column(String)
    languages = Column(String)

#Base.metadata.create_all(bind=engine)

class MovieModel(BaseModel):
    id: str
    title: str
    year: int
    duration: Optional[str]
    MPA: Optional[str]
    rating: Optional[float]
    votes: Optional[str]  # fixed from int to str
    meta_score: Optional[float]
    description: Optional[str]
    movie_link: Optional[str]
    writers: Optional[str]
    directors: Optional[str]
    stars: Optional[str]
    budget: Optional[str]
    opening_weekend_gross: Optional[str]
    gross_worldwide: Optional[str]
    gross_us_canada: Optional[str]
    release_date: Optional[float]
    countries_origin: Optional[str]
    filming_locations: Optional[str]
    production_companies: Optional[str]
    awards_content: Optional[str]
    genres: Optional[str]
    languages: Optional[str]

    class Config:
        orm_mode = True

# Create FastAPI app
app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: Search movies by actor
@app.get("/movies/actor/{actor}", response_model=List[MovieModel])
def get_movies_by_actor(actor: str, db: Session = Depends(get_db)):
    results = db.query(Movie).filter(Movie.stars.ilike(f"%{actor}%")).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No movies found for actor '{actor}'")
    return results

# Endpoint: Search movies by director
@app.get("/movies/director/{director}", response_model=List[MovieModel])
def get_movies_by_director(director: str, db: Session = Depends(get_db)):
    results = db.query(Movie).filter(Movie.directors.ilike(f"%{director}%")).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No movies found for director '{director}'")
    return results

# Endpoint: Return sample directors for testing
@app.get("/debug-directors/")
def debug_directors(db: Session = Depends(get_db)):
    return db.query(Movie.directors).limit(20).all()

# Endpoint: Confirm database connection and movie count
@app.get("/check")
def check_movies(db: Session = Depends(get_db)):
    count = db.query(Movie).count()
    return {"movie_count": count}

# Endpoint: Gets top 10 movies based on rating. You can change the amount and what its based on.
@app.get("/movies/", response_model=List[MovieModel])
def get_top_movies(db: Session = Depends(get_db)):
    return db.query(Movie).order_by(Movie.rating.desc()).limit(10).all()

# Endpoint: Gets movie by id.
@app.get("/movie/{movie_id}", response_model=MovieModel)
def get_movie(movie_id: str, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# EndPoint: Search for a movie by title 
@app.get("/movies/title/{title}", response_model=List[MovieModel])
def search_movie_by_title(title: str, db: Session = Depends(get_db)):
    # Case-insensitive, trimmed, partial match
    # Query The DB for a movie title 
    # Case Insensitive match 
    # Trims whitespace on both sides 
    # Partial match included for titles that aren't fully correct (Like %title%)
    # Example Interstell = Interstellar 
    movie = (
        db.query(Movie)
        .filter(func.lower(func.trim(Movie.title)).like(f"%{title.strip().lower()}%"))
        .all()
    )
# If no mive is found return 404 error 
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
# Return the matching movie with all its data from the MovieModel In JSON
# All JSON is given but just display Title, description, director, and IMDB link
    return movie

# EndPoint: Get a random movie that matches a given genre
# Give the discord user a selection of genres to choose from
# Example of genres to give the user
#    "Action",
#    "Adventure",
#    "Comedy",
#    "Drama",
#    "Fantasy",
#    "Horror",
#    "Mystery",
#    "Romance",
#    "Sci-Fi",
#    "Thriller",
#    "Documentary",
#    "Crime",
#    "Western",
#    "War",
#    "Animation"
@app.get("/movies/bygenre/{genre}", response_model=MovieModel)
def get_random_movie_by_genre(genre: str, db: Session = Depends(get_db)):
# Query the DB for a movie where the genre field contains the given genre string 
# Case insensitive match 
# Uses SQL RANDOM() to shuffle and pick a random matching movie from genre 
    movie = (
        db.query(Movie)
        .filter(func.lower(Movie.genres).like(f"%{genre.lower()}%"))
        .order_by(func.random())
        .first()
    )
# If no movie in that genre is found return 404 error 
    if not movie:
        raise HTTPException(status_code=404, detail=f"No movies found in genre '{genre}'")
# Return the radomly selected movie as JSON from the movie model
# All JSON is given but just display Title, description, director, and IMDB link
    return movie



# Endpoint: Get all movies from a given genre
# Example: /movies/genre/Comedy
# Useful for showing a full list of movies in a selected genre (for dropdowns or search)
# Returns a list of matching movies (case-insensitive, partial match)
@app.get("/movies/genre/{genre}", response_model=List[MovieModel])
def get_movies_by_genre(genre: str, db: Session = Depends(get_db)):
    movies = (
        db.query(Movie)
        .filter(func.lower(Movie.genres).like(f"%{genre.lower()}%"))
        .limit(2500) #Limit on movies from genre pulls the first 2500 movies for a genre
    )
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found in genre '{genre}'")
    return movies


#starts the api as local host
if __name__ == "__main__":
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
