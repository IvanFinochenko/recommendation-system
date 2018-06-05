from pyspark.sql import SparkSession
from pyspark.ml.feature import StandardScaler, VectorAssembler, OneHotEncoderEstimator
from pyspark.sql.functions import col, split, avg, count, first, collect_list, udf
from pyspark.sql.types import ArrayType, StringType, IntegerType
from pyspark.sql.functions import udf
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from utils import OneHotEncoderArray, HashingFeature
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.linalg import SparseVector, VectorUDT, Vectors
from pyspark.sql.window import Window
from pyspark.ml.clustering import KMeans
from pyspark.ml.regression import RandomForestRegressor
import sys

def read_postgres(table):
    df = spark.read.format('jdbc').options(
    url = 'jdbc:postgresql://localhost:5432/movies_db?user=ivan&password=qwerty',
    dbtable=table).load()
    return df

def cluster_sparse(cluster_list, cluster_percent, cluster_avg):
    t = list(map(lambda x: x + 28, cluster_list))
    index = cluster_list + t
    value = cluster_percent + cluster_avg
    l = sorted(list(zip(index, value)), key=lambda x: x[0])
    k = [list(t) for t in zip(*l)]
    return SparseVector(56, k[0], k[1])

spark = SparkSession\
    .builder\
    .master('local[4]')\
    .appName('clustering-movies')\
    .getOrCreate()

a = list(filter(lambda x: 'user_id' in x, sys.argv))
user_id = a[0].split('=')[1]

movies = read_postgres('movies')
genres = read_postgres('genres')
awards = read_postgres('awards')
movies_genre = read_postgres('movies_genre')
movies_award = read_postgres('movies_award')
ratings = read_postgres('ratings')

df = ratings.join(movies, 'movie_id').cache()
windowUserId = Window.partitionBy('user_id')

clusters = df.withColumn('count_movies', count('movie_id').over(windowUserId))\
    .groupby('user_id', 'cluster')\
    .agg((count('movie_id') / first('count_movies')).alias('cluster_percent'),
        (avg('vote')).alias('cluster_rating'))

cluster_udf = udf(cluster_sparse, VectorUDT())
data = clusters.groupby('user_id')\
    .agg(
        collect_list('cluster').alias('cluster'),
        collect_list('cluster_percent').alias('cluster_percent'),
        collect_list('cluster_rating').alias('cluster_rating')
    ).withColumn('cluster_vector', cluster_udf(col('cluster'), col('cluster_percent'), col('cluster_rating')))

scaler = StandardScaler(inputCol='cluster_vector', outputCol='features')
kmeans = KMeans(k=28, seed=1)
pipeline = Pipeline(stages=[scaler, kmeans])

model = pipeline.fit(data)
predictions = model.transform(data)
cluster_user = predictions.filter(col('user_id') == user_id).select('prediction').first()[0]

movies_user = df.filter(col('user_id') == user_id).select('movie_id').rdd.map(lambda x: x[0]).collect()

top100 = df.join(predictions.select('user_id', 'prediction'), 'user_id')\
    .filter((col('prediction') == cluster_user) & (col('user_id') != user_id))\
    .filter(~col('movie_id').isin(movies_user))\
    .sort(col('vote').desc())\
    .select('movie_id')\
    .rdd.map(lambda row: row[0]).take(100)

print(top100)

movies_genres = movies_genre.groupby('movie_id').agg(F.collect_list('genre_id').alias('genres_arr'))
movies = movies.join(movies_genres, 'movie_id')\
    .filter(col('country').isNotNull())\
    .na.fill(1)

user_ratings = ratings.filter(col('user_id') == user_id)
user_movies = movies.join(user_ratings, 'movie_id').withColumnRenamed('vote', 'label')

predictions_data = movies.filter(col('movie_id').isin(top100))

scaler = StandardScaler(inputCol='features_vec', outputCol='features')
hfDirector = HashingFeature(inputCol='director', outputCol='director_hash')
hfCountry = HashingFeature(inputCol='country', outputCol='country_hash')
ohe = OneHotEncoderArray(inputCol='genres_arr', outputCol='genres_vec', size=32)
assembler = VectorAssembler(inputCols=[
    'year', 'genres_vec','count_reviews',
    'percent_good_reviews', 'budget', 'box_office',
    'country_hash', 'age', 'image', 'rating'], outputCol='features_vec')

rf = RandomForestRegressor(featuresCol="features_vec")

pipeline = Pipeline(stages=[hfCountry, ohe, assembler, scaler, rf])
model = pipeline.fit(user_movies)
predictions = model.transform(predictions_data)

predictions.sort(col('prediction').desc())\
    .select(F.lit(user_id).cast(IntegerType()).alias('user_id'), 'movie_id', F.lit('recommendation').alias('type'))\
    .limit(10)\
    .write.jdbc(mode='append', url='jdbc:postgresql://localhost:5432/movies_db', table='user_movies',
                properties={'user': 'ivan', 'password': 'qwerty'})


