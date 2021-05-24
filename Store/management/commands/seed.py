# <project>/<app>/management/commands/seed.py
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.utils import Error, IntegrityError
from django.contrib.auth.models import Group, User
import logging
import random

from Store.models import *

logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete Address instances")
    User.objects.all().delete()
    Group.objects.all().delete()
    Order.objects.all().delete()
    Category.objects.all().delete()
    Menu.objects.all().delete()
    PaymentMethod.objects.all().delete()
    Location.objects.all().delete()
    OrderStatus.objects.all().delete()


def create_constant_data():
    """Creates an address object combining different elements from the list"""
    
    payment_options = ['Cash', 'Account']
    locations = ['Office', 'New canteen', 'Old canteen']
    order_statuses = ['Completed', 'Cancelled', 'Created', 'Uncollected', 'Ready for collection']

    logger.info("Creating payment options...")
    for option in payment_options:
        model = PaymentMethod(name=option)
        try:
            model.save()
            logger.info("{} payment method created.".format(model))
        except:
            logger.warning(f"{model} payment method already exists.")
    logger.info("Finished adding payment options.")

    logger.info("Creating locations...")
    for location in locations:
        model = Location(name=location)
        try:
            model.save()
            logger.info("{} location created.".format(model))
        except:
            logger.warning(f"{model} location already exists.")
    logger.info("Finished adding locations.")
    
    logger.info("Creating order status'...")
    for status in order_statuses:
        model = OrderStatus(name=status)
        try:
            model.save()
            logger.info("{} status created.".format(model))
        except:
            logger.warning(f"{model} status already exists.")
    logger.info("Finished adding locations.")


class CanteenContants:
    def __init__(self):
        self.location_office = Location.objects.get(name='Office')
        self.location_new = Location.objects.get(name='New canteen')
        self.location_old = Location.objects.get(name='Old canteen')

        self.payment_account = PaymentMethod.objects.get(name='Account')
        self.payment_cash = PaymentMethod.objects.get(name='Cash')

        self.status_completed = OrderStatus.objects.get(name='Completed')
        self.status_cancelled = OrderStatus.objects.get(name='Cancelled')
        self.status_created = OrderStatus.objects.get(name='Created')
        self.status_uncollected = OrderStatus.objects.get(name='Uncollected')
        self.status_ready = OrderStatus.objects.get(name='Ready for collection')

def category_price_generator(items):
    for item in items:
        d = item.category.description
        if d == 'Starters':
            item.price = random.randint(10, 30)
        elif d == 'Main':
            item.price = random.randint(25, 60)
        elif d == 'Sweets':
            item.price = random.randint(5, 20)
        elif d == 'Beverages':
            item.price = random.randint(5, 20)
        elif d == 'Fruit':
            item.price = random.randint(2, 10)

def create_sample_data():
    categories = [
        Category(description='Starters'),
        Category(description='Main'),
        Category(description='Sweets'),
        Category(description='Beverages'),
        Category(description='Fruit'),
    ]

    for category in categories:
        try:
            category.save()
        except IntegrityError:
            logger.warning(f"{category} already exists.")

    items = [
        Menu(category=categories[4], name='Apples', description='Juicy red apples, grown in our own well-kept garden.'),
        Menu(category=categories[4], name='Bananas', description='Large bananas with impressive sizes.'),
        Menu(category=categories[4], name='Pears', description='Juicy pears that will make your drool.'),
        Menu(category=categories[4], name='Oranges', description='Sweet oranges that are pleasant to eat and squeeze.'),
        Menu(category=categories[4], name='Peaches', description='Oh so sweet.'),
        
        Menu(category=categories[3], name='Valpre water', description='Stiller than quiet...'),
        Menu(category=categories[3], name='Coke', description='Not the white stuff.'),
        Menu(category=categories[3], name='Fanta', description='Is this the real life, or is this just "Fanta-see'),
        Menu(category=categories[3], name='Iron Brew', description='In order to pump those irons, you have got to try this... Mah bru'),
        Menu(category=categories[3], name='Orange juice', description='Squeezed from our own sweet oranges.'),
        
        Menu(category=categories[2], name='Gummy bears', description='Bouncing here and there and everywhere...'),
        Menu(category=categories[2], name='Wine gums', description='Now with 0% alchohol'),
        Menu(category=categories[2], name='Marshmellows', description='How many can you put in your mouth?'),
        Menu(category=categories[2], name='Kit kat', description='Have a break - have a KitKat'),
        Menu(category=categories[2], name="m%m's", description='Back to reality, oh there goes cavities'),
        
        Menu(category=categories[1], name='Fish and chips', description='Hot dish consisting of fried fish in batter, served with chips dressed in vinegar.'),
        Menu(category=categories[1], name='Hamburger', description="Seeded bun with juicy beef patty, onions, tomatoes and our secret burger sauce."),
        Menu(category=categories[1], name='Mayo sandwitch', description='Chichen and mayo sammy'),
        Menu(category=categories[1], name='Bunny chow', description='Half loaf filled with chicken and the hottest curry sauce. Guaranteed to fill that void!'),
        Menu(category=categories[1], name='Hotdog', description='Rol with not one, but TWO weenies and tomato sauce! What generosity!'),
        
        Menu(category=categories[0], name='Garlic bread', description='Guaranteed to keep Count Dracula away...'),
        Menu(category=categories[0], name='Chicken wings', description='Will clear up the sinuses.'),
        Menu(category=categories[0], name='Slap chips', description='Lekker slap chips dressed in vinegar.'),
    ]

    category_price_generator(items)

    for item in items:
        try:
            item.save()
        except Error as e:
            logger.warning(e)
    
def create_users():
    """Creates an address object combining different elements from the list"""
    logger.info("Creating group")
    group = ["Practice Manager"]

    groups = [
        Group(name="admin"),
        Group(name="manager"),
    ]

    for group in groups:
        try:
            group.save()
        except IntegrityError as e:
            logger.warning(f"Group {group.name} already exists.")

    users = [
        User(
            is_superuser = 1,
            username = 'jethro',
            is_staff = 1,
            is_active = 1,
            date_joined = datetime.now(),
            password = 'pbkdf2_sha256$216000$FEotATLzY5Qv$XV+l0jS4OHzglPJgHyBRVFDExn/9PcYvQ/j7rnoKo7E='
        ),
        User(
            is_superuser = 1,
            username = 'rudolf@a-i-solutions.co.za',
            is_staff = 1,
            is_active = 1,
            date_joined = datetime.now(),
            password = 'pbkdf2_sha256$216000$SHEx5hzQ603u$Z9WcLNA39aqHXlFDYC0cYmIOFvAg19t86d20jrPwrSE='
        )
    ]
    
    for user in users:
        try:
            user.save()
        except IntegrityError as e:
            logger.warning(f"User {user.username} already exists.")

    for user in users:
        groups[0].user_set.add(user)
        groups[0].save()

    logger.info("{} group created.".format(group))
    return group

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return
    create_users()
    create_constant_data()
    create_sample_data()