from logging import log
import src.Logger as logger
from src.WurzelBot import WurzelBot
import i18n

# Login data
user = ''
pw = ''
server = 17
lang = 'de' # de, en
portalacc = False
# Global vars
wurzelBot: WurzelBot = object

# enable logging? change to True else change it to False
log = False

i18n.load_path.append('lang')
i18n.set('locale', lang)
i18n.set('fallback', 'en')

def main():
    logo()
    init()
    logging()
    
    while True:
        print('')
        userInput = input('▶ ').strip()
        inputLower = userInput.lower()

        if inputLower == 'exit': closeConnection()
        elif inputLower == 'bee': bee()
        elif inputLower == 'harvest': harvest()
        elif inputLower == '?' or inputLower == 'help': help()
        elif inputLower.startswith('buy'): buy(userInput)
        elif inputLower.startswith('grow'): grow(userInput)
        elif inputLower.startswith('lowest'): lowest(userInput)
        elif inputLower.startswith('stock'): getStock(userInput)
        elif inputLower == 'user': userData()
        elif inputLower == 'water': water()
        elif inputLower == 'weed': removeWeed()
        elif inputLower == 'bonus': getDailyLoginBonus()
        elif inputLower == 'wimp': processWimp()
        elif inputLower.startswith('details'): productDetails(userInput)
        else:
            print('Unknown command type \'help\' or \'?\' to see all available commands')


def logo():
    print('  _      __                 _____       __ ')
    print(' | | /| / /_ _________ ___ / / _ )___  / /_')
    print(' | |/ |/ / // / __/_ // -_) / _  / _ \/ __/')
    print(' |__/|__/\_,_/_/  /__/\__/_/____/\___/\__/ ')
    print('')

def init():
    print(i18n.t('wimpb.initialize_bot'))
    
    if user == '' or pw == '' or portalacc == '':
        print(i18n.t('wimpb.login_credentials_not_configured'))
        print('')
        exit()
    
    global wurzelBot
    wurzelBot = WurzelBot()
    succ = wurzelBot.launchBot(server, user, pw, lang, portalacc)
    if succ != True:
        exit(-1)

def closeConnection():
    print(i18n.t('wimpb.close_connection'))
    print('')
    wurzelBot.exitBot()
    exit()

def help():
    print('Available commands:')
    print('-------------------')
    print('bee          Send bees')
    print('bonus        Get the daily login bonus')
    print('details      Show details to the products')
    print('             Opt. argument: "all"')
    print('buy          Buy a given plant')
    print('exit         Close connection and exit bot')
    print('grow         Grow a given plant')
    print('harvest      Harvest all gardens')
    print('help         Show all available commands')
    print('lowest       Show the plant with the lowest stock (unequal zero)')
    print('             Opt. argument: "single"')
    print('stock        Show all plants in stock')
    print('             Opt. argument: "sort"')
    print('user         Show details to the current user')
    print('water        Water all plants')
    print('weed         Remove all weed')
    print('wimp         Process Wimp Customers in Gardens')

def harvest():
    print('Harvest all gardens...')
    wurzelBot.harvestAllGarden()

def bee():
    print('Sending bees...')
    wurzelBot.sendBienen()

def buy(argStr : str):
    argStr = argStr.replace('buy', '', 1).strip()
    args = argStr.split(' ')

    if len(args) != 2 or (len(args) == 2 and not args[1].isnumeric()):
        print('Cannot parse input.')
        print('Expected format: grow [plant name] [opt. amount]')
        return

    print('Buying ' + args[1] + ' ' + args[0] + '...')
    wurzelBot.doBuyFromShop(args[0], int(args[1]))

def grow(argStr : str):
    argStr = argStr.replace('grow', '', 1).strip()
    args = argStr.split(' ')
    
    if len(args) > 2 or len(args) < 1 or args[0] == '' or (len(args) == 2 and not args[1].isnumeric()):
        print('Cannot parse input.')
        print('Expected format: grow [plant name] [opt. amount]')
        return
    
    if len(args) == 1:
        print('Grow ' + args[0] + '...')
        wurzelBot.growPlantsInGardens(args[0])
    if len(args) == 2:
        print('Grow ' + args[1] + ' ' + args[0] + '...')
        wurzelBot.growPlantsInGardens(args[0], int(args[1]))

def lowest(argStr : str):
    argStr = argStr.replace('lowest', '', 1).strip()
    args = argStr.split(' ')
    
    if len(args) > 1 or (len(args) == 1 and args[0] != 'single' and args[0] != ''):
        print('Cannot parse input.')
        print('Expected format: lowest [single]')
        return

    if args[0] == '':
        print(wurzelBot.getLowestPlantStockEntry())
    elif args[0] == 'single':
        print(wurzelBot.getLowestSinglePlantStockEntry())

def getStock(argStr : str):
    argStr = argStr.replace('stock', '', 1).strip()
    args = argStr.split(' ')
    
    if len(args) > 1 or (len(args) == 1 and args[0] != 'sort' and args[0] != ''):
        print('Cannot parse input.')
        print('Expected format: stock [sort]')
        return

    if args[0] == '':
        wurzelBot.printStock()
    elif args[0] == 'sort':
        print(wurzelBot.getOrderedStockList())

def userData():
    colWidth = 20
    print('User:'.ljust(colWidth) + wurzelBot.spieler.getUserName())
    print('Anzahl der Gärten:'.ljust(colWidth) + str(wurzelBot.spieler.numberOfGardens))
    print('Level:'.ljust(colWidth) + str(wurzelBot.spieler.getLevelNr()) + ' (' + wurzelBot.spieler.getLevelName() + ')')
    print('Bar:'.ljust(colWidth) + wurzelBot.spieler.getBarFormated())
    print('Points:'.ljust(colWidth) + f'{wurzelBot.spieler.getPoints():,}'.replace(',', '.'))
    print('Coins:'.ljust(colWidth) + str(wurzelBot.spieler.getCoins()))
    
def water():
    print('Water all plants in all gardens...')
    wurzelBot.waterPlantsInAllGardens()

def productDetails(argStr : str):
    argStr = argStr.replace('details', '', 1).strip()
    args = argStr.split(' ')

    if len(args) > 1 or (len(args) == 1 and args[0] != 'all' and args[0] != ''):
        print('Cannot parse input.')
        print('Expected format: details [all]')
        return

    if args[0] == '':
        wurzelBot.printPlantDetails()
    elif args[0] == 'all':
        wurzelBot.printProductDetails()

def removeWeed():
    print(i18n.t('wimpb.remove_weed_from_all_gardens'))
    wurzelBot.removeWeedInAllGardens()

def getDailyLoginBonus():
    print('Claiming daily login bonus...')
    wurzelBot.getDailyLoginBonus()
    
def processWimp():
    """Process Wimp Customers in Gardens"""
    print(i18n.t('wimpb.process_wimps'))
    wurzelBot.sellWimpsProducts(0, 0)

def logging():
    if log:
        logger.logger()

if __name__ == "__main__":
    main()
