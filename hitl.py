def human_fallback(query):
    print("\n Escalating to human support...")
    print("User Query:", query)
    answer = input(" Enter human response: ")
    return answer
