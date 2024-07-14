from flask_restful import Api, Resource
from flask import jsonify, make_response, request
from main.redis import get_cached_data_or_fetch
import json

# Resource for handling /properties endpoint
class PropertyListResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        properties = get_cached_data_or_fetch()
        total_count = len(properties)
        
        paginated_properties = properties[(page - 1) * per_page: page * per_page]
        
        if len(paginated_properties) == 0:
            response = make_response(jsonify(
                {'message': 'No data available'}), 404
                )
            response.headers['Content-Type'] = 'application/json'
            return response
        
        result = {
            'count': len(paginated_properties),
            'total_count': total_count,
            'limit': per_page,
            'next_page': page + 1 if len(paginated_properties) == per_page else None,
            'previous_page': page - 1 if page > 1 else None,
            'results': [prop for prop in paginated_properties]
        }
        
        response = make_response(jsonify(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

class PropertyListByTypeResource(Resource):
    def get(self, selected_option):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        properties = get_cached_data_or_fetch(selected_option)
        total_count = len(properties)
        
        paginated_properties = properties[(page - 1) * per_page: page * per_page]
        
        if len(paginated_properties) == 0:
            response = make_response(jsonify(
                {'message': 'Could not find data, make sure you are using the correct Type'}), 404
                )
            response.headers['Content-Type'] = 'application/json'
            return response
        
        result = {
            'count': len(paginated_properties),
            'total_count': total_count,
            'limit': per_page,
            'next_page': page + 1 if len(paginated_properties) == per_page else None,
            'previous_page': page - 1 if page > 1 else None,
            'results': [prop for prop in paginated_properties]
        }
        
        response = make_response(jsonify(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
