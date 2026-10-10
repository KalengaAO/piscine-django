import antigravity 
import sys

def geohashing():
    if len(sys.argv) == 4:
        try:
            latitude = float(sys.argv[1])
            longitude = float(sys.argv[2])
            date = sys.argv[3];
        except ValueError as e:
            print(f"Error occurred: {e}")
            return 
        antigravity.geohash(latitude, longitude, date.encode())
    else:
        print(f"User: python {sys.argv[0]} latitude longitude date!")

if __name__ == "__main__":
    geohashing()