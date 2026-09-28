import sys

def print_state(city):
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }  

    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    found = False

    for ct_key, ct_value in capital_cities.items():
        if city == ct_value:
            for st_key, st_value in states.items():
                if ct_key == st_value:
                    print(st_key)
                    found = True
    
    if not found:
        print("Unknow capital city")



if __name__ == "__main__":
    if len(sys.argv) == 2:
        print_state(sys.argv[1])
