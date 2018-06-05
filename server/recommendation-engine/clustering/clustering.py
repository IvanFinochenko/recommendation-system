from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, split
from utils import OneHotEncoderArray, HashingFeature
from pyspark.ml.feature import StandardScaler, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.clustering import KMeans
from pyspark.sql.types import ArrayType, StringType, IntegerType
import psycopg2

def read_postgres(table):
    df = spark.read.format('jdbc').options(
    url = 'jdbc:postgresql://localhost:5432/movies_db?user=ivan&password=qwerty',
    dbtable=table).load()
    return df

def update_movie(partition):
    conn = psycopg2.connect(user='ivan', password='qwerty', dbname='movies_db')
    cur = conn.cursor()
    for row in partition:
        cur.execute('update movies set cluster=%s where movie_id=%s', (row[1], row[0]))
    conn.commit()
    cur.close()
    conn.close()

spark = SparkSession\
    .builder\
    .master('local[4]')\
    .appName('clustering-movies')\
    .getOrCreate()

movies = read_postgres('movies')
genres = read_postgres('genres')
awards = read_postgres('awards')
movies_genre = read_postgres('movies_genre')
movies_award = read_postgres('movies_award')
ratings = read_postgres('ratings')

movies_genres = movies_genre.groupby('movie_id').agg(F.collect_list('genre_id').alias('genres_arr'))
movies = movies.join(movies_genres, 'movie_id')\
    .filter(col('country').isNotNull())\
    .na.fill(1)

scaler = StandardScaler(inputCol='features_vec', outputCol='features')
hfDirector = HashingFeature(inputCol='director', outputCol='director_hash')
hfCountry = HashingFeature(inputCol='country', outputCol='country_hash')
ohe = OneHotEncoderArray(inputCol='genres_arr', outputCol='genres_vec', size=32)
assembler = VectorAssembler(inputCols=[
    'year', 'genres_vec','count_reviews',
    'percent_good_reviews', 'budget', 'box_office',
    'country_hash', 'age', 'image', 'rating'], outputCol='features_vec')

kmeans = KMeans(k=28, seed=1)
pipeline = Pipeline(stages=[hfCountry, ohe, assembler, scaler, kmeans])
model = pipeline.fit(movies)

predictions = model.transform(movies)

predictions.select('movie_id', 'prediction')\
    .foreachPartition(update_movie)
