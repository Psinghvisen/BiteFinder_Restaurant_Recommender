import json

def save_user_feedback(feedback):
    with open('data/user_feedback.csv', 'a') as file:
        file.write(feedback + "\n")

def load_user_preferences():
    with open('data/user_preferences.json', 'r') as file:
        return json.load(file)

if __name__ == '__main__':
    save_user_feedback("Restaurant X, 5 stars, Great!")
    print(load_user_preferences())
