from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, LambdaFunction
from diagrams.aws.integration import SNS
from diagrams.aws.compute import EC2
from diagrams.aws.database import Dynamodb, RDS
from diagrams.onprem.client import Users, User
from diagrams.onprem.compute import Server
from diagrams.onprem.workflow import Airflow


def main():
    with Diagram('A basic data pipeline in AWS Cloud', show=False, filename='img/basic_data_pipeline'):
        users = [User('User 1'), User('User 2'), User('User n')]
        with Cluster('AWS'):
            raw_bucket = S3('Raw data')
            rds = RDS('RDS')
            airflow = Airflow('Airflow')

        users >> Edge(label='CSV file') >> raw_bucket >> Edge(label='all files') >> airflow
        airflow >> Edge(label='save') >> rds

    with Diagram('Data pipeline with data quality check in AWS Cloud', show=False, filename='img/data_quality_data_pipeline'):
        users = [User('User 1'), User('User 2'), User('User n')]
        with Cluster('AWS'):
            raw_bucket = S3('Raw data')
            lambda_ = Lambda('Lambda Function')
            check_bucket = S3('Checked data')
            sns = SNS('SNS')
            airflow = Airflow('Airflow')
            rds = RDS('RDS')


        users >> Edge(label='CSV file') >> raw_bucket >> Edge(label='trigger') >> lambda_
        lambda_ >> Edge(label='good files', style='dashed', color='darkgreen') >> check_bucket >> airflow >> rds
        lambda_ >> Edge(label='bad files' ,style='dashed', color='firebrick') >> sns

if __name__=='__main__':
    main()