import json
from main.app import redis_client, db
from main.database.models.models import Property

# redis_client.delete('properties')

def get_cached_data_or_fetch(selected_option=None):
    cached_data = redis_client.get('properties')
    
    if cached_data:
        data = json.loads(cached_data)
        
        if selected_option is not None:
            filtered_data = [item for item in data if item["roll"] == selected_option]
            return filtered_data
        else:
            return data
    else:
        queryset = db.session.query(Property)
        
        if selected_option is not None:
            queryset = queryset.filter(Property.roll == selected_option)
        
        query_data = [instance.json() for instance in queryset.all()]
        serialized_data = json.dumps(query_data)
        
        try:
            redis_client.set('properties', serialized_data)
            redis_client.expire('properties', 3600)
        except TypeError as e:
            print(f"Serialization error: {e}")
            print(f"Data: {query_data}")
        
        return query_data
