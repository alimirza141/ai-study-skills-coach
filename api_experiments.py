import requests


def inspect_api(name, url):
    print(f"\n{name}")
    print("-" * len(name))

    try:
        response = requests.get(url, timeout=10)

        print(f"Status code: {response.status_code}")

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            print(f"Top-level keys: {list(data.keys())[:10]}")
        elif isinstance(data, list):
            print(f"Number of returned items: {len(data)}")
        else:
            print(f"Returned type: {type(data).__name__}")

    except requests.RequestException as error:
        print(f"Request failed: {error}")

    except ValueError:
        print("The response is not valid JSON.")


def main():
    inspect_api(
        "GitHub API",
        "https://api.github.com",
    )

    inspect_api(
        "Public APIs directory",
        "https://api.publicapis.org/entries",
    )


if __name__ == "__main__":
    main()