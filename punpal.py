import requests
import pyttsx3
import time

engine = pyttsx3.init()
ratings = []

def fetch_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["type"] == "single":
            return data["joke"]
        elif data["type"] == "twopart":
            return f'{data["setup"]}\n{data["delivery"]}'
    return "Sorry, I couldn't fetch a joke at the moment."

def tell_joke(joke):
    print("\nJoke:")
    print(joke)
    engine.say(joke)
    engine.runAndWait()

def rate_joke(joke):
    rating = input("\nRate this joke (1-5): ").strip()
    if rating.isdigit() and 1 <= int(rating) <= 5:
        ratings.append(int(rating))
        print("Thanks for rating the joke!")
        update_leaderboard(joke, int(rating))
    else:
        print("Invalid rating. Skipping rating for this joke.")

def update_leaderboard(joke, rating):
    with open("joke_leaderboard.txt", "a") as file:
        file.write(f"Joke: {joke}\nRating: {rating}\n\n")

def display_leaderboard():
    if ratings:
        average_rating = sum(ratings) / len(ratings)
        print("\n--- Leaderboard ---")
        print(f"Total Jokes Rated: {len(ratings)}")
        print(f"Average Rating: {average_rating:.2f}")
        print("-------------------")
    else:
        print("\nNo ratings yet. Be the first to rate a joke!")

def suspense():
    print("\nGetting ready to tell the joke", end="", flush=True)
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")

def main():
    print("Welcome to PunPal")
    while True:
        # Fetch a joke
        suspense()
        joke = fetch_joke()
        
        tell_joke(joke)
        
        rate_joke(joke)

        display_leaderboard()
        
        another = input("\nDo you want to hear another joke? (yes/no): ").strip().lower()
        if another != "yes":
            print("Thanks for using PunPal")
            break

if __name__ == "__main__":
    main()
