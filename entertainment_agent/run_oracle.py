from core.brain import EntertainmentBrain

import sys

oracle = EntertainmentBrain()

print("Entertainment Oracle is ready!")
print("Share something you loved (book, movie, show, podcast, or song):")
user_input = sys.stdin.readline().strip()

if user_input:
    result = oracle.get_recommendation(user_input)
    print(f"\nAnalysis: {result.get('analysis')}")
    print(f"Wildcard Recommendation: {result.get('wildcard_recommendation')}")