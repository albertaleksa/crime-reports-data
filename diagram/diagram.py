from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import BigQuery, Dataproc
from diagrams.gcp.storage import GCS
from diagrams.generic.blank import Blank
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.container import Docker
from diagrams.onprem.analytics import Spark, Dbt
from diagrams.onprem.iac import Terraform
from diagrams.programming.language import Python
from diagrams.generic.blank import Blank

graph_attr = {
    "fontsize": "30",  # Set Cluster label font size
}

graph_attr_inner = {
    "fontsize": "20",  # Set Cluster label font size
}

node_attr = {
    "fontsize": "20",  # Set node label font size
    "fontname": "Helvetica-bold",
}

edge_attr = {
    "fontsize": "25",  # Set edge label font size
    "fontname": "Helvetica-bold",
}


with Diagram("Data Engineering Architecture", show=False, direction="LR", graph_attr=graph_attr, node_attr=node_attr):

    with Cluster("",
                 graph_attr={
                     "bgcolor": "lightgrey",
                     "fontsize": "30"
                 }):
        with Cluster("Ingestion",
                     graph_attr={
                         "bgcolor": "moccasin",
                         "fontsize": "30"
                     }):
            with Cluster("Internet", graph_attr=graph_attr_inner):
                files = [Custom("file 1", "csv.png"),
                         Custom("file 2", "csv.png")]
            with Cluster("Local file", graph_attr=graph_attr_inner):
                spark_job = Python("Spark job")

            gcs = GCS("Google Cloud Storage\nData Lake")

        with Cluster("Transformation",
                     graph_attr={
                         "bgcolor": "aliceblue",
                         "fontsize": "30"
                     }):
            with Cluster(""):
                spark = Spark()
                dataproc = Dataproc("Dataproc\nCluster")

            bl1 = Blank(height="2.2")
            # bl1 = Docker()
            # bl2 = Docker()

            bigquery = BigQuery("BigQuery\nData Warehouse")
            dbt = Dbt()

        with Cluster("Visualization",
                     graph_attr={
                         "bgcolor": "mistyrose",
                         "fontsize": "30"
                     }):
            looker = [Blank(),
                      Custom("", "Looker.jpeg", height="2"),
                      Blank(height="2.5")]


    with Cluster("Orchestration",
                 graph_attr={
                    "bgcolor": "honeydew",
                    "fontsize": "30"
                 }):
        bl_orch = Blank()
        prefect = Custom("", "Prefect.png", width="2.5")
        Blank(width="1.8") >> Edge(style="invis") \
            >> bl_orch >> Edge(style="invis") \
            >> Blank() >> Edge(style="invis") \
            >> prefect >> Edge(style="invis") \
            >> Blank() >> Edge(style="invis") \
            >> Blank(width="2.6")

    with Cluster("Infrastructure",
                 graph_attr={
                     "bgcolor": "thistle",
                     "fontsize": "30"
                 }) as cls2:
        terraform = Terraform("", width="1.8")
        bl_inf = Blank()
        docker = Docker("Docker", width="2.6")
        terraform >> Edge(style="invis") \
            >> Blank() >> Edge(style="invis") \
            >> bl_inf >> Edge(style="invis") \
            >> Blank() >> Edge(style="invis") \
            >> Blank() >> Edge(style="invis")\
            >> docker

    spark_job >> Edge(style="invis") \
        >> bl_orch >> Edge(style="invis") \
        >> bl_inf

    files >> Edge(label="Upload", color="blue", style="bold", **edge_attr) \
        >> gcs
    spark_job >> Edge(label="Upload", color="blue", style="bold", **edge_attr) \
        >> gcs
    gcs >> Edge(color="darkgreen", style="bold", **edge_attr) \
        >> spark

    spark - Edge(label="Running\na Spark job", color="brown", style="dotted", **edge_attr)\
        - dataproc
    spark >> Edge(color="black", style="bold", **edge_attr) \
        >> bigquery

    bigquery >> Edge(label="Data\nTransformation", color="darkgreen", style="bold", **edge_attr) << dbt

    bigquery >> Edge(label="Visualize\ndata", color="black", style="bold", **edge_attr)\
        >> looker[1]
    dbt >> Edge(style="invis") >> looker[0]

