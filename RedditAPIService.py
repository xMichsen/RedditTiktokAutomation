import requests

class RedditAPIService:
    def __init__(self, thread_url):
        if not thread_url.endswith('.json'):
            self.thread_url = thread_url + '.json'
        else:
            self.thread_url = thread_url
        self.thread_data = None

    def fetch_thread(self):
        headers = {'User-agent': 'RedditThreadFetcherBot/1.0'}
        response = requests.get(self.thread_url, headers=headers)
        if response.status_code == 200:
            self.thread_data = response.json()
        else:
            raise Exception(f"Failed to fetch thread: {response.status_code}")

    def get_thread_info(self):
        if self.thread_data is None:
            raise Exception("Thread data has not been fetched. Call fetch_thread() first.")
        # Thread data is in the first element of the list
        thread = self.thread_data[0]['data']['children'][0]['data']
        threadText = thread.get('selftext')
        title = thread.get('title')
        author = thread.get('author')
        upvotes = thread.get('ups')
        downvotes = thread.get('downs')
        num_comments = thread.get('num_comments')
        subreddit = thread.get('subreddit')
        return {
            'title': title,
            'text': threadText,
            'subreddit': subreddit,
            'author': author,
            'upvotes': upvotes,
            'downvotes': downvotes,
            'num_comments': num_comments
        }

    def get_top_comments(self, n, max_words_per_comment=30):
        if self.thread_data is None:
            raise Exception("Thread data has not been fetched. Call fetch_thread() first.")
        # Comments are in the second element of the list
        comments = self.thread_data[1]['data']['children']
        top_comments = []
        count = 0
        for comment in comments:
            if comment['kind'] != 'more' and count < n:
                data = comment['data']
                authorLowerCase = data.get('author').lower()
                body = data.get('body')

                # Filter out comments that are too long
                word_count = len(body.split())
                if word_count > max_words_per_comment:
                    continue  # Skip this comment

                # Skip comments from users containing "moderator"
                if "moderator" in authorLowerCase:
                    continue

                if "https://" in body or "http://" in body:
                    continue

                author = data.get('author')
                upvotes = data.get('ups')
                downvotes = data.get('downs')
                top_comments.append({
                    'author': author,
                    'body': body,
                    'upvotes': upvotes,
                    'downvotes': downvotes
                })
                count += 1
            if count >= n:
                break
        return top_comments
