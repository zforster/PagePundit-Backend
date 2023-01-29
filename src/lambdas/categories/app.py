from typing import Dict

import lambdas.categories.service as service_layer


def get_categories(
    event: Dict,
    context: Dict,
) -> Dict:
    return {
        "statusCode": 200,
        "body": service_layer.get_categories(),
    }
