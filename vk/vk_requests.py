import aiohttp


class VkRequests:
    def __init__(
        self,
        group_domain: str,
        vk_token: str,
        ver: str,
        proxy: str = None,
        check_time: int = 300,
        post_offset: int = 1,
        should_parse_post_title: bool = False,
    ):
        self.check_time = check_time
        self.post_offset = post_offset
        self.should_parse_post_title = should_parse_post_title
        self.proxy = proxy

        self.last_post_date: str

        self.url = "https://api.vk.com/method/wall.get"
        self.params = {
            "access_token": vk_token,
            "v": ver,
            "domain": group_domain,
            "count": 1,
            "offset": post_offset,
        }

    async def check_last_post(self) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    self.url, params=self.params, proxy=self.proxy
                ) as response:
                    response_json = await response.json()
                    file_type = response_json["response"]["items"][-1]["type"]

                    if file_type == "post":
                        self._parse_photos(response_json)
                        return True

                    else:
                        self._parse_doc(response_json)

            except aiohttp.ClientError as e:
                print(f"Ошибка соединения: {e}")
                return None
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                return None

        return False

    async def _parse_photos(self, response_json) -> list:
        photo_urls = [
            att["photo"]["orig_photo"]["url"]
            for att in response_json["response"]["items"][-1]["attachments"]
        ]

        photo_date = response_json["response"]["items"][-1]["date"]
        return photo_urls, photo_date

    async def _parse_doc(self, response_json) -> dict:
        """
        Отдельно парсить доки

        :return:
        doc_file  - file ссылкой на документ,
        doc_text  - текст поста,
        doc_date  - дата поста,
        """

        doc_file = response_json["response"]["items"][-1]["attachments"][-1]["doc"][
            "url"
        ]
        doc_title = response_json["response"]["items"][-1]["text"]
        doc_date = response_json["response"]["items"][-1]["date"]

        return {
            "doc": doc_file,
            "doc_title": doc_title,
            "doc_date": doc_date,
        }
