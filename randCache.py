import random
import math

import matplotlib.pyplot as plt


page_addresses = 2000 # represented as N
num_cached_pages = 20 # reprsented as C

class WorkloadGenerator():
  """
  Write a program that generates an "80-20 Read Workload"; generate a sequence of 1000
  referenced page addresses to read with the following behavior:
  - 80% of the references are made to 20% of the pages [0, 1, … , 𝑁_1]
  - The remaining 20% of the reference are made to the remaining 80% of the pages
  [0, 1, … , 𝑁_1]
  """
  def __init__(self, number_of_pages: int, sequnce_length: int) -> None:
    self.num_pages = number_of_pages
    self.num_of_refernces = sequnce_length
    self.pages = self.create_pages()
    self.twentry_percent = self.twnety_percent_access()
    self.eighty_percent = self.eighty_percent_access()
    self.reference_list = self.create_reference_list()


  def create_pages(self) -> set:
    """
    returns an array of pages, each number is a page
    """
    return {page for page in range(self.num_pages)}
    

  def twnety_percent_access(self):
    """
    Randomly select 20% of the pages
    """
    selected_pages = set()
    while len(selected_pages) < self.num_pages * 0.2:
      random_page =  random.randint(0, self.num_pages-1)
      if random_page not in selected_pages:
        selected_pages.add(random_page)
    return selected_pages


  def eighty_percent_access(self):
    """
    Selects 80% of the pages
    """
    return self.pages - self.twentry_percent
  
  def create_reference_list(self):
    """
    80% of the references are made to 20% of the pages [0, 1, … , 𝑁_1]
    20% of the references are made to the reminder pages
    """
    refs = []
    eighty_refrences = []
    twenty_refrences = []
    refrences_from_twenty_percent = math.ceil(0.8 * self.num_of_refernces)
    print(f"itens to select from 20%: {refrences_from_twenty_percent}")
    for i in range(refrences_from_twenty_percent):
      # make 80% of the refrences from the 20% list
      page_from_twenty = random.choice(list(self.twentry_percent))
      eighty_refrences.append(page_from_twenty)

    for t in range(self.num_of_refernces - refrences_from_twenty_percent):
      # make 80% of the refrences from the 20% list
      page_from_eighty = random.choice(list(self.eighty_percent))
      twenty_refrences.append(page_from_eighty) 

    refs = eighty_refrences + twenty_refrences
    random.shuffle(refs)
    return refs

class Rand():

  def __init__(self, page_addresses: list, cache_size: int, worworkloadkflow: list) -> None:
    self.cache_size = cache_size
    self.pages = page_addresses
    self.cache = []
    self.hits = 0
    self.misses = 0
    self.workload = worworkloadkflow

  def get(self, item_from_cache):
    if item_from_cache in self.cache:
      self.hits += 1
    else:
      self.misses += 1
      self.set_item(item_from_cache)

  def set_item(self, item_to_set):
    if len(self.cache) < self.cache_size:
      self.cache.append(item_to_set)
    else:
      element_to_remove = random.choice(self.cache)
      self.cache.remove(element_to_remove)
      self.cache.append(item_to_set)

  def simulate_workload(self) -> dict:
    for item in self.workload:
      self.get(item)
    return {"misses": self.misses, "hits": self.hits, "hit_rate": (self.hits/(self.hits + self.misses))}



class Opt():
  
  def __init__(self, page_addresses: list, cache_size: int, worworkloadkflow: list) -> None:
    self.cache_size = cache_size
    self.pages = page_addresses
    self.cache = []
    self.hits = 0
    self.misses = 0
    self.workload = worworkloadkflow

  def get(self, item_from_cache, item_index_in_ref_list):
    if item_from_cache in self.cache:
      self.hits += 1
    else:
      self.misses += 1
      self.set_item(item_from_cache, item_index_in_ref_list)

  def set_item(self, item_to_set, item_index_in_ref_list):
    if len(self.cache) < self.cache_size:
      self.cache.append(item_to_set)
    else:
      element_to_remove = self.find_least_optimal_element(item_index_in_ref_list)
      self.cache.remove(element_to_remove)
      self.cache.append(item_to_set)

  def find_least_optimal_element(self, item_index_in_ref_list: int):
    """
    Replace the page that has the greatest forward distance, that will be accessed furthest in the future
    Traverse the elements in the cache and check which one is accessed the furthest
    """
    element_to_remove = ""
    max_distance = 0
    for cached_page in self.cache:
      # find the next call relative to current index.

      if not cached_page in self.workload[item_index_in_ref_list:]:
        return cached_page

      distance_to_next_access = self.workload.index(cached_page, item_index_in_ref_list) - item_index_in_ref_list
      if distance_to_next_access > max_distance:
        element_to_remove = cached_page
        max_distance = distance_to_next_access
    return element_to_remove


  def simulate_workload(self) -> dict:
    for index, item in enumerate(self.workload):
      self.get(item, index)
    return {"misses": self.misses, "hits": self.hits, "hit_rate": (self.hits/(self.hits + self.misses))}


def plot_results(rand_hit_rate, opt_hit_rate, cache_size):
  """
  Hit rate - Y
  Cache Size - X
  """
  plt.plot(cache_size, rand_hit_rate, label="Random")
  plt.plot(cache_size, opt_hit_rate, label="Optimal")
  plt.title("Cache Hit Rate")
  plt.xlabel("Cache Size")
  plt.ylabel("Hit Rate %")
  plt.legend(loc="upper left")
  plt.show()


if __name__ == "__main__":
  cache_size = [20, 50, 70, 100, 200]
  workload = WorkloadGenerator(number_of_pages=2000, sequnce_length=1000)
  rand_results = []
  opt_results = []
  for size in cache_size:
    rand_cache = Rand(page_addresses=workload.pages, cache_size=size, worworkloadkflow=workload.reference_list)
    rand_res = rand_cache.simulate_workload()
    
    print(f"RANDOM cache size: {size}, results: {rand_res}")
    
    opt_cache = Opt(page_addresses=workload.pages, cache_size=size, worworkloadkflow=workload.reference_list)
    opt_res = opt_cache.simulate_workload()
    
    print(f"OPTIMAL cache size: {size}, results: {opt_res}")

    rand_results.append(rand_res["hit_rate"])
    opt_results.append(opt_res["hit_rate"])

  plot_results(rand_results, opt_results, cache_size)