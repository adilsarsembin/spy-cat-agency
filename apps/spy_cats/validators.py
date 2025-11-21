import requests
from rest_framework import serializers
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


def get_valid_breeds():
    cache_key = 'thecatapi_breeds'
    breeds = cache.get(cache_key)
    
    if breeds is None:
        try:
            response = requests.get('https://api.thecatapi.com/v1/breeds', timeout=5)
            if response.status_code == 200:
                breeds_data = response.json()
                breeds = [breed['name'] for breed in breeds_data]
                cache.set(cache_key, breeds, 60 * 60 * 24)
                logger.info(f"Successfully fetched {len(breeds)} breeds from TheCatAPI")
            else:
                logger.warning(f"TheCatAPI returned status code {response.status_code}")
                breeds = []
        except requests.Timeout:
            logger.error("Timeout while fetching breeds from TheCatAPI")
            breeds = []
        except requests.RequestException as e:
            logger.error(f"Error fetching breeds from TheCatAPI: {str(e)}")
            breeds = []
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing breeds from TheCatAPI response: {str(e)}")
            breeds = []
    
    return breeds


def validate_breed(value):
    if not value:
        raise serializers.ValidationError("Breed is required.")
    
    if not isinstance(value, str):
        raise serializers.ValidationError("Breed must be a string.")
    
    value = value.strip()
    if not value:
        raise serializers.ValidationError("Breed cannot be empty.")
    
    valid_breeds = get_valid_breeds()
    
    if not valid_breeds:
        raise serializers.ValidationError(
            "Unable to validate breed at this time. TheCatAPI is unavailable. "
            "Please try again later."
        )
    
    if value not in valid_breeds:
        raise serializers.ValidationError(
            f"'{value}' is not a recognized cat breed according to TheCatAPI. "
            f"Please use a valid breed name."
        )
    
    return value
