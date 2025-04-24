import socket

HOST = "192.168.176.214"
PORT = 7777

def display_difficulty_menu():
    print("\nChoose Your Challenge Level:")
    levels = {
        1: "Easy (1–10)",
        2: "Medium (1–50)",
        3: "Hard (1–100)"
    }
    for key, value in levels.items():
        print(f"{key}) {value}")
    return levels

def get_user_choice():
    levels = display_difficulty_menu()
    while True:
        try:
            selection = int(input("Enter your choice (1–3): "))
            if selection in levels:
                return selection
            else:
                print("Please choose a valid option from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def determine_range(level):
    ranges = {
        1: (1, 10),
        2: (1, 50),
        3: (1, 100)
    }
    return ranges[level]

def auto_guess_game():
    with socket.socket() as sock:
        print("Connecting to the server...")
        sock.connect((HOST, PORT))
        
        welcome_msg = sock.recv(1024).decode().strip()
        print(f"\nServer says: {welcome_msg}")

        difficulty = get_user_choice()
        sock.sendall(f"{difficulty}\n".encode())

        low, high = determine_range(difficulty)

        intro = sock.recv(1024).decode().strip()
        print(f"\n{intro}")

        print("\nStarting the automated guessing...")
        attempt_count = 0

        while low <= high:
            guess = (low + high) // 2
            attempt_count += 1
            print(f"Attempt #{attempt_count}: Trying {guess}")
            sock.sendall(f"{guess}\n".encode())

            server_reply = sock.recv(1024).decode().strip()
            print(f"Feedback: {server_reply}")

            if "CORRECT" in server_reply:
                print(f"\nSuccess! The correct number is {guess}")
                print(f"Total Attempts: {attempt_count}")
                break
            elif "Higher" in server_reply:
                low = guess + 1
            elif "Lower" in server_reply:
                high = guess - 1

if __name__ == "__main__":
    print("=== Binary Bot: Smart Number Guesser ===")
    auto_guess_game()
