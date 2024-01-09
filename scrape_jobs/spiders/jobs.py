import scrapy
from scrapy.http import Response
from ..technologies import TECHNOLOGIES


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def parse(self, response: Response, **kwargs):
        for job_href in response.css(
                "div.job-list-item__title > div > a::attr(href)"
        ).getall():
            yield scrapy.Request(
                url=response.urljoin(job_href),
                callback=self._parse_single_job
            )

        next_page = response.css("ul.pagination > li:last-child > a::attr(href)").get()

        if next_page != "#":
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def _parse_single_job(self, response: Response) -> dict:
        english_level, experience = self._parse_additional_info(response)
        published, views, application = self._parse_view_applications(response)
        requirements = self._collect_job_requirements(response)

        return {
            "title": response.css(
                "div.detail--title-wrapper > div > div.col > h1::text"
            ).get().strip(r"\n").strip(),
            "description": response.css(
                "div.job-post-page > div:nth-child(2) > div.col-sm-8.row-mobile-order-2 > div:nth-child(1)::text"
            ).get().strip(r"\n").strip() or "Not specified",
            "location": (" ".join(response.css(
                "div.job-additional-info > ul > li > div > span.location-text::text"
            ).getall()).replace("\n", "").replace(",", "")).split(),
            "requirements": requirements,
            "published": published,
            "views": views,
            "replies": application,
            "english_level": english_level,
            "years_of_experience": experience,
        }

    def _parse_additional_info(self, response: Response) -> tuple:
        english_level, experience = None, None

        additional_info = [item.replace(r"\n", "").strip() for item in response.css(
            "div.job-post-page > div > div > div > ul > li > div::text"
        ).getall() if item.replace(r"\n", "").strip() is not None]

        for item in additional_info:
            if "Англійська:" in item:
                english_level = item.split()[-1]
            elif "досвід" in item:
                experience = int("".join(char for char in item if char.isdigit()))

        return english_level, experience

    def _parse_view_applications(self, response: Response) -> tuple:
        published, views, application = None, None, None

        data = [item.replace(r"\n", "").strip() for item in response.css(
            "div.job-post-page > div > div.row-mobile-order-2 > div.text-small > p::text"
        ).getall() if item.replace(r"\n", "").strip() is not None]

        for item in data:
            if "Вакансія опублікована" in item or "Job posted" in item:
                published = item.split("\n")[-1].strip()
            elif "перегляд" in item or "views" in item:
                views = int(item.split()[0])
            elif "відгук" in item or "application" in item:
                application = int(item.split()[0])

        return published, views, application

    def _collect_job_requirements(self, response: Response) -> set[str]:
        data = set(" ".join(response.css(
            "div.job-post-page > div > div.row-mobile-order-2 > div.mb-4::text"
        ).getall()).replace("\n", "").upper().split())

        return data.intersection(TECHNOLOGIES)
