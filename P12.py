from abc import ABCMeta, abstractmethod, abstractproperty
from collections import namedtuple
import time, random, copy, logging

log = logging.basicConfig(filename='p12_log.txt', filemode='w', level=logging.INFO)

def freshness_func(age, lifetime):
    lifetime = lifetime
    return round((1 - age / lifetime) * 100, 2) if age < lifetime else 0

def price_func(base_cost, length_of_stem, min_length_of_stem, max_length_of_stem):
    average_length_of_stem = (min_length_of_stem + max_length_of_stem) / 2
    return round(base_cost * length_of_stem / average_length_of_stem, 2)


class Colors(object):

    RED = 'Red'
    ORANGE = 'Orange'
    YELLOW = 'Yellow'
    GREEN = 'Green'
    BLUE = 'Blue'
    DARK_BLUE = 'Dark_blue'
    PURPLE = 'Purple'
    WHITE = 'White'

class Accessories(object):

    Acces = namedtuple('Acces', ['name', 'price'])

    RHINESTONES = Acces('rhinestones', 0.5)
    RIBBON = Acces('Ribbon', 0.2)
    BUTTERFLY = Acces('butterfly', 0.3)
    BASKET = Acces('basket', 0.3)

    @classmethod
    def list_of_accessories(self):
        return [value for key, value in Accessories.__dict__.items() if isinstance(value, tuple)]

    @classmethod
    def random_accessor(self):
        return random.choice([value for key, value in Accessories.__dict__.items() if isinstance(value, tuple)])

class Flower(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        self.__extra_age = random.randint(0, 24)  # hours
        time.clock()

    @property
    def age_of_the_flower(self):
        return round(time.clock() / 3600 + self.__extra_age, 2)

    @abstractmethod
    def freshness(self):  # percents
        pass

    @abstractmethod
    def price(self):
        pass


class Rose(Flower):

    def __init__(self):
        super(Rose, self).__init__()

        self.name = 'Rose'
        self.__min_lifetime = 72  # hours
        self.__max_lifetime = 168 # hours
        self.lifetime = random.randint(self.__min_lifetime, self.__max_lifetime)

        self.__posible_colors = [Colors.RED, Colors.DARK_BLUE, Colors.WHITE]
        self.color = random.choice(self.__posible_colors)

        self.__min_length_of_stem = 30  # centimeters
        self.__max_length_of_stem = 70  # centimeters
        self.length_of_stem = random.randint(self.__min_length_of_stem, self.__max_length_of_stem)

        self.__base_cost = 2.0  # dollars

    @property
    def freshness(self):  # percents
        return freshness_func(self.age_of_the_flower, self.lifetime)

    @property
    def price(self):  # dollars
        return price_func(self.__base_cost, self.length_of_stem, self.__min_length_of_stem, self.__max_length_of_stem)


class Tulip(Flower):

    def __init__(self):
        super(Tulip, self).__init__()

        self.name = 'Tulip'
        self.__min_lifetime = 48  # hours
        self.__max_lifetime = 120 # hours
        self.lifetime = random.randint(self.__min_lifetime, self.__max_lifetime)

        self.__posible_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.BLUE]
        self.color = random.choice(self.__posible_colors)

        self.__min_length_of_stem = 30  # centimeters
        self.__max_length_of_stem = 60  # centimeters
        self.length_of_stem = random.randint(self.__min_length_of_stem, self.__max_length_of_stem)

        self.__base_cost = 1.0  # dollars

    @property
    def freshness(self):  # percents
        return freshness_func(self.age_of_the_flower, self.lifetime)

    @property
    def price(self):  # dollars
        return price_func(self.__base_cost, self.length_of_stem, self.__min_length_of_stem, self.__max_length_of_stem)


class Chamomile(Flower):

    def __init__(self):
        super(Chamomile, self).__init__()

        self.name = 'Chamomile'
        self.__min_lifetime = 24  # hours
        self.__max_lifetime = 72 # hours
        self.lifetime = random.randint(self.__min_lifetime, self.__max_lifetime)

        self.__posible_colors = [Colors.WHITE]
        self.color = random.choice(self.__posible_colors)

        self.__min_length_of_stem = 10  # centimeters
        self.__max_length_of_stem = 20  # centimeters
        self.length_of_stem = random.randint(self.__min_length_of_stem, self.__max_length_of_stem)

        self.__base_cost = 0.5  # dollars

    @property
    def freshness(self):  # percents
        return freshness_func(self.age_of_the_flower, self.lifetime)

    @property
    def price(self):  # dollars
        return price_func(self.__base_cost, self.length_of_stem, self.__min_length_of_stem, self.__max_length_of_stem)

