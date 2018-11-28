#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
#rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename, encoding='utf8') as f:
            initdesc = f.readline().split()
            self._n = int(initdesc[0])
            self._nlinks = int(initdesc[1])
            
            self._titles = []
            self._sizes = array.array('L', [0]*_n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*_n)
            self._offset = array.array('L', [0]*(_n+1))

            for i in range(self._n):
                title = f.readline()
                titledesc = f.readline().split()

                self._titles.append(title.strip())

                self._sizes[i]    = int(titledesc[0])
                self._redirect[i] = int(titledesc[1])
                self._offset[i+1] = self._offset[i] + int(titledesc[2])
                for j in range(self._offset[i], self._offset[i+1]):
                    self._links.append(int(f.readline()))

        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return self._offset[_id + 1] - self._offset[_id]

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id + 1]]

    def get_id(self, title):
        return self._titles.index(title)

    def get_number_of_pages(self):
        return self._n

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._pagesize[_id]


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл

def get_array_stats(wg, arr):
    stats = dict()

    stats['avg']      = statistics.mean(arr)
    stats['maxval']   = max(arr)
    stats['maxcount'] = arr.count(stats['maxval'])
    maxindex          = arr.index(stats['maxval'])
    stats['maxtitle'] = wg.get_title(maxindex)
    
    stats['minval']   = min(arr)
    stats['mincount'] = arr.count(stats['minval'])
    minindex          = arr.index(stats['minval'])
    stats['mintitle'] = wg.get_title(minindex)

    return stats

def get_links_from_stats(wg):
    linksfrom = array.array('L', [wg.get_number_of_links_from(i) for i in range(wg.get_number_of_pages())])
    return get_array_stats(wg, linksfrom)

def get_links_to_stats(wg):
    linksto = array.array('L', [0]*wg.get_number_of_pages())
    for i in range(wg.get_number_of_pages()):
        if not wg.is_redirect(i):
            links = wg.get_links_from(i)
            for link in links:
                linksto[link] += 1

    return get_array_stats(wg, linksto)

def get_redirects_to_stats(wg):
    redirectsto = array.array('L', [0]*wg.get_number_of_pages())
    for i in range(wg.get_number_of_pages()):
        if wg.is_redirect(i):
            links = wg.get_links_from(i)
            for link in links:
                redirectsto[link] += 1

    return get_array_stats(wg, redirectsto)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('Файл с графом не найден')
        sys.exit(-1)

    wg = WikiGraph()
    wg.load_from_file(sys.argv[1])

    linksfrom   = get_links_from_stats(wg)
    linksto     = get_links_to_stats(wg)
    redirectsto = get_redirects_to_stats(wg)
    
    print("Количество статей с максимальным количеством внешних ссылок: ", linksfrom['maxcount'])
    print("Статья с наибольшим количеством внешних ссылок: ", linksfrom['maxtitle'])
    print("Среднее количество внешних ссылок на статью: ", linksto['avg'])
    print("Минимальное количество перенаправлений на статью: ", redirectsto['minval'])
    print("Количество статей с минимальным количеством внешних перенаправлений: ", redirectsto['mincount'])
    print("Максимальное количество перенаправлений на статью: ", redirectsto['maxval'])
    print("Количество статей с максимальным количеством внешних перенаправлений: ", redirectsto['maxcount'])
    print("Статья с наибольшим количеством внешних перенаправлений: ", redirectsto['maxtitle'])
    print("Среднее количество внешних перенаправлений на статью: ", redirectsto['avg'])
