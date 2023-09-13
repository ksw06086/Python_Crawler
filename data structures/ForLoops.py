
# * URL Formatting
websites = (
    "https://google.com",
    "https://airbnb.com",
    "https://twitter.com",
    "https://facebook.com"
)

for website in websites:
    if not website.startswith("https://"):
        website = f"https://{website}"
    print(website)