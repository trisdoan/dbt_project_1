
from typing import Dict, List

def get_aws_creds() -> Dict[str, str]:
    return {
        "endpoint_url": 'http://cloud-store:9000',
        "aws_access_key_id": 'AKIAIOSFODNN7EXAMPLE',
        "aws_secret_access_key": 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        "region_name": 'us-east-1',
    }