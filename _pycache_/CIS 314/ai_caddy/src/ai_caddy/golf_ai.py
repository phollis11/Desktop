from openai import OpenAI
import os

#API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#Function for making a call to OpenAI
#Accepts arguements of clubs in bag, hole information, and current distance to the pin
def ask_chat(bag, hole, distance):
    print(hole)
    print(distance)
    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [{"role": "developer", "content": "You are a golf caddy. Using the clubs distance, course information and distance to hole, make a club recommendation for the next shot. Keep in mind avoiding hazards, bunkers, and bad misses when selecting clubs. Response Format: Club Recommendation, then why"},
                {"role": "user", "content": f"Users clubs are: {bag}, the hole info is: {hole}, and the current distance to the middle of the green is: {distance}"}
        ]
    )
    #Return as string to ensure text formatting
    return str(completion.choices[0].message.content)

if __name__ == "__main__":
    #Example usage
    #Load a users bag with clubs and distances
    bag = {"Driver":240,
           "7i": 150,
           "PW": 125}
    #Load hole information
    hole = "Par 4, Fairway: Left 225 Bunkers, Right Trees, Long 280. Green: Left hill, Right Bunker, Long Bunker"
    #Give distance
    distance = 130

    print(ask_chat(bag, hole, distance))
    