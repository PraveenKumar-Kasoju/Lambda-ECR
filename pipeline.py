import boto3

pipeline_name = 'my-pipeline'
ecr_repo_name = 'my-ecr-repo'
lambda_function_name = 'my-lambda-function'
s3_bucket = 'my-codepipeline-bucket'
source_artifact_name = 'source_output'
build_artifact_name = 'build_output'

codepipeline = boto3.client('codepipeline')
s3 = boto3.client('s3')

def create_pipeline():
    response = codepipeline.create_pipeline(
        pipeline={
            'name': pipeline_name,
            'roleArn': 'arn:aws:iam::YOUR_ACCOUNT_ID:role/AWS-CodePipeline-Service',
            'artifactStore': {
                'type': 'S3',
                'location': s3_bucket,
            },
            'stages': [
                {
                    'name': 'Source',
                    'actions': [
                        {
                            'name': 'SourceAction',
                            'actionTypeId': {
                                'category': 'Source',
                                'owner': 'AWS',
                                'provider': 'S3',
                                'version': '1'
                            },
                            'outputArtifacts': [
                                {
                                    'name': source_artifact_name
                                }
                            ],
                            'configuration': {
                                'S3Bucket': s3_bucket,
                                'S3ObjectKey': 'source.zip',
                            },
                            'runOrder': 1
                        }
                    ]
                },
                {
                    'name': 'Build',
                    'actions': [
                        {
                            'name': 'BuildAction',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'inputArtifacts': [
                                {
                                    'name': source_artifact_name
                                }
                            ],
                            'outputArtifacts': [
                                {
                                    'name': build_artifact_name
                                }
                            ],
                            'configuration': {
                                'ProjectName': 'my-codebuild-project',
                            },
                            'runOrder': 1
                        }
                    ]
                },
                {
                    'name': 'Deploy',
                    'actions': [
                        {
                            'name': 'DeployAction',
                            'actionTypeId': {
                                'category': 'Deploy',
                                'owner': 'AWS',
                                'provider': 'Lambda',
                                'version': '1'
                            },
                            'inputArtifacts': [
                                {
                                    'name': build_artifact_name
                                }
                            ],
                            'configuration': {
                                'FunctionName': lambda_function_name,
                                'UserParameters': '{"ImageUri": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest"}',
                            },
                            'runOrder': 1
                        }
                    ]
                }
            ],
            'version': 1
        }
    )

    return response

if __name__ == "__main__":
    create_pipeline()
