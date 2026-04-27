import json
import os
from typing import List, Dict, Optional

def load_catalog() -> List[Dict]:
    catalog_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'catalog.json')
    with open(catalog_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_products(query: str = "", max_price_aed: Optional[float] = None, age_months: Optional[int] = None) -> List[Dict]:
    """
    Search the catalog for products matching the given criteria.
    This is a simplified mock search that filters by budget, age, and a basic keyword match.
    """
    catalog = load_catalog()
    results = []
    
    # Simple keyword match
    query_terms = [t.lower() for t in query.split()] if query else []
    
    for product in catalog:
        # Check budget
        if max_price_aed is not None and product['price_aed'] > max_price_aed:
            continue
            
        # Check age
        if age_months is not None:
            min_age = product.get('age_min_months')
            max_age = product.get('age_max_months')
            
            # If product has age constraints and the child's age falls outside, skip it.
            # Gifts for moms (like spa sets) have null age constraints, which means they are for any age.
            if min_age is not None and age_months < min_age:
                continue
            if max_age is not None and age_months > max_age:
                continue
                
        # Keyword check (if query provided)
        if query_terms:
            text_to_search = (product['name'] + " " + product['description'] + " " + " ".join(product['categories'])).lower()
            # If NO terms match, we skip (a very naive search).
            # A better search would use embeddings, but this suffices for the mock.
            if not any(term in text_to_search for term in query_terms):
                continue
                
        results.append(product)
        
    return results

if __name__ == "__main__":
    print(search_products(query="dinosaur", max_price_aed=150, age_months=36))
