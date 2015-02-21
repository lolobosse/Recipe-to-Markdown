#!/usr/bin/env python
# encoding: utf-8
__author__ = 'laurentmeyer'

from AbstractScraper import RecipeScraper
import re
class Marmiton(RecipeScraper):

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

    def num_servings(self):
        pattern = re.compile("(\d.) (personnes)")
        toGet = self.find("p", {"class", "m_content_recette_ingredients"}).find('span').next
        servings = re.search(re.compile('(\d+)( )(personnes)'), toGet).group(1)
        return servings

    def prep_time(self, addMin = True):
        duration = self.find("span", {"class", "preptime"}).next.strip()
        return str(duration)+" mins" if addMin else int(duration)

    def cook_time(self, addMin = True):
        duration = self.find("span", {"class", "cooktime"}).next.strip()
        return str(duration)+" mins" if addMin else int(duration)

    def total_time(self):
        return str(int(self.prep_time(addMin=False))+int(self.cook_time(addMin=False)))+" mins"

    def ingredients(self):
        textToExtract = self.find("p", {"class", "m_content_recette_ingredients"}).text
        textToExtract = self.tsplit(textToExtract, ("\r","\n"))
        for text in textToExtract:
            if u'Ingrédient'in text or text.strip=='':
                continue
            text = text.strip()
            text= text.split('-')
            for ingredient in text:
                if ingredient.strip()!='':
                    yield ingredient

    def directions(self):
        alltext = self.find("div", {"class", "m_content_recette_todo"}).text
        alltext = re.sub(r'\([^)]*\)', '', alltext)
        alltext = self.tsplit(alltext, ("\r","\n",".","!"))
        for instruction in alltext:
            if u'Préparation' in instruction:
                continue
            if u'Remarque' in instruction:
                break
            if instruction.strip()!='':
                instruction = instruction.strip()+".".replace("\d+\/ ","")
                instruction = re.sub(r'\d\/ ','', instruction)
                yield instruction

    def note(self):
        return self.findAll("img", {"class":"on"}).count()