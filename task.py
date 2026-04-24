import requests
import time


def performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        wrapper.last_exec_time = end_time - start_time
        return result

    return wrapper


@performance
def fetching_posts():
    proxy_url = [
        [
            "https://api.codetabs.com/v1/proxy?quest=https://jsonplaceholder.typicode.com/posts",
            "codetabs",
        ],
        ["https://corsproxy.io/?https://jsonplaceholder.typicode.com/posts", "cors"],
        ["http://jsonplaceholder.typicode.com/posts", "direct"],
    ]

    print("Using Some proxys to fetch posts")

    for url in proxy_url:
        try:
            print(f"\nTrying URL: {url[0]}")
            response = requests.get(url[0], timeout=25)
            response.raise_for_status()
            if response.status_code == 200:
                posts = response.json()
                first_10_posts = posts[:10]
                print(
                    f"\nSuccessfully fetched {len(first_10_posts)} posts through {url[1]} proxy"
                )
                return first_10_posts

        except Exception as e:
            print(f"Proxy Failed: {e}")
    return None


def get_post_titles_bodies(data):
    for post in data:
        yield post["title"], post["body"]


