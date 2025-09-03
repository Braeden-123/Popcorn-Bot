import discord
from discord.ext import commands
import requests
from pydantic import BaseModel
from typing import Optional, List

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

base_url = "http://localhost:8000"

class MovieModel(BaseModel):
    id: str
    title: str
    year: int
    duration: Optional[str]
    MPA: Optional[str]
    rating: Optional[float]
    votes: Optional[str]
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

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

#DONE
@bot.hybrid_command(description="Shows all movies that match the given title")
async def stitle(ctx, title : str):
    await ctx.send(f"Now searching {title}")
    returnInfo = discord.Embed(title=f"Top 10 \'{title}\' Movies")
    data = requests.get(f"{base_url}/movies/title/{title}").json()
    movie_list: List[MovieModel] = [MovieModel(**movie) for movie in data]
    for movie in movie_list:
        if movie.rating == None:
            movie.rating = 0.0
    movie_list.sort(key=lambda MovieModel: MovieModel.rating, reverse=True)
    number = 1
    embedString= ""
    for movie in movie_list[:10]:
        embedString += f"**{number}.** {movie.title} - {movie.duration} - {movie.rating} - {movie.directors[1:-1]}\n\n"
        number += 1
    returnInfo.add_field(name="Name - Length - Rating - Director", value=embedString)
    await ctx.send(embed = returnInfo)

@bot.hybrid_command(description="Shows all details for a given movie")
async def moviedetails(ctx, title : str):
    await ctx.send(f"Now searching {title}")
    data = requests.get(f"{base_url}/movies/title/{title}").json()
    movie_list: List[MovieModel] = [MovieModel(**movie) for movie in data]
    for movie in movie_list:
        if movie.rating == None:
            movie.rating = 0.0
    movie_list.sort(key=lambda MovieModel: MovieModel.rating, reverse=True)
    movie : MovieModel = movie_list[0]
    embedString= f"""
**Title:** {movie.title}
**Year:** {movie.year}
**Duration:** {movie.duration or 'N/A'}
**MPA Rating:** {movie.MPA or 'N/A'}
**IMDb Rating:** {movie.rating if movie.rating is not None else 'N/A'}
**Votes:** {movie.votes or 'N/A'}
**Metascore:** {movie.meta_score if movie.meta_score is not None else 'N/A'}

**Description:**
{movie.description or 'N/A'}

**Link:** {movie.movie_link or 'N/A'}

**Writers:** {movie.writers or 'N/A'}
**Directors:** {movie.directors or 'N/A'}
**Stars:** {movie.stars or 'N/A'}
**Budget:** {movie.budget or 'N/A'}
**Opening Weekend Gross:** {movie.opening_weekend_gross or 'N/A'}
**Worldwide Gross:** {movie.gross_worldwide or 'N/A'}
**US/Canada Gross:** {movie.gross_us_canada or 'N/A'}
**Release Date:** {movie.release_date if movie.release_date is not None else 'N/A'}

**Countries of Origin:** {movie.countries_origin or 'N/A'}
**Filming Locations:** {movie.filming_locations or 'N/A'}
**Production Companies:** {movie.production_companies or 'N/A'}
**Awards:** {movie.awards_content or 'N/A'}
**Genres:** {movie.genres or 'N/A'}
**Languages:** {movie.languages or 'N/A'}
""".strip()
    await ctx.send(embedString)

#DONE
@bot.hybrid_command(description="Shows top movies within a given genre")
async def sgenre(ctx, genre : str):
    await ctx.send(f"Now searching {genre}")
    returnInfo = discord.Embed(title=f"Top 10 \'{genre}\' Movies")
    data = requests.get(f"{base_url}/movies/genre/{genre}").json()
    movie_list: List[MovieModel] = [MovieModel(**movie) for movie in data]
    for movie in movie_list:
        if movie.rating == None:
            movie.rating = 0.0
    movie_list.sort(key=lambda MovieModel: MovieModel.rating, reverse=True)
    number = 1
    embedString= ""
    for movie in movie_list[:10]:
        embedString += f"**{number}.** {movie.title} - {movie.duration} - {movie.rating} - {movie.directors[1:-1]}\n\n"
        number += 1
    returnInfo.add_field(name="Name - Length - Rating - Director", value=embedString)
    await ctx.send(embed = returnInfo)

#DONE
@bot.hybrid_command(description="Shows top movies for a given director")
async def sdirector(ctx, director : str):
    await ctx.send(f"Now searching {director}")
    returnInfo = discord.Embed(title=f"Top 10 \'{director}\' Movies")
    data = requests.get(f"{base_url}/movies/director/{director}").json()
    movie_list: List[MovieModel] = [MovieModel(**movie) for movie in data]
    for movie in movie_list:
        if movie.rating == None:
            movie.rating = 0.0
    movie_list.sort(key=lambda MovieModel: MovieModel.rating, reverse=True)
    number = 1
    embedString= ""
    for movie in movie_list[:10]:
        embedString += f"**{number}.** {movie.title} - {movie.duration} - {movie.rating} - {movie.directors[1:-1]}\n\n"
        number += 1
    returnInfo.add_field(name="Name - Length - Rating - Director", value=embedString)
    await ctx.send(embed = returnInfo)

#DONE
@bot.hybrid_command(description="Shows top movies for a given actor")
async def sactor(ctx, actor : str):
    await ctx.send(f"Now searching {actor}")
    returnInfo = discord.Embed(title=f"Top 10 \'{actor}\' Movies")
    data = requests.get(f"{base_url}/movies/actor/{actor}").json()
    movie_list: List[MovieModel] = [MovieModel(**movie) for movie in data]
    for movie in movie_list:
        if movie.rating == None:
            movie.rating = 0.0
    movie_list.sort(key=lambda MovieModel: MovieModel.rating, reverse=True)
    number = 1
    embedString= ""
    for movie in movie_list[:10]:
        embedString += f"**{number}.** {movie.title} - {movie.duration} - {movie.rating} - {movie.directors[1:-1]}\n\n"
        number += 1
    returnInfo.add_field(name="Name - Length - Rating - Director", value=embedString)
    await ctx.send(embed = returnInfo)

@bot.hybrid_command(description="Returns details for a random movie within a given genre")
async def genrerandom(ctx, genre:str):
    data = requests.get(f"{base_url}/movies/bygenre/{genre}").json()
    movie :MovieModel = MovieModel(**data)
    embedString= f"""
**Title:** {movie.title}
**Year:** {movie.year}
**Duration:** {movie.duration or 'N/A'}
**MPA Rating:** {movie.MPA or 'N/A'}
**IMDb Rating:** {movie.rating if movie.rating is not None else 'N/A'}
**Votes:** {movie.votes or 'N/A'}
**Metascore:** {movie.meta_score if movie.meta_score is not None else 'N/A'}

**Description:**
{movie.description or 'N/A'}

**Link:** {movie.movie_link or 'N/A'}

**Writers:** {movie.writers or 'N/A'}
**Directors:** {movie.directors or 'N/A'}
**Stars:** {movie.stars or 'N/A'}
**Budget:** {movie.budget or 'N/A'}
**Opening Weekend Gross:** {movie.opening_weekend_gross or 'N/A'}
**Worldwide Gross:** {movie.gross_worldwide or 'N/A'}
**US/Canada Gross:** {movie.gross_us_canada or 'N/A'}
**Release Date:** {movie.release_date if movie.release_date is not None else 'N/A'}

**Countries of Origin:** {movie.countries_origin or 'N/A'}
**Filming Locations:** {movie.filming_locations or 'N/A'}
**Production Companies:** {movie.production_companies or 'N/A'}
**Awards:** {movie.awards_content or 'N/A'}
**Genres:** {movie.genres or 'N/A'}
**Languages:** {movie.languages or 'N/A'}
""".strip()
    await ctx.send(embedString)



bot.run("insert token here")