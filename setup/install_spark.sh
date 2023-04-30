#!/bin/sh

echo "=== Run install_spark.sh..."

mkdir -p $HOME/spark
cd spark

# Download Java
echo "=== Download Java..."
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
# Remove the archive
rm openjdk-11.0.2_linux-x64_bin.tar.gz

# Download Spark
echo "=== Download Spark..."
wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
tar xzfv spark-3.3.2-bin-hadoop3.tgz
# Remove the archive
rm spark-3.3.2-bin-hadoop3.tgz

# Append the exports to .bashrc
echo 'export JAVA_HOME="${HOME}/spark/jdk-11.0.2"' >> ~/.bashrc
echo 'export PATH="${JAVA_HOME}/bin:${PATH}"' >> ~/.bashrc
echo 'export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"' >> ~/.bashrc
echo 'export PATH="${SPARK_HOME}/bin:${PATH}"' >> ~/.bashrc

# PySpark
# Add exports to .bashrc
echo 'export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"' >> ~/.bashrc
echo 'export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"' >> ~/.bashrc

# Re-evaluate .bashrc
source ~/.bashrc
