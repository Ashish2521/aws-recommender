from flask import Flask, request, jsonify
from flask_cors import CORS
import aws_service

app = Flask(__name__)
CORS(app)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    num_users = data.get('num_users')
    workload_type = data.get('workload_type')
    data_size = data.get('data_size')
    
    # Get EC2 and RDS recommendations
    ec2_recommendations = aws_service.get_ec2_recommendations(num_users, workload_type)
    # rds_recommendations = aws_service.get_rds_recommendations(data_size, workload_type)

    # Combine recommendations
    # recommendations = ec2_recommendations + rds_recommendations
    recommendations = ec2_recommendations 
    
    return jsonify(recommendations)

@app.route('/api/generate-template', methods=['POST'])
def generate_template():
    selected_resource = request.json.get('selected_resource')
    template = aws_service.generate_cloudformation_template(selected_resource)
    return jsonify({'template': template})

if __name__ == '__main__':
    app.run(debug=True)
