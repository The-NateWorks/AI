import nautical
while True:
    user = input("You: ")
    response = nautical.respond(user)
    print("Nautical: " + response)