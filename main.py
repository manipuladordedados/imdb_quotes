#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Valter Nazianzeno <manipuladordedados at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import urllib.request
from bs4 import BeautifulSoup

links = ["https://www.imdb.com/title/tt0071853/quotes",
        "https://www.imdb.com/title/tt0062622/quotes",
        "https://www.imdb.com/title/tt0114709/quotes"]

def returnData(links=[]):
    jsonData = { # Empty Json/Dict model
    "title": [],
    "year": [],
    "quotes": []
    }
    movie_title = []
    movie_year = []
    final_list = []
    temp_list = []
    count = 0
    for link in links:    
        url = link
        header={"Accept-Language": "en-US"} # To IMDB display the original movie title in English.
        req = urllib.request.Request(url, headers=header)
        source = urllib.request.urlopen(req)
        soup = BeautifulSoup(source, features="lxml")

        movie_title += [[i.string for i in soup.find_all(itemprop="url")][0]]
        movie_year += [[i.string for i in soup.find(class_="nobr")][0].replace(" ","")[2:][:4]]

        temp_list += [[i.contents for i in soup.find_all(class_="sodatext")]]
        final_list += [[""]*len(temp_list[count])] # Creates a list to receive new values based on the 
                                               # number of entries of the variable temp_list.

        for vez in range(len(temp_list[count])):
            temp_list[count][vez].pop(0) # We don't need the first value.
            del temp_list[count][vez][-1] # Bugs happen if you don't delete the last value of the list.

        for vez in range(len(temp_list[count])):
            for n in range(len(temp_list[count][vez])):
                final_list[count][vez] += temp_list[count][vez][n].text.replace(":\n", ": ")

        count +=1

    for value in range(len(links)):
        jsonData["title"] += [movie_title[value]]
        jsonData["year"] += [movie_year[value]]
        jsonData["quotes"] += [final_list[value]]

    with open("data_file.json", "w", newline="\n") as write_file:
        json.dump(jsonData, write_file, indent=2)

if __name__ == "__main__":
    returnData(links) 