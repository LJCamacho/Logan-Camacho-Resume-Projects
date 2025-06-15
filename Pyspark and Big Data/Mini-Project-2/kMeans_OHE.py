#!/usr/bin/env python
# coding: utf-8

# # DS/CMPSC 410 MiniProject Deliverable #2
# 
# # Spring 2025
# ### Instructor: Prof. John Yen
# ### TA: Peng Jin and Jingxi Zhu
# 
# ### Learning Objectives
# - Be able to represent ports scanned by scanners as binary features using One Hot Encoding
# - Be able to apply k-means clustering to cluster the scanners based on the set of ports they scanned. 
# - Be able to identify the set of top k ports for one-hot encoding ports scanned.
# - Be able to interpret the results of clustering using cluster centers.
# - After successful clustering of the small Darknet dataset, conduct clustering on the large Darknet dataset (running spark in cluster mode).
# - Be able to evaluate the result of k-means clustering (cluster mode) using Silhouette score and Mirai labels.
# - Be able to use .persist() and .unpersist() to improve the scalability/efficiency of PySpark code.
# 
# ### Total points: 120 
# - Problem 1A: 5 points
# - Problem 1B: 5 points
# - Problem 1C: 10 points
# - Problem 2: 10 points 
# - Problem 3: 10 points 
# - Problem 4: 5 points
# - Problem 5: 10 points
# - Problem 6: 10 points
# - Problem 7: 15 points
# - Problem 8: 40 points
# 
# ### Items for Submission: 
# - Completed Jupyter Notebook for local mode (HTML format)
# - .py file for successful execution in cluster mode 
# - log file (including execution time information) for successful execution in cluster mode
# - The csv file (generated in cluster mode) for Mirai Ratio and Cluster Centers for all clusters
# - The csv file (generated in cluster mode) for sorted count of scanners that scan the same number of ports
# - The first data file (i.e., part-00000) (generated in cluster mode) in ``sorted_top_ports_counts.txt``
#   
# ### Due: 11:59 pm, April 11, 2025
# ### Early Submission bonus (before midnight April 6, 2025): 12 points

# In[1]:


import pyspark
import csv


# In[2]:


from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, LongType, IntegerType, DecimalType, BooleanType
from pyspark.sql.functions import col, column
from pyspark.sql.functions import expr
from pyspark.sql.functions import split
from pyspark.sql.functions import array_contains
from pyspark.sql import Row
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler, IndexToString
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator


# In[3]:


ss = SparkSession.builder.appName("MiniProject 2 k-meas Clustering using OHE").getOrCreate()


# In[4]:


ss.sparkContext.setLogLevel("WARN")


# # Problem 1A (5 points)
# Complete the path for input file in the code below and enter your name in this Markdown cell:
# - Name: Logan Camacho
# ## Note: You will need to change the name of the input file in the cluster mode to `Day_2020_profile.csv`

# In[5]:


scanner_schema = StructType([StructField("_c0", IntegerType(), False),                              StructField("id", IntegerType(), False ),                              StructField("numports", IntegerType(), False),                              StructField("lifetime", DecimalType(), False ),                              StructField("Bytes", IntegerType(), False ),                              StructField("Packets", IntegerType(), False),                              StructField("average_packetsize", IntegerType(), False),                              StructField("MinUniqueDests", IntegerType(), False),                             StructField("MaxUniqueDests", IntegerType(), False),                              StructField("MinUniqueDest24s", IntegerType(), False),                              StructField("MaxUniqueDest24s", IntegerType(), False),                              StructField("average_lifetime", DecimalType(), False),                              StructField("mirai", BooleanType(), True),                              StructField("zmap", BooleanType(), True),
                             StructField("masscan", BooleanType(), True),
                             StructField("country", StringType(), False), \
                             StructField("traffic_types_scanned_str", StringType(), False), \
                             StructField("ports_scanned_str", StringType(), False), \
                             StructField("host_tags_per_censys", StringType(), False), \
                             StructField("host_services_per_censys", StringType(), False) \
                           ])


# In[10]:


Scanners_df = ss.read.csv("/storage/home/ljc5809/work/MiniProj2/Day_2020_profile.csv", schema= scanner_schema, header= True, inferSchema=False )


# ## We can use printSchema() to display the schema of the DataFrame Scanners_df to see whether it was consistent with the schema.

# In[11]:


Scanners_df.printSchema()


# # In this lab, our goal is to answer the question:
# ## Q: What groups of scanners are similar in the ports they scan?
# 
# ### Because we know (from MiniProject 1) about two third of the scanners scan only 1 port, we can exclude them so that we focus on the grouping of those scanners that scan at least two ports.

# ### Because the feature `numports` record the total number of ports being scanned by each scanner, we can use it to separate 1-port-scanners from multi-port-scanners.

# In[12]:


one_port_scanners = Scanners_df.where(col('numports') == 1)


# In[13]:





# In[14]:


multi_port_scanners = Scanners_df.where(col("numports") > 1)


# In[15]:


multi_port_scanners_count = multi_port_scanners.count()


# In[16]:





# # Before clustering, it can be useful to understand the distribution of scanners based on the number of ports they scan.
# # Because the column "numports' already contain the information about the number of ports each scanner (represented by a row in the input csv file), we can use `groupby("numports")` on `Scanners_df` followed by `.count()` 

# In[17]:


ScannersCount_byNumPorts = Scanners_df.groupby("numports").count()


# In[18]:


SortedScannersCount_byNumPorts= ScannersCount_byNumPorts.orderBy("count", ascending=False)


# In[19]:





# In[21]:


output1 = "/storage/home/ljc5809/work/MiniProj2/clusterV2/SortedScannersCount_byNumPorts_Cluster.csv"
SortedScannersCount_byNumPorts.write.option("header", True).csv(output1)


# # What is the maximum and average of number of ports being scanned?

# # Problem 1B (5 points)
# ## Use `agg` method of DataFrame to find the maximal and average number of ports being scanned across all scanners.

# In[23]:


MaxNumPorts = Scanners_df.agg({"numports" : "max"})


# In[24]:





# In[25]:


AvgNumPorts = Scanners_df.agg({"numports" : "avg"})


# In[26]:





# # We can also find scanners that scan many ports by investigating scanners whose numports is unique (one-of-a-kind, a unicorn)

# In[27]:


ScannersCount_byNumPorts.where(col("count")==1).show(10)


# # We noticed that some of the scanners that scan for very large number of ports (we call them Extreme Scanners) is unique in the number of ports they scan.
# ## A heuristic to separate extreme scanners: Find the largest number of ports that are scanned by at least two scanners. Use the number as the threshold to filter extreme scanners.

# In[28]:


non_rare_NumPorts = SortedScannersCount_byNumPorts.where(col("count") > 1)


# In[29]:





# # DataFrame can aggregate a column using .agg({ "column name" : "operator name" })
# ## We can find the maximum of numports column using "max" as aggregation operator.
# ## The result is a DataFrame with only column named as ``<operator name>(<column name>)``

# In[30]:


max_non_rare_NumPorts_df = non_rare_NumPorts.agg({"numports" : "max"})


# # We want to record this number, rather than using the number (654) as a constant in the code below.
# ## Why?
# ## Because the number is based on the data, which is different for the cluster mode.

# In[31]:


max_non_rare_NumPorts_rdd = max_non_rare_NumPorts_df.rdd.map(lambda x: x[0])


# In[32]:


max_non_rare_NumPorts_list = max_non_rare_NumPorts_rdd.collect()


# In[33]:


max_non_rare_NumPorts=max_non_rare_NumPorts_list[0]


# ## We are going to focus on the grouping of scanners that scan at least two ports, and do not scan extremely large number of ports. We will call these scanners Non-extreme Multi-port Scanners.
# ## We will save the extreme scanners in a csv file so that we can process it separately.

