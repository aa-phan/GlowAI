from databases import find_products, initialize_supabase
import pareto_set
from llm_analysis import analyze_pareto_products
import requests, os
from llm_analysis import rag_ingredients
import glob


def product_select(ingredients=None, exclude_ingredients=None, max_price=None, combination=None, dry=None, normal=None, oily=None, sensitive=None, product_type=None, analyze_with_llm=False):
    database_set = find_products(ingredients, exclude_ingredients, max_price, combination, dry, normal, oily, sensitive, product_type)
       
    pareto_results = pareto_set.pareto_front(database_set, max_price, combination, dry, normal, oily, sensitive)
    
    if analyze_with_llm:
        return analyze_pareto_products(pareto_results)
        
    else:     
        print("\nPareto-optimal products:")
        for i, product in enumerate(pareto_results, start=1):
            print(f"\n{i}. {product['name']}")
            print("Scores:")
            for objective, score in product['scores'].items():
                print(f"  {objective}: {score:.2f}")

    
                
def main():
    images_folder = r"C:\Users\Aaron\Documents\Facial-Skincare-Analysis\training\images"
    image_files = glob.glob(os.path.join(images_folder, "*.jpg"))

    # Construct the full path to the image
    image_path = image_files[0]
    
    url = 'http://localhost:5000/predict'
    try:
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            result = response.json()
            prediction = int(result['prediction'])
            #print(f"Prediction: {prediction}")
            suggested_ingredients = rag_ingredients(prediction)
            for ing in suggested_ingredients:
                product_select(ingredients=ing, max_price=100,analyze_with_llm=True)
        else:
            print(f"Error: {response.status_code}")
            print(f"Response content: {response.text}")
    except FileNotFoundError:
        print(f"Image file not found at: {image_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        
    
    
if __name__ == "__main__":
    main()
"""                
def main():
    def print_limited_results(description, results):
        print(f"\n{description}")
        for item in results[:5]:
            name = item.get("name", "Unknown")
            product_type = item.get("product_type", "Unknown")
            price = item.get("price", "Unknown")
            rating = item.get("rating")
            skin_type_booleans = {
                "combination": item.get("combination", False),
                "dry": item.get("dry", False),
                "normal": item.get("normal", False),
                "oily": item.get("oily", False),
                "sensitive": item.get("sensitive", False)
            }
            brand = item.get("brand")
            
            
            print(f"{name} | {product_type}")
        print(f"Total results: {len(results)}")
    
    # Test the find_products function with various parameters
    print_limited_results("Test 1: Search for products with 'hyaluronic acid'",
                          find_products(ingredients="hyaluronic acid"))

    print_limited_results("Test 2: Exclude products with 'alcohol'",
                          find_products(exclude_ingredients="alcohol"))

    print_limited_results("Test 3: Search for products under $50",
                          find_products(max_price=50))

    print_limited_results("Test 4: Search for combination skin products with 'vitamin C'",
                          find_products(ingredients="vitamin C", combination=True))

    print_limited_results("Test 5: Search for sensitive skin products excluding 'fragrance'",
                          find_products(sensitive=True, exclude_ingredients="fragrance"))

    print_limited_results("Test 6: Search for moisturizers for dry skin",
                          find_products(product_type="moisturizer", dry=True))
    
    database_sets = [find_products(ingredients="hyaluronic acid"), find_products(exclude_ingredients="alcohol"), find_products(max_price=50), 
                     find_products(ingredients="vitamin C", combination=True), find_products(sensitive=True, exclude_ingredients="fragrance"),
                     find_products(product_type="moisturizer", dry=True)]
    
    for dbs in database_sets:   
        pareto_results = pareto_set.pareto_front(dbs)
        print("\nPareto-optimal products:")
        for i, product in enumerate(pareto_results):
            print(f"\n{i}. {product['name']}")
            print("Scores:")
            for objective, score in product['scores'].items():
                print(f"  {objective}: {score:.2f}")

# Call the main function
if __name__ == "__main__":
    main()
"""