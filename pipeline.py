import boto3

# Define your AWS resources and configuration
pipeline_name = 'github-lambda-ecr'
region = 'us-east-1'
lambda_function_name = 'github-to-lambda-demo'
github_owner = 'PraveenKumar-Kasoju'
github_repo = 'Lambda-Ecr'
github_branch = 'main'
github_token = 'your-github-token'
codebuild_project_name = 'github-lambda-ecr'
artifact_store_s3_bucket = 'lambda-deploy-bucket'
codepipeline_role_arn = 'arn:aws:iam::506236563550:role/github-lambda-ecr-role'

# Create the CodePipeline client
codepipeline_client = boto3.client('codepipeline', region_name=region)

# Define the pipeline structure
pipeline = {
    'name': pipeline_name,
    'roleArn': codepipeline_role_arn,
    'artifactStore': {
        'type': 'S3',
        'location': artifact_store_s3_bucket
    },
    'stages': [
        {
            'name': 'Source',
            'actions': [
                {
                    'name': 'SourceAction',
                    'actionTypeId': {
                        'category': 'Source',
                        'owner': 'ThirdParty',
                        'provider': 'GitHub',
                        'version': '1'
                    },
                    'outputArtifacts': [
                        {
                            'name': 'SourceOutput'
                        }
                    ],
                    'configuration': {
                        'Owner': github_owner,
                        'Repo': github_repo,
                        'Branch': github_branch,
                        'OAuthToken': github_token
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
                            'name': 'SourceOutput'
                        }
                    ],
                    'outputArtifacts': [
                        {
                            'name': 'BuildOutput'
                        }
                    ],
                    'configuration': {
                        'ProjectName': codebuild_project_name
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
                            'name': 'BuildOutput'
                        }
                    ],
                    'configuration': {
                        'FunctionName': lambda_function_name
                    },
                    'runOrder': 1
                }
            ]
        }
    ]
}

# Create or update the pipeline
try:
    response = codepipeline_client.get_pipeline(name=pipeline_name)
    print(f"Pipeline {pipeline_name} exists. Updating...")
    response = codepipeline_client.update_pipeline(pipeline=pipeline)
except codepipeline_client.exceptions.PipelineNotFoundException:
    print(f"Pipeline {pipeline_name} does not exist. Creating...")
    response = codepipeline_client.create_pipeline(pipeline=pipeline)

print(response)
