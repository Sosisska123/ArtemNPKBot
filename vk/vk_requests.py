import logging
import aiohttp

from .schemas.vk_group import VkGroupSchema


logger = logging.getLogger(__name__)


class VkRequests:
    def __init__(
        self,
        group_schema: VkGroupSchema,
        api_vk_token: str,
        api_ver: str,
        proxy: str = None,
    ):
        self.proxy = proxy

        self.group = group_schema

        self.url = "https://api.vk.com/method/wall.get"
        self.params = {
            "access_token": api_vk_token,
            "v": api_ver,
            "count": 1,
            "domain": group_schema.domain,
            "offset": group_schema.start_post_offset,
        }

        self.last_post_date: str = ""

    async def check_last_post(self) -> dict[str, VkGroupSchema]:
        result = {}

        async with aiohttp.ClientSession() as session:
            try:
                logger.info("- - - - - - - - - - - - - - - - - - - - - - -")
                logger.info("STARTING FETCH POSTS FROM | %s", self.group.domain)

                async with session.get(
                    self.url, params=self.params, proxy=self.proxy
                ) as response:
                    response_json = await response.json()

                    file_type = response_json["response"]["items"][-1]["attachments"][
                        0
                    ]["type"]
                    file_date = response_json["response"]["items"][0]["date"]

                    if self.last_post_date == file_date:
                        # File Is Already Parsed
                        return result

                    elif self.last_post_date == "":
                        # now its the latest post
                        self.last_post_date = file_date
                        return result

                    if (
                        file_type == "photo"
                        and file_type == self.group.return_file_type
                    ):
                        logger.info("PHOTO FOUND; PARSING...")

                        photo_urls = self._parse_photos(response_json)

                        self.last_post_date = file_date

                        result[self.group.group_name_shortcut] = self.group.model_copy(
                            update={
                                "files_url": photo_urls,
                                "photo_date": file_date,
                            }
                        )

                    elif (
                        file_type == "doc" and file_type == self.group.return_file_type
                    ):
                        logger.info("DOCUMENT FOUND; PARSING...")

                        doc_url, doc_title = self._parse_doc(response_json)

                        self.last_post_date = file_date

                        result[self.group.group_name_shortcut] = self.group.model_copy(
                            update={
                                "files_url": doc_url,
                                "doc_title": doc_title,
                                "doc_date": file_date,
                            }
                        )

                    # else:
                    #     logger.info("NO POSTS FOUND in GROUP %s", group)
            except aiohttp.ClientError as e:
                logger.error("Ошибка соединения aiohttp.ClientError: %s", e)
                return None
            except Exception as e:
                logger.error("Неожаданная ошибка: %s", e)
                return None

        return result

    def _parse_photos(self, response_json) -> list[str]:
        photo_urls = [
            att["photo"]["orig_photo"]["url"]
            for att in response_json["response"]["items"][-1]["attachments"]
        ]

        return photo_urls

    def _parse_doc(self, response_json) -> list[str]:
        doc_file = response_json["response"]["items"][-1]["attachments"][-1]["doc"][
            "url"
        ]
        doc_title = response_json["response"]["items"][-1]["text"]

        return doc_file, doc_title