class Bouquet(object):

    def __init__(self):
        self.flowers_in_a_bouquet = []
        self.bought_accessories = []

    def __repr__(self):
        if not self.flowers_in_a_bouquet:
#            return 'you do not have a bouquet'
#        return 'flowers: {}\n\naccessories: {}'.format(['{} {}, freshness = {}, length_of_stem = {}, price = {};'.format(i.color, i.name, i.freshness, i.length_of_stem, i.price) for i in self.flowers_in_a_bouquet], [i.name for i in self.bought_accessories])

            return 'you do not have any bouquet'
        for_return = 'Flowers:\n'
        for flower in self.flowers_in_a_bouquet:
            for_return += '{} {}: freshness = {}, length_of_stem = {}, price = {};\n'.format(flower.color, 
                                                                                              flower.name, 
                                                                                              flower.freshness, 
                                                                                              flower.length_of_stem, 
                                                                                              flower.price)  
        for_return += '\nAccessories:\n'
        for accessor in self.bought_accessories:
            for_return += '{}\n'.format(accessor.name)
        return for_return
        
    def make_bouquet(self, roses=0, tulips=0, chamomiles=0, accessories=False):
        logging.info('attempt to create a bouquet')
        # if a bouquet is already created:
        if self.flowers_in_a_bouquet:
            logging.info('you already have a bouquet')
            while True:
                answer = raw_input('You have a bouquet. Do you want make out old bouquet and create new one? Y/N ')
                if answer.lower() == 'y':
                    logging.info('decided to re-create a bouquet')
                    self.make_out_bouquet()
                    self.make_bouquet(roses, tulips, chamomiles, accessories)
                    break
                elif answer.lower() == 'n':
                    break
                else:
                    print('You must press "Y" or "N", try again.')
                    continue

        # add flowers
        if roses:
            self.flowers_in_a_bouquet += [Rose() for _ in xrange(roses)]
        if tulips:
            self.flowers_in_a_bouquet += [Tulip() for _ in xrange(tulips)]
        if chamomiles:
            self.flowers_in_a_bouquet += [Chamomile() for _ in xrange(chamomiles)]
        if not self.flowers_in_a_bouquet:
            logging.info('attempt to create a bouquet without any flowers')
            return
        
        # add accessories
        if accessories:
            goods_in_stock = Accessories.list_of_accessories()
            print("""Choose number of the accessories you want.\nIf you have finished press "q" and "enter":\n""")
            while True:
                number = 0
                for accessor in goods_in_stock:
                    number += 1
                    print('{}. {} - {}$'.format(number, accessor.name, accessor.price))
                choice = raw_input()
                if choice == 'q':
                    logging.info('{} accessories were added to the bouquet'.format(len(self.bought_accessories)))
                    break
                try:
                    choice = int(choice)
                except ValueError:
                    print('You must enter number or "q"')
                    continue
                if choice > len(goods_in_stock):
                    print('You must enter number in price list')
                    continue
                self.bought_accessories.append(goods_in_stock[choice - 1])

    @property
    def cost_of_a_bouquet(self):
        return (sum([flower.price for flower in self.flowers_in_a_bouquet]) + 
                sum([accessor.price for accessor in self.bought_accessories]))

    @property
    def wilting_time(self):
        return sum([flower.lifetime - flower.age_of_the_flower for flower in self.flowers_in_a_bouquet]) / len(self.flowers_in_a_bouquet)

    def flowers_sorting(self, sort_parameter):
        """sort_parameter can be 'freshness', 'color', 'length_of_stem', 'price'"""
        logging.info('sorting of flowers in a bouquet; sort_parameter = {}'.format(sort_parameter))
        if sort_parameter == 'freshness':
            self.flowers_in_a_bouquet.sort(key = lambda x: x.freshness)
        elif sort_parameter == 'color':
            self.flowers_in_a_bouquet.sort(key = lambda x: x.color)
        elif sort_parameter == 'length_of_stem':
            self.flowers_in_a_bouquet.sort(key = lambda x: x.length_of_stem)
        elif sort_parameter == 'price':
            self.flowers_in_a_bouquet.sort(key = lambda x: x.price)
        else:
            logging.info('uncorrect value for sort_parameter')
            return
        logging.info('a bouquet was sorted')

    def search_flower_in_a_bouquet(self, name=False, freshness=False, color=False, length_of_stem=False, price=False, ):
        """
        name = 'Rose' or 'Tulip' or ...
        freshness = '10>' or '20<' or '50' or ...
        color = Red, or, Orange or ...
        length_of_stem = '10>' or '20<' or '50' or ...
        price = '1>' or '2<' or '5' or ...
        """
        logging.info('search flowers in a bouquet. Parameters:\nname={}\nfreshness={}\ncolor={}\nlength_of_stem={}\nprice={}'.format(name,
                                                                                                                                     freshness,
                                                                                                                                     color,
                                                                                                                                     length_of_stem,
                                                                                                                                     price))
        search_results = copy.deepcopy(self.flowers_in_a_bouquet)
        
        if name:
            search_results = filter(lambda x: x.name.lower() == name.lower(), search_results)

        if freshness:
            if freshness[-1:] == '>':
                search_results = filter(lambda x: x.freshness > int(freshness[:-1]), search_results)
            elif freshness[-1:] == '<':
                search_results = filter(lambda x: x.freshness < int(freshness[:-1]), search_results)
            else:
                search_results = filter(lambda x: x.freshness == int(freshness), search_results)

        if color:
            search_results = filter(lambda x: x.color.lower() == color.lower(), search_results)

        if length_of_stem:
            if length_of_stem[-1:] == '>':
                search_results = filter(lambda x: x.length_of_stem > int(length_of_stem[:-1]), search_results)
            elif length_of_stem[-1:] == '<':
                search_results = filter(lambda x: x.length_of_stem < int(length_of_stem[:-1]), search_results)
            else:
                search_results = filter(lambda x: x.length_of_stem == int(length_of_stem), search_results)

        if price:
            if price[-1:] == '>':
                search_results = filter(lambda x: x.price > int(price[:-1]), search_results)
            elif price[-1:] == '<':
                search_results = filter(lambda x: x.price < int(price[:-1]), search_results)
            else:
                search_results = filter(lambda x: x.price == int(price), search_results)

        if search_results:
            logging.info('search_results:')
            for flower in search_results:
                logging.info('{} {} freshness = {}, length_of_stem = {}, price = {} in a bouquet'.format(flower.color,
                                                                                                  flower.name,
                                                                                                  flower.freshness,
                                                                                                  flower.length_of_stem,
                                                                                                  flower.price))
        else:
            logging.info('no one flower satisfy the condition')

    def fast_search_for_name(self, name):
        logging.info('fast search for flower; name = {}'.format(name))
        for flower in self.flowers_in_a_bouquet:
            if flower.name.lower() == name.lower():
                logging.info('{} was found in the bouquet'.format(name))
                return
        logging.info('{} was not found in the bouquet'.format(name))

    def make_random_bouquet(self):
        logging.info('make random bouquet')
        self.make_bouquet(random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
        amount_of_accessories = random.randint(0, 9)
        for _ in xrange(amount_of_accessories):
            self.bought_accessories.append(Accessories.random_accessor())

    def make_out_bouquet(self):
        logging.info('make out a bouquet')
        if self.flowers_in_a_bouquet:
            for flower in self.flowers_in_a_bouquet:
                del flower
        
        if self.bought_accessories:
            for accessor in self.bought_accessories:
                del accessor

        self.flowers_in_a_bouquet = []
        self.bought_accessories = []
        logging.info('a bouquet was made out')



bouquet = Bouquet()
bouquet.make_random_bouquet()
logging.info(bouquet)

logging.info('cost_of_a_bouquet = {}'.format(bouquet.cost_of_a_bouquet))
logging.info('wilting_time = {}'.format(bouquet.wilting_time))

bouquet.search_flower_in_a_bouquet(name='Rose')
bouquet.search_flower_in_a_bouquet(freshness='10>')
bouquet.search_flower_in_a_bouquet(color='red')
bouquet.search_flower_in_a_bouquet(length_of_stem='50<')
bouquet.search_flower_in_a_bouquet(price='1>')
bouquet.search_flower_in_a_bouquet(name='Rose', freshness='50>', color='red', length_of_stem='40>', price='2>')
bouquet.fast_search_for_name('rose')

bouquet.flowers_sorting('freshness')
logging.info(bouquet)

bouquet.flowers_sorting('color')
logging.info(bouquet)

bouquet.flowers_sorting('length_of_stem')
logging.info(bouquet)

bouquet.flowers_sorting('price')
logging.info(bouquet)

bouquet.make_out_bouquet()
logging.info(bouquet)
