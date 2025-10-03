from urllib.parse import urlencode


class Player:
    __base_url = "https://www.vidking.net/embed"
    __movie = __base_url + "/movie/{tmdb_id}"
    __tv = __base_url + "/tv/{tmdb_id}/{ses}/{ep}"

    def __init__(self) -> None:
        self.color = "red"
        self.auto_play = False
        self.next_ep_button = False
        self.ep_selector_button = False

    def get_query(self) -> str:
        mapping: dict[str, str | bool] = {
            "color": self.color,
            "autoPlay": str(self.auto_play).lower(),
            "nextEpisode": str(self.next_ep_button).lower(),
            "episodeSelector": str(self.ep_selector_button).lower(),
        }
        return "?" + urlencode(mapping)

    def embed_url(
        self,
        tmdb_id: int,
        *,
        ses: int | None = None,
        ep: int | None = None,
    ) -> str:
        if ses:
            return (
                self.__tv.format(tmdb_id=tmdb_id, ses=ses, ep=ep if ep else 1)
                + self.get_query()
            )
        return self.__movie.format(tmdb_id=tmdb_id) + self.get_query()


if __name__ == "__main__":
    p = Player()
    print(p.embed_url(123))
    print(p.embed_url(123, ses=1, ep=2))
