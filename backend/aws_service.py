from utils.pricing import calculate_cost

#  Prashant and Rajit to make this data intensive so that we get best recommendations
EC2_RECOMMENDATIONS = {
    'CPU-intensive': {
        'low': 't3.micro',
        'medium': 't3.medium',
        'high': 'c5.large'
    },
    'Memory-intensive': {
        'low': 'r5.large',
        'medium': 'r5.xlarge',
        'high': 'r5.2xlarge'
    },
    'General-purpose': {
        'low': 't3.micro',
        'medium': 't3.medium',
        'high': 'm5.large'
    }
}

RDS_RECOMMENDATIONS = {
    'CPU-intensive': {
        'small': 'db.t3.small',
        'medium': 'db.m5.large',
        'large': 'db.m5.xlarge'
    },
    'General-purpose': {
        'small': 'db.t3.micro',
        'medium': 'db.t3.medium',
        'large': 'db.m5.large'
    }
}

def get_recommendations(service_type, num_users, workload_type, data_size):
    if service_type == 'EC2':
        return get_ec2_recommendations(num_users, workload_type)
    elif service_type == 'RDS':
        return get_rds_recommendations(data_size, workload_type)

def get_ec2_recommendations(num_users, workload_type):
    scale = 'low' if num_users < 50 else 'medium' if num_users < 200 else 'high'
    instance_type = EC2_RECOMMENDATIONS.get(workload_type, EC2_RECOMMENDATIONS['General-purpose'])[scale]
    cost = calculate_cost(instance_type, 'AmazonEC2')
    return [{'type': instance_type, 'cost': f'{cost} USD/month'}]

def get_rds_recommendations(data_size, workload_type):
    scale = 'small' if data_size < 100 else 'medium' if data_size < 500 else 'large'
    instance_type = RDS_RECOMMENDATIONS.get(workload_type, RDS_RECOMMENDATIONS['General-purpose'])[scale]
    cost = calculate_cost(instance_type, 'AmazonRDS')
    return [{'type': instance_type, 'cost': f'{cost} USD/month'}]

def generate_cloudformation_template(selected_resource):
    template = f"""
    AWSTemplateFormatVersion: '2010-09-09'
    Resources:
      MyInstance:
        Type: 'AWS::EC2::Instance'
        Properties:
          InstanceType: {selected_resource}
    """
    return template
