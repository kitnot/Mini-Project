import argparse
from zxcvbn import zxcvbn

# 1. Password Strength Checker
def analyze_password(password):
    result = zxcvbn(password)
    print("\n--- Password Analysis ---")
    print(f"Password: {password}")
    print(f"Strength Score (0-4): {result['score']}")
    print(f"Crack Time: {result['crack_times_display']['online_no_throttling_10_per_second']}")
    print(f"Warning: {result['feedback']['warning'] or 'None'}")
    print("Suggestions:")
    for suggestion in result['feedback']['suggestions']:
        print(f"- {suggestion}")

# 2. Wordlist Generator
def generate_wordlist(keywords, years):
    wordlist = []
    for keyword in keywords:
        wordlist.append(keyword)  # Base word
        wordlist.append(keyword + "123")  # Common suffix
        for year in years:
            wordlist.append(keyword + str(year))  # e.g., "alice2023"
    return wordlist

# 3. Save Wordlist to File
def save_wordlist(wordlist, filename="custom_wordlist.txt"):
    with open(filename, "w") as f:
        for word in wordlist:
            f.write(word + "\n")
    print(f"\nWordlist saved to: {filename}")

# 4. CLI Interface
def main():
    parser = argparse.ArgumentParser(description="Password Analyzer & Wordlist Generator")
    parser.add_argument("--analyze", help="Check password strength")
    parser.add_argument("--generate", help="Generate wordlist from keywords (comma-separated)")
    parser.add_argument("--years", help="Years to append (comma-separated)")
    args = parser.parse_args()

    if args.analyze:
        analyze_password(args.analyze)
    elif args.generate:
        keywords = args.generate.split(",")
        years = list(map(int, args.years.split(","))) if args.years else []
        save_wordlist(generate_wordlist(keywords, years))
    else:
        print("No action selected. Use --analyze or --generate.")

if __name__ == "__main__":
    main()