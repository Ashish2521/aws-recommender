import boto3
import json

def calculate_cost(instance_type, service_code):
    pricing_client = boto3.client('pricing', region_name='us-east-1')
    
    response = pricing_client.get_products(
        ServiceCode=service_code,
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'US East (N. Virginia)'}
        ]
    )
    
    price_list = response['PriceList']
    if not price_list:
        return 'N/A'
    
    price_details = json.loads(price_list[0])
    price_dimensions = price_details['terms']['OnDemand']
    
    for term in price_dimensions.values():
        price_per_unit = term['priceDimensions']
        for dimension in price_per_unit.values():
            if 'USD' in dimension['pricePerUnit']:
                return dimension['pricePerUnit']['USD']
    
    return 'N/A'
