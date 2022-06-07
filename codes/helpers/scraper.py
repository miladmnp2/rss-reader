import backoff
import httpx
import xmltodict
import requests
from helpers.publishers import PublisherHelper
from helpers.feeds import FeedHelper


class ScraperHelper:
    @staticmethod
    async def scrap_publishers_periodically_test():
        publishers = await PublisherHelper.get_all_publishers()
        await ScraperHelper.scrap_pubs(
            [{
                "id": publisher.id,
                "link": publisher.link
            } for publisher in publishers])

    @staticmethod
    async def scrap_pubs(publishers):
        for publisher in publishers[1:]:
            items = await ScraperHelper.get_single_feed(publisher["link"])
            for item in items:
                feed_data = {
                    "title": item["title"] if "title" in item else "",
                    "link": item["link"] if "link" in item else "",
                    "description": item["description"] if "description" in item else "",
                    "publisher_id": publisher["id"]
                }

                await FeedHelper.create_feed(feed_data)

        print("Finishing periodic function")

    @staticmethod
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError), max_time=5)
    async def get_single_feed(url):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            r = await client.get(url, )
            tree = xmltodict.parse(r.content.decode("utf-8"))

            return tree["rss"]["channel"]["item"]
