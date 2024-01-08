import time
import json

# ANSI escape codes for text color
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
END_COLOR = "\033[0m"

# Load words from JSON file into dict
def load_words_from_json(filename):
    with open(filename) as f:
        return json.load(f)

# Load categories data from an external file
categories_data_filename = 'words.json'
words_dict = load_words_from_json(categories_data_filename)

# Update leaderboard 
def update_leaderboard(username, words_typed, time_taken, wpm):
    leaderboard_file = 'leaderboard.json'
    
    try:
        with open(leaderboard_file, 'r') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = {}

    leaderboard[username] = {
        f"Words Typed " : words_typed,
        "Time Taken": f"{time_taken:.2f} seconds",
        "Words Per Minute": f"{wpm} WPM "
    }

    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f, indent=4)  

# Display leaderboard
def show_leaderboard():
    leaderboard_file = 'leaderboard.json'
    
    try:
        with open(leaderboard_file, 'r') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = {}
    
    print("== Leaderboard ==")
    
    if not leaderboard:
        print("Leaderboard is empty.")
    else:
        for user, metrics in leaderboard.items():
            print(f"{user}: {metrics}")

# Get user input    
def get_user_input():
  try:
    username = input(f"{YELLOW}Enter your Username: {END_COLOR} ").capitalize()
    print(f"<======== Welcome {username} =========>")
    print("1. Start Typing Test")
    print("2. Show Leaderboard")
    print("3. Quit")
    
    choice = input(f"{CYAN}Choice: {END_COLOR}")
    return username, choice
  except Exception as e: 
        print(f"{RED}Something went wrong{END_COLOR}")
  except KeyboardInterrupt:
        print("Exiting...")
        
def display_category_data(category):
    print(f"{PURPLE}{words_dict[category]['paragraph']}{END_COLOR}")

def main():
    try:
        print("<=== 🥷 Welcome to Typing Test 🥷 ===>")
        username, choice = get_user_input()
        print(f"Selected choice: {choice}")
        
        if choice == '1':
            # Choose a category
            print(f"{CYAN}Your favorite Category: {END_COLOR} ")
            print(", ".join(words_dict.keys()))

            selected_category = input(f"{CYAN}\nEnter the Category: {END_COLOR} ")

            # Check if the selected category exists
            if selected_category in words_dict:
                # Display category data
                display_category_data(selected_category)

                # Start typing test with words from the selected category
                words = words_dict[selected_category]['paragraph'].split()

                print(f"\nType the following paragraph related to '{selected_category}':")

                start_time = time.time()

                user_input = input("Start typing: ")

                end_time = time.time()

                time_taken = end_time - start_time
                words_typed = len(user_input.split())
                wpm = int((words_typed / time_taken) * 60) if time_taken > 0 else 0

                # Check for errors in the typed text
                errors = sum(c1 != c2 for c1, c2 in zip(user_input, words_dict[selected_category]['paragraph']))

                print(f"{CYAN}\n{username.capitalize()} Your Stats: {END_COLOR}")
                print(f"Words Typed: {words_typed}\nTime Taken: {time_taken:.2f} seconds\nWords Per Minute: {wpm} WPM")
                print(f"Errors: {errors}")

                update_leaderboard(username, words_typed, time_taken, wpm)

                # Ask if the user wants to exit or continue
                exit_choice = input("\nDo you want to exit? (y/n): ").lower()
                if exit_choice == 'y':
                    print("Goodbye!")
                    print("Exiting...")
                    exit()
            else:
                print(f"{RED}Invalid category: {selected_category}. Please choose a valid category.{END_COLOR}")

        elif choice == '2':
            show_leaderboard()

        elif choice == '3':
            print("Goodbye!")
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{END_COLOR}")
    except KeyboardInterrupt:
        print("Exiting...")
        exit()

while True:
    main()