# In[34]:


extreme_scanners = Scanners_df.where(col("numports") > max_non_rare_NumPorts)


# In[35]:


path2="/storage/home/ljc5809/work/MiniProj2/clusterV2/Extreme_Scanners_Cluster.csv"
extreme_scanners.write.option("header",True).csv(path2)


# In[36]:


non_extreme_multi_port_scanners = Scanners_df.where(col("numports") <= max_non_rare_NumPorts).where(col("numports") > 1)


# In[37]:


non_extreme_multi_port_scanners.persist()


# In[38]:


non_extreme_multi_port_scanners.count()


# # Part A: One Hot Encoding of Top 100 Ports
# We want to apply one hot encoding to the top 100 ports scanned by scanners. 
# - A1: Find top k ports scanned by non_extreme_multi_port scanners (This is similar to the first part of MiniProject 1)
# - A2: Generate One Hot Encodding for these top k ports

# In[39]:





# # For each port scanned, count the Total Number of Scanners that Scan the Given Port
# Like MiniProject 1, to calculate this, we need to 
# - (a) convert the ports_scanned_str into an array/list of ports
# - (b) Convert the DataFrame into an RDD
# - (c) Use flatMap to count the total number of scanners for each port.

# # The Following Code Implements the three steps.
# ## (a) Create a new column "Ports_Array" by splitting the column "ports_scanned_str" using "-" as the delimiter.

# In[40]:


# (a)
NEMP_Scanners_df=non_extreme_multi_port_scanners.withColumn("Ports_Array", split(col("ports_scanned_str"), "-") )


# # We will need to use NEMP_Scanners_df multiple times in creating OHE features later, so we persist it.

# In[41]:


NEMP_Scanners_df.persist()


# ## (b) We convert the column ```Ports_Array``` into an RDD so that we can apply flatMap for counting the number of scanners, among those that scan at least two ports, but not extreme scanners, that scan each port.

# In[42]:


Ports_Scanned_RDD = NEMP_Scanners_df.select("Ports_Array").rdd


# In[43]:





# ## (c) Because each port number in the Ports_Array column for each row/scanner occurs only once, we can count the total number of scanners by counting the total occurance of each port number through flatMap.
# ### Because each element of the ``Ports_Scanned_RDD`` rdd is a Row object, we need to first extract ``Ports_Array`` from the row object.
# # Problem 1C (10%) Complete the code below to count the total number of scanners that scan a port using ``flatMap`` and ``reduceByKey`` (like miniProject 1).

# In[44]:





# In[45]:


Ports_list_RDD = Ports_Scanned_RDD.map(lambda row: row.Ports_Array )


# In[46]:





# In[47]:


flattened_Ports_list_RDD = Ports_list_RDD.flatMap(lambda x: x )


# In[48]:





# In[49]:


Port_1_RDD = flattened_Ports_list_RDD.map(lambda x: (x,1))


# In[50]:


Port_count_RDD = Port_1_RDD.reduceByKey(lambda x,y: x+y, 5)


# # Problem 2 (10%) 
# ### Complete The code below to find top k ports scanned by non-extreme multi-port scanners using ``sortByKey``, like mini-project 1.
# ### We will set k to 120 for mini-project 2.

# In[51]:


Sorted_Count_Port_RDD = Port_count_RDD.map(lambda x: (x[1],x[0])).sortByKey( ascending = False)


# In[52]:


top_ports = 120


# In[53]:


path3="/storage/home/ljc5809/work/MiniProj2/clusterV2/sorted_top_ports_counts_Cluster"
Sorted_Count_Port_RDD.saveAsTextFile(path3)


# # Because we have applied ``persist()`` on ``NEMP_scanners_DF``, and the above action has generated the NEMP_scanners_DF, we can release the resource of ``non_extreme_multi_port_scanners`` because we don't need it in the rest of the code.

# In[54]:


non_extreme_multi_port_scanners.unpersist()


# # Like miniproject 1, we want to get a list of k top ports.  However, unlike miniproject 1, we use the list of k top ports to create One Hot Encoding for each top port in the list.
# # We use the top k ports for One Hot Encoding
# # The value of top_ports (120) is assigned in Problem 2

# In[55]:


Sorted_Ports_RDD= Sorted_Count_Port_RDD.map(lambda x: x[1] )
Top_Ports_list = Sorted_Ports_RDD.take(top_ports)


# In[56]:





# In[57]:





# #  A.2 One Hot Encoding of Top K Ports
# ## One-Hot-Encoded Feature/Column Name
# Because we need to create a name for each one-hot-encoded feature, which is one of the top k ports, we can adopt the convention that the column name is "PortXXXX", where "XXXX" is a port number. This can be done by concatenating two strings using ``+``.

# In[58]:


Top_Ports_list[1]


# In[59]:


FeatureName = "Port"+Top_Ports_list[1]


# In[60]:


FeatureName


# ## One-Hot-Encoding using withColumn and array_contains

# # Problem 3 (10 points) Complete the code below for One-Hot-Encoding of the SECOND top port.

# In[61]:


from pyspark.sql.functions import array_contains


# In[67]:


NEMP_Scanners2_df= NEMP_Scanners_df.withColumn("Port"+Top_Ports_list[1], array_contains("Ports_Array", Top_Ports_list[1]))


# In[68]:





# ## Verify the Correctness of One-Hot-Encoded Feature
# ## Problem 4 (5 points)
# ### Check whether one-hot encoding of the second top port is encoded correctly by completing the code below and enter your answer the in the next Markdown cell.

# In[69]:


Second_top_port_scanners_count = NEMP_Scanners2_df.where(col("Port"+Top_Ports_list[1])== True).count()


# In[70]:





# In[71]:





# ## Answer for Problem 4:
# - The second top port is : 17130
# - The total number of scanners that scan the secont top port, based on ``Sorted_Count_Port_RDD`` is:  25134
# - Is this number the same as the number of scanners whose One-Hot-Encoded feature of the second top port is True?    Yes, both the number from the Second_top_port_scanners_count is the same as the number of scanners next to port 17130 from the Sorted_Count_Port.RDD

# ## Generate Hot-One Encoded Feature for each of the top k ports in the Top_Ports_list
# 
# - Iterate through the Top_Ports_list so that each top port is one-hot encoded into the DataFrame for non-extreme multi-port scanners (i.e., `NEMP_Scanners2.df`).

# ## Problem 5 (10 points)
# Complete the following PySpark code for encoding the top n ports using One Hot Encoding, where n is specified by the variable ```top_ports```

# In[72]:


top_ports


# In[73]:


Top_Ports_list[top_ports - 1]


# In[74]:


for i in range(0, top_ports):
    # "Port" + Top_Ports_list[i]  is the name of each new feature created through One Hot Encoding Top_Ports_list
    NEMP_Scanners3_df = NEMP_Scanners2_df.withColumn("Port" + Top_Ports_list[i], array_contains("Ports_Array",Top_Ports_list[i]))
    NEMP_Scanners2_df = NEMP_Scanners3_df


# In[75]:


NEMP_Scanners2_df.printSchema()


# # Problem 6 (10 points)
# ## Complete the code below to use k-means (number of clusters = 200) to cluster non-extreme multi-port scanners using one-hot-encoded top 120 ports.

# ## Specify Parameters for k Means Clustering

# In[76]:


input_features = [ ]
for i in range(0, top_ports ):
    input_features.append( "Port"+ Top_Ports_list[i] )


# In[77]:





# In[78]:


va = VectorAssembler().setInputCols(input_features).setOutputCol("features")


# In[79]:


data= va.transform(NEMP_Scanners2_df)


