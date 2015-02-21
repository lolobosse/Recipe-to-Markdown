#!/usr/bin/env python
# encoding: utf-8
__author__ = 'laurentmeyer'

from AbstractScraper import RecipeScraper
# re is for few parts which are bad structured on the website
import re


class Marmiton(RecipeScraper):

    # Multi-split from SO
    def tsplit(self, s, sep):
        stack = [s]
        for char in sep:
            pieces = []
            for substr in stack:
                pieces.extend(substr.split(char))
            stack = pieces
        return stack

    def title(self):
        title = self.find("span", {"class", "fn"})
        return title.next

    def url(self):
        return self.url

    # Have to parse the string to get the number of servings
    def num_servings(self):
        toGet = self.find("p", {"class", "m_content_recette_ingredients"}).find('span').next
        servings = re.search(re.compile('(\d+)( )(personnes)'), toGet).group(1)
        return servings

    # Added a default value of type boolean to be able to make a difference between the function called to return an int
    # (for the calculation of the total) and one called to be printed
    def prep_time(self, addMin=True):
        duration = self.find("span", {"class", "preptime"}).next.strip()
        return str(duration) + " mins" if addMin else int(duration)

    def cook_time(self, addMin=True):
        duration = self.find("span", {"class", "cooktime"}).next.strip()
        return str(duration) + " mins" if addMin else int(duration)

    def total_time(self):
        return str(int(self.prep_time(addMin=False)) + int(self.cook_time(addMin=False))) + " mins"

    # Removed the header not to have a repetition in the output
    def ingredients(self):
        textToExtract = self.tsplit(self.find("p", {"class", "m_content_recette_ingredients"}).text, ("\r", "\n"))
        for text in textToExtract:
            if u'Ingrédient' in text or text.strip == '':
                continue
            text = text.strip()
            text = text.split('-')
            for ingredient in text:
                if ingredient.strip() != '':
                    yield ingredient

    # Not properly implemented on the website; so I had to remove manually useless parts
    def directions(self):
        # Removed the parenthesis to be have things clearer
        alltext = self.tsplit(re.sub(r'\([^)]*\)', '', self.find("div", {"class", "m_content_recette_todo"}).text),
                              ("\r", "\n", ".", "!"))
        for instruction in alltext:
            if u'Préparation' in instruction:
                continue
            if u'Remarque' in instruction:
                break
            if instruction.strip() != '':
                instruction = instruction.strip() + ".".replace("\d+\/ ", "")
                instruction = re.sub(r'\d\/ ', '', instruction)
                yield instruction

    def note(self):
        return self.findAll("img", {"class": "on"}).count()