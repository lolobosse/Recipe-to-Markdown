from AbstractScraper import RecipeScraper


class TwoPeas(RecipeScraper):

    def title(self):
        return self.soup.title.string.encode("ascii", 'ignore').strip().split(" - ")[0]

    def url(self):
        return self.url

    def num_servings(self):
        return self.soup.find("span", {"class": "yield"}).get_text()

    def prep_time(self):
        return self.soup.find("span", {"class": "preptime"}).get_text()

    def cook_time(self):
        return self.soup.find("span", {"class": "cooktime"}).get_text()

    def total_time(self):
        return self.soup.find("span", {"class": "duration"}).get_text()

    def ingredients(self):
        for s in self.soup.findAll("div", {"class": "ingredient"}):
            yield s.get_text().encode("ascii", "ignore").strip()

    def directions(self):
        for s in self.soup.findAll("div", {"class": "instructions"}):
            yield s.get_text().encode("ascii", "ignore").strip()

    def note(self):
        return "none"
