from cachetools import cached, TTLCache
from models import Quote, Author
from redis import StrictRedis

redis_host = 'localhost'
redis_port = 6379

redis_client = StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

cache = TTLCache(maxsize=100, ttl=300)


@cached(cache)
def find_by_author(author: str):
    print(f'Find by {author}')
    authors = Author.objects(fullname__iregex=author)
    result = {}
    if author:
        for a in authors:
            quotes = Quote.objects(author=a)
            result[a.fullname] = ([q.quote for q in quotes])
        return result
    else:
        return []


@cached(cache)
def find_by_tag(tag: str):
    print(f'Find by {tag}')
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cached(cache)
def find_by_tags(tag: str):
    tags = tag.split(",")
    print(f'Find by {tags}')
    result = []
    unique_quotes = set()  # множина для унікальних цитат
    for tag in tags:
        quotes = Quote.objects(tags__iregex=tag)
        unique_quotes.update(quote.quote for quote in quotes)
    result.append(list(unique_quotes))
    return result


def search_command(command, arg):
    if command == 'name':
        return find_by_author(arg)
    elif command == 'tag':
        return find_by_tag(arg)
    elif command == 'tags':
        return find_by_tags(arg)
    else:
        return None


def main():
    while True:
        user_input = input('Enter the command: ')
        if user_input == 'exit':
            break
        else:
            try:
                command, arg = user_input.split(':')
                if command in ['name', 'tag', 'tags']:
                    result = search_command(command, arg)
                    print(result)
                else:
                    print('Incorrect command')
            except ValueError:
                print('Invalid input format. Use command format: command:argument')
            except Exception as err:
                print(f'Error: {err}')


if __name__ == '__main__':
    main()
