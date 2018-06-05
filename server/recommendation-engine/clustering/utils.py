from pyspark.ml.linalg import SparseVector, VectorUDT, Vectors
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param
from pyspark import keyword_only
from pyspark.sql.types import ArrayType, StringType, IntegerType
from pyspark.sql.functions import udf
import mmh3

class OneHotEncoderArray(Transformer, HasInputCol, HasOutputCol):

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, size=None):
        super(OneHotEncoderArray, self).__init__()
        self.size = Param(self, "size", "")
        self._setDefault(size=set())
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, outputCol=None, size=None):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setSize(self, value):
        self._paramMap[self.size] = value
        return self

    def getSize(self):
        return self.getOrDefault(self.size)

    def _transform(self, dataset):
        size = self.getSize()

        def f(genres_arr):
            genres_arr.sort()
            return SparseVector(size, genres_arr, [1]*len(genres_arr))

        t = VectorUDT()
        out_col = self.getOutputCol()
        in_col = dataset[self.getInputCol()]
        return dataset.withColumn(out_col, udf(f, t)(in_col))

class HashingFeature(Transformer, HasInputCol, HasOutputCol):

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None):
        super(HashingFeature, self).__init__()
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, outputCol=None):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def _transform(self, dataset):

        def f(x):
            return mmh3.hash(x)

        t = IntegerType()
        out_col = self.getOutputCol()
        in_col = dataset[self.getInputCol()]
        return dataset.withColumn(out_col, udf(f, t)(in_col))