# In[80]:





# In[81]:


data.persist()


# In[82]:


km = KMeans(featuresCol= "features", predictionCol="prediction").setK(200).setSeed(127)
km.explainParams()


# In[83]:


kmModel=km.fit(data)


# In[84]:


kmModel


# In[85]:


predictions = kmModel.transform(data)


# In[86]:





# # Find The Size of The First Cluster

# In[87]:


Cluster1_df=predictions.where(col("prediction")==0)


# In[88]:


Cluster1_df.count()


# In[89]:


summary = kmModel.summary


# In[90]:


summary.clusterSizes


# In[91]:


evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)


# In[92]:





# In[93]:


centers = kmModel.clusterCenters()


# In[94]:





# # Record cluster index, cluster size, percentage of Mirai scanners, and cluster centers for each clusters formed.
# ## The value of cluster center for a OHE top port is the percentage of data/clusters in the cluster that scans the top port. For example, a cluster center `[0.094, 0.8, 0, ...]` indicates the following
# - 9.4% of the scanners in the cluster scan Top_Ports_list[0]: port 17132
# - 80% of the scanners in the cluster scan Top_Ports_list[1]: port 17130
# - No scanners in the cluster scan Top_Ports_list[2]: port 17140

# # Problem 7 (15 points) Complete the code below for computing the percentage of Mirai scanners for each scanner, and record it together with cluster centers for each cluster. Add persist to PySpark DataFrames that are used multiple times.  Add unpersist whenever the resource for a PySpark DataFrame is no longer needed.

# In[95]:


import pandas as pd
import numpy as np
import math


# In[96]:


# Define columns of the Pandas dataframe
column_list = ['cluster ID', 'size', 'mirai_ratio' ]
cluster_num =200
predictions.persist()
for feature in input_features:
    column_list.append(feature)
clusters_summary_df = pd.DataFrame( columns = column_list )
for i in range(0, cluster_num):
    cluster_i = predictions.where(col('prediction')==i)
    cluster_i_size = cluster_i.count()
    cluster_i_mirai_count = cluster_i.where(col('mirai')).count()
    cluster_i_mirai_ratio = cluster_i_mirai_count/cluster_i_size
    if cluster_i_mirai_count > 0:
        print("Cluster ", i, "; Mirai Ratio:", cluster_i_mirai_ratio, "; Cluster Size: ", cluster_i_size)
    cluster_row = [i, cluster_i_size, cluster_i_mirai_ratio]
    for j in range(0, len(input_features)):
        cluster_row.append(centers[i][j])
    clusters_summary_df.loc[i]= cluster_row
predictions.unpersist()


# In[97]:


# Create a file name based on the number of top_ports
path4= "/storage/home/ljc5809/work/MiniProj2/clusterV2/MiraiRatio_Cluster_centers_"+"OHE"+ str(top_ports)+"top_ports"+"_k200_Cluster"
clusters_summary_df.to_csv(path4, header=True)


# # Problem 8 (40 points)
# - Modify the Jupyter Notebook for running in cluster mode using the big dataset (Day_2020_profile.csv). 
# - Make sure you change the output directory from `../local/..` to `../cluster/..` so that it does not destroy the result you obtained in local mode.
# - Add suitable persist and unpersist for Problem 7.
# - If you want to compare performance of different persist options, make sure you change the output directory (e.g., ``../cluster_np/`` for without persist).
# - Run the .py file the cluster mode. The following submission items (in addition to the completed Jupyter Notebook for local mode) are generated from the cluster mode.
# - Submit the .py file 
# - Submit the the log file that contains the run time information for a successful execution in the cluster mode.
# - Submit the csv file that records the mirai percentage and cluster centers in the cluster mode.
# - Submit the csv file that contains count of scanners that scan the same number of ports.
# - Submit the first data file (part-00000) in ``sorted_top_ports_counts.txt``

# In[98]:


ss.stop()


# In[ ]:




