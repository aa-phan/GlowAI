def price_optimization(price=None):
    """
    Objective: Minimize price.
    Returns a score inversely proportional to the price.
    """
    if price is None or price <= 0:
        return 0  # Return 0 for invalid or missing price
    return 1 / (1 + price)

def rating_maximization(rating=None):
    """
    Objective: Maximize product rating.
    Returns the rating normalized to a 0-1 scale.
    """
    if rating is None or rating < 0 or rating > 5:
        return 0  # Return 0 for invalid or missing rating
    return rating / 5  # Assuming rating is out of 5

def skin_type_suitability(skin_type_booleans, target_skin_type):
    matches = sum(bool(skin_type_booleans.get(skin, False)) for skin in target_skin_type)
    return matches / len(target_skin_type) if target_skin_type else 0


def brand_preference(brand=None, preferred_brands=None):
    """
    Objective: Maximize preference for certain brands.
    brand: The brand of the product.
    preferred_brands: A list of preferred brands.
    """
    if brand is None or preferred_brands is None:
        return 0  # Return 0 if either parameter is missing
    return 1 if brand in preferred_brands else 0

def pareto_front(database_results):
    evaluated_products = []
    
    for product in database_results:
        price_score = price_optimization(product.get("price"))
        rating_score = rating_maximization(product.get("rank"))
        skin_score = skin_type_suitability({
                "combination": product.get("combination", False),
                "dry": product.get("dry", False),
                "normal": product.get("normal", False),
                "oily": product.get("oily", False),
                "sensitive": product.get("sensitive", False)
            }, ["sensitive","dry"])
        brand_score = brand_preference(product.get("brand"), ["CLINIQUE", "DRUNK ELEPHANT"])
        evaluated_products.append({
            "name": product["name"],
            "scores": {
                "price": price_score,
                "rating": rating_score,
                "skin": skin_score,
                "brand": brand_score
            }
        })
    
    pareto_front = []
    for i, product in enumerate(evaluated_products):
        dominated = False
        for j, other_product in enumerate(evaluated_products):
            if i != j:  # Don't compare the product with itself
                if all(other_product["scores"][key] >= product["scores"][key] for key in product["scores"]) and \
                   any(other_product["scores"][key] > product["scores"][key] for key in product["scores"]):
                    dominated = True
                    break
        if not dominated:
            pareto_front.append(product)
    
    return pareto_front