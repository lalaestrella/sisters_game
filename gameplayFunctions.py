import random

from initGameObjects import ChaosThePlayer, QueenThePlayer, VictorThePlayer, JulianThePlayer, CompassTheCard, \
    GuildThePlayer, WarTheSister, WeaponShopTheCard, WitchShopTheCard, PlagueTheSister, HungerTheSister, \
    DeathTheSister, allRandomEvents, selectWeapon, selectSister, swapWeapons, EyeTheCard, GloveTheCard
from writelogs import logs


# ФУНКЦИЯ ПРОВЕРКИ ПОБЕДЫ
def currentWinner():
    # сначала проверяем победу Хаоса
    if ChaosThePlayer.influence >= 30:
        return ChaosThePlayer
    if QueenThePlayer.havingSisters == 4:
        return ChaosThePlayer
    if GuildThePlayer.havingSisters == 4:
        return ChaosThePlayer
    # дальше смотрим апокалипсис: если он случился или предотвратился, то пофиг на влияние
    if VictorThePlayer.havingSisters == 4 or JulianThePlayer.havingSisters == 4:
        if VictorThePlayer.isHavingCard(CompassTheCard) or QueenThePlayer.isHavingCard(CompassTheCard):
            return VictorThePlayer
        if JulianThePlayer.isHavingCard(CompassTheCard) or GuildThePlayer.isHavingCard(CompassTheCard):
            return JulianThePlayer
    # теперь проверяем влияние
    if GuildThePlayer.influence >= 30 and GuildThePlayer.havingSisters >= 1:
        if QueenThePlayer.influence >= 30 and QueenThePlayer.isHavingCard(
                WarTheSister):  # вдруг распределилось по принципу 30-30
            return ChaosThePlayer  # никакой ничьи, всё по хардкору )))
        else:
            return GuildThePlayer
    if QueenThePlayer.influence >= 30 and QueenThePlayer.isHavingCard(WarTheSister):
        return QueenThePlayer
    return 0


# ФУНКЦИИ ГЕЙМПЛЕЯ - ПЕРВЫЙ ЭТАП ХОДА. ГИЛЬДИЯ ВОРУЕТ

def stealACard(player):
    victimPlayer = random.choice([VictorThePlayer, JulianThePlayer, QueenThePlayer, ChaosThePlayer])
    cardsToSteal = []
    for card in victimPlayer.cards:
        if card.isArtefact() or card.isWeapon():
            cardsToSteal.append(card)
    stolenCard = random.choice(cardsToSteal)
    player.getCard(stolenCard, victimPlayer)
    card.makePrivate()
    logs.print(
        "Карта " + stolenCard.name + " украдена Гильдией. Предыдущий владелец: " + victimPlayer.name + ".\n")

# ФУНКЦИИ ГЕЙМПЛЕЯ - ВТОРОЙ ЭТАП ХОДА

def sellSomething(player):
    print("Желаете что-нибудь продать?")
    while True:
        print("Введите ответ: 1 - да, 0 - нет.")
        answer = input()
        if answer == "1":
            while True:
                print("У вас " + str(player.money) + " монет.")
                print("Что будем продавать?")
                print("1 - очки влияния")
                print("2 - локации")
                print("3 - оружие")
                print("4 - артефакты")
                print("0 - ничего")
                answer2 = input()
                if answer2 == "1":
                    # считаем, сколько очков влияния мы можем продать
                    influenceToSold = player.influenceToSold()
                    logs.print("У вас " + str(influenceToSold) + " свободных очков влияния. Вы можете продать их по "
                                                                 "курсу 1 очко влияния = 2 монеты.")
                    # продаём
                    logs.print("Сколько очков влияния вы хотите продать? Введите число от 0 до " + str(influenceToSold))
                    answer3 = logs.input()
                    try:
                        if int(answer3) > influenceToSold:
                            logs.print("Вы не можете продать " + answer3 + " очков влияния, у вас всего "
                                       + str(influenceToSold) + " свободных очков.\n")
                        else:
                            if int(answer3) < 0:
                                logs.print("Вы не можете продать " + answer3 + " очков влияния.\n")
                            else:
                                player.influence -= int(answer3)
                                player.money += int(answer3) * 2
                                logs.print(
                                    "Продажа очков влияния завершена. Теперь у вас " + str(player.money) + ' монет и '
                                    + str(player.influence - influenceToSold + int(answer3)) + "+"
                                    + str(influenceToSold - int(answer3)) + "=" + str(player.influence)
                                    + " очков влияния.\n")
                    except Exception:
                        print("Некорректный ввод. Попробуйте ещё раз.\n")
                if answer2 == "2":
                    # никогда так не делайте, но: собираем массив из всех локаций на руках
                    allLocations = []
                    for card in player.cards:
                        if card.isLocation():
                            allLocations.append(card)
                    if len(allLocations) > 0:  # если есть, что продавать
                        logs.print("Локации на продажу:\n")
                        for locationCard in allLocations:
                            logs.print("ЛОТ №" + str(allLocations.index(locationCard) + 1))
                            locationCard.writeInfo()
                            logs.print("")
                        # продаём
                        logs.print("Введите номер лота, который желаете продать.")
                        print("Вы получите в десять раз больше монет, чем стоимость локации.")
                        print("Вы потеряете бонусы локации и принадлежащие ей очки влияния.")
                        print("Для отмены продажи введите 0.")
                        answer3 = logs.input()
                        if answer3 == "0":
                            continue
                        try:
                            locationCost = allLocations[int(answer3) - 1].influence * 10
                            logs.print(
                                allLocations[int(answer3) - 1].name + " будет продано за " + str(
                                    locationCost) + " монет.")
                            player.money += locationCost
                            # влияние переводится внутри функции передачи карты
                            ChaosThePlayer.getCard(allLocations[int(answer3) - 1], player)
                            logs.print("Продажа локации " + allLocations[
                                int(answer3) - 1].name + " завершена. Теперь у вас " + str(player.money) + " монет и "
                                       + str(player.influence) + " очков влияния.\n")
                        except Exception:
                            print("Некорректный ввод. Попробуйте ещё раз.\n")
                    else:  # если продавать нечего
                        logs.print("У вас нет локаций на продажу.\n")
                if answer2 == "3":
                    # никогда так не делайте, но: собираем массив из всего оружия на руках
                    allWeapons = []
                    for card in player.cards:
                        if card.isWeapon():
                            allWeapons.append(card)
                    if len(allWeapons) > 0:  # если есть, что продавать
                        logs.print("Оружие на продажу:\n")
                        for weaponCard in allWeapons:
                            logs.print("ЛОТ №" + str(allWeapons.index(weaponCard) + 1))
                            weaponCard.writeInfo()
                            logs.print("")
                        # продаём
                        logs.print("Введите номер лота, который желаете продать.")
                        if player != GuildThePlayer:
                            print("Выбранное оружие будет продано дону Реджани за половину цены.")
                        else:  # разбойники продают по полной цене, остальные - за половину
                            print("Выбранное оружие будет продано дону Реджани за полную цену.")
                        print("Для отмены продажи введите 0.")
                        answer3 = logs.input()
                        if answer3 == "0":
                            continue
                        try:
                            weaponStartCost = allWeapons[int(answer3) - 1].cost
                            if player != GuildThePlayer:
                                finalCost = int(weaponStartCost / 2)
                            else:
                                finalCost = weaponStartCost
                            logs.print(
                                allWeapons[int(answer3) - 1].name + " будет продано за " + str(finalCost) + " монет.")
                            player.money += finalCost
                            allWeapons[int(answer3) - 1].makePrivate()  # после продажи оружие становится закрытым
                            ChaosThePlayer.getCard(allWeapons[int(answer3) - 1], player)
                            if player.isHavingCard(WeaponShopTheCard):
                                logs.print("Вы - владелец оружейной лавки. Получите дополнительно 2 монеты.")
                                player.money += 2
                            logs.print("Продажа оружия " + allWeapons[
                                int(answer3) - 1].name + " завершена. Теперь у вас " + str(player.money) + " монет.\n")
                        except Exception:
                            print("Некорректный ввод. Попробуйте ещё раз.\n")
                    else:  # если продавать нечего
                        logs.print("У вас нет оружия на продажу.\n")
                if answer2 == "4":
                    # никогда так не делайте, но: собираем массив из всех артефактов на руках
                    allArtefacts = []
                    for card in player.cards:
                        if card.isArtefact():
                            allArtefacts.append(card)
                    if len(allArtefacts) > 0:  # если есть, что продавать
                        logs.print("Артефакты на продажу:\n")
                        for artefactCard in allArtefacts:
                            logs.print("ЛОТ №" + str(allArtefacts.index(artefactCard) + 1))
                            artefactCard.writeInfo()
                            logs.print("")
                        # продаём
                        logs.print("Введите номер лота, который желаете продать.")
                        if player != GuildThePlayer:
                            print("Выбранный артефакт будет продан ведьме за половину цены.")
                        else:  # разбойники продают по полной цене, остальные - за половину
                            print("Выбранный артефакт будет продан ведьме за полную цену.")
                        print("Для отмены продажи введите 0.")
                        answer3 = logs.input()
                        if answer3 == "0":
                            continue
                        try:
                            artefactStartCost = allArtefacts[int(answer3) - 1].cost
                            if player != GuildThePlayer:
                                finalCost = int(artefactStartCost / 2)
                            else:
                                finalCost = artefactStartCost
                            logs.print(
                                allArtefacts[int(answer3) - 1].name + " будет продано за " + str(finalCost) + " монет.")
                            player.money += finalCost
                            allArtefacts[
                                int(answer3) - 1].makePrivate()  # после продажи артефакт становится закрытым
                            ChaosThePlayer.getCard(allArtefacts[int(answer3) - 1], player)
                            if player.isHavingCard(WitchShopTheCard):
                                logs.print("Вы - владелец лавки ведьмы. Получите дополнительно 5 монет.")
                                player.money += 5
                            logs.print("Продажа артефакта " + allArtefacts[
                                int(answer3) - 1].name + " завершена. Теперь у вас " + str(player.money) + " монет.\n")
                        except Exception:
                            print("Некорректный ввод. Попробуйте ещё раз.\n")
                    else:  # если продавать нечего
                        logs.print("У вас нет артефактов на продажу.\n")
                if answer2 == "0":
                    logs.print("Вы закончили продавать.\n")
                    break
                if answer2 not in ["0", "1", "2", "3", "4"]:
                    print("Некорректный ввод. Попробуйте ещё раз.")
            break
        else:
            if answer == "0":
                logs.print("Вы решили ничего не продавать.\n")
                break
            else:
                print("Некорректный ввод. Попробуйте ещё раз.")


def buyInfluence(player):
    if player.money >= 3:
        print("Желаете купить 1 очко влияния за 3 монеты?")
        while True:
            print("Введите ответ: 1 - да, 0 - нет.")
            answer = input()
            if answer == "1":
                player.money -= 3
                player.influence += 1
                logs.print(
                    "Покупка очков влияния завершена. Теперь у вас " + str(player.money) + " монет и "
                    + str(player.influence) + " очков влияния.\n")
                break
            else:
                if answer == "0":
                    logs.print(
                        "Покупка очков влияния не совершена. У вас " + str(player.money) + " монет и "
                        + str(player.influence) + " очков влияния.\n")
                    break
                else:
                    print("Некорректный ввод. Попробуйте ещё раз.")
    else:
        logs.print("У вас нет денег, чтобы купить очки влияния.\n")


def buyWeapon(player):
    print("Желаете купить оружие?")
    while True:
        logs.print("Введите ответ: 1 - да, 0 - нет.")
        answer = input()
        if answer == "1":
            print("Добро пожаловать в ☆˙˙· .Оружейную Лавку дона Реджани˙˙· . ☆")
            print("Здесь вы можете выбрать оружие на любой вкус.\n")

            # никогда так не делайте, но: собираем массив из всего оружия не на руках
            allWeapons = []
            for card in ChaosThePlayer.cards:
                if card.isWeapon():
                    allWeapons.append(card)

            if len(allWeapons) == 0:  # если в игре не осталось свободного оружия
                print("К сожалению, дону Реджани нечего вам предложить.\n")
                break
            else:  # если осталось, будем выводить список
                print("Вот что предлагает дон Реджани сегодня:\n")

            weaponsToBuy = []
            # если свободного оружия больше трёх, выбираем три рандомных
            if len(allWeapons) > 3:
                for i in [1, 2, 3]:
                    tempWeaponCard = random.choice(allWeapons)
                    weaponsToBuy.append(tempWeaponCard)
                    allWeapons.remove(tempWeaponCard)
            else:
                weaponsToBuy = allWeapons

            # выводим список для покупки
            for weaponCard in weaponsToBuy:
                logs.print("ЛОТ №" + str(weaponsToBuy.index(weaponCard) + 1))
                weaponCard.writeInfo()
                logs.print("")

            print("Введите номер желаемого лота для покупки или введите 0, чтобы выйти из магазина без покупки.")
            print("Вы можете купить только один лот. Доступные монеты: " + str(player.money))
            if player.isHavingCard(WeaponShopTheCard):
                logs.print("Вы - владелец оружейной лавки. Для вас действует скидка в 2 монеты на любое оружие.")

            while True:
                buyIndex = logs.input()
                if buyIndex == "0":
                    logs.print(
                        "Вы ушли из лавки без покупок.\n")
                    break
                else:
                    try:
                        weaponCost = weaponsToBuy[int(buyIndex) - 1].cost
                        if player.isHavingCard(WeaponShopTheCard):  # если игрок владеет оружейной лавкой, делаем скидку
                            weaponCost = weaponCost - 2
                            if weaponCost < 0:  # цена не может быть отрицательной
                                weaponCost = 0
                        if player.money >= weaponCost:  # проверка, что хватает денег
                            player.money -= weaponCost
                            player.getCard(weaponsToBuy[int(buyIndex) - 1], ChaosThePlayer)
                            logs.print(
                                "Покупка оружия завершена. Теперь у вас " + str(player.money) + " монет и "
                                + weaponsToBuy[int(buyIndex) - 1].name + ".\n")
                            break
                        else:
                            print("У вас недостаточно денег на этот лот.")
                            print(
                                "Введите номер желаемого лота для покупки или введите 0, чтобы выйти из магазина без "
                                "покупки.")
                            print("Вы можете купить только один лот. Доступные монеты: " + str(player.money))
                            if player.isHavingCard(WeaponShopTheCard):
                                print(
                                    "Вы - владелец оружейной лавки. Для вас действует скидка в 2 монеты на любое "
                                    "оружие.")
                    except Exception:
                        print("Некорректный ввод. Попробуйте ещё раз.")
            break
        else:
            if answer == "0":
                logs.print(
                    "Вы не стали посещать оружейную лавку.\n")
                break
            else:
                print("Некорректный ввод. Попробуйте ещё раз.")


def buyArtefact(player):
    print("Желаете купить артефакт?")
    while True:
        logs.print("Введите ответ: 1 - да, 0 - нет.")
        answer = input()
        if answer == "1":
            print("Добро пожаловать в ЛАВКУ ВЕДЬМЫ!")
            print("Здесь вы найдёте самые таинственные предметы.\n")

            # никогда так не делайте, но: собираем массив из всего оружия не на руках
            allArtefacts = []
            for card in ChaosThePlayer.cards:
                if card.isArtefact():
                    allArtefacts.append(card)

            if len(allArtefacts) == 0:  # если в игре не осталось свободного оружия
                print("Артефакты для продажи закончились. Сразитесь с другими игроками, чтобы получить их артефакты.\n")
                break
            else:  # если осталось, будем выводить список
                print("Ведьмина витрина:\n")

            artefactsToBuy = []
            # если свободного оружия больше трёх, выбираем три рандомных
            if len(allArtefacts) > 3:
                for i in [1, 2, 3]:
                    tempCard = random.choice(allArtefacts)
                    artefactsToBuy.append(tempCard)
                    allArtefacts.remove(tempCard)
            else:
                artefactsToBuy = allArtefacts

            # выводим список для покупки
            for artefactCard in artefactsToBuy:
                logs.print("ЛОТ №" + str(artefactsToBuy.index(artefactCard) + 1))
                artefactCard.writeInfo()
                logs.print("")

            print("Введите номер желаемого лота для покупки или введите 0, чтобы выйти из магазина без покупки.")
            print("Вы можете купить только один лот. Доступные монеты: " + str(player.money))
            if player.isHavingCard(WitchShopTheCard):
                logs.print("Вы - владелец лавки ведьмы. Для вас действует скидка в 5 монет на любой артефакт.")

            while True:
                buyIndex = logs.input()
                if buyIndex == "0":
                    logs.print(
                        "Вы ушли из лавки без покупок.\n")
                    break
                else:
                    try:
                        artefactCost = artefactsToBuy[int(buyIndex) - 1].cost
                        if player.isHavingCard(WitchShopTheCard):  # если игрок владеет лавкой ведьмы, делаем скидку
                            artefactCost = artefactCost - 5
                            if artefactCost < 0:  # цена не может быть отрицательной
                                artefactCost = 0
                        if player.money >= artefactCost:  # проверка, что хватает денег
                            player.money -= artefactCost
                            player.getCard(artefactsToBuy[int(buyIndex) - 1], ChaosThePlayer)
                            logs.print(
                                "Покупка артефакта завершена. Теперь у вас " + str(player.money) + " монет и "
                                + artefactsToBuy[int(buyIndex) - 1].name + ".\n")
                            break
                        else:
                            print("У вас недостаточно денег на этот лот.")
                            print(
                                "Введите номер желаемого лота для покупки или введите 0, чтобы выйти из магазина без "
                                "покупки.")
                            print("Вы можете купить только один лот. Доступные монеты: " + str(player.money))
                            if player.isHavingCard(WitchShopTheCard):
                                logs.print(
                                    "Вы - владелец лавки ведьмы. Для вас действует скидка в 2 монеты на любой артефакт.")
                    except Exception:
                        print("Некорректный ввод. Попробуйте ещё раз.")
            break
        else:
            if answer == "0":
                logs.print(
                    "Вы не стали посещать лавку ведьмы.\n")
                break
            else:
                print("Некорректный ввод. Попробуйте ещё раз.")


# ФУНКЦИИ ГЕЙМПЛЕЯ - ТРЕТИЙ ЭТАП ХОДА

def inviteToSisterFight(attackingPlayer):
    print("Желаете сразиться за сестру?")
    while True:
        logs.print("Введите ответ: 1 - да, 0 - нет.")
        answer = input()
        if answer == "1":

            if attackingPlayer.isHavingCard(CompassTheCard):  # владелец компаса знает, у кого сёстры
                logs.print("Вы - владелец компаса. Вы знаете, у кого какая сестра.")
                CompassTheCard.makePublic()  # спалился
                for player in [VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer, ChaosThePlayer]:
                    for card in player.cards:
                        if card.isSister():
                            logs.print("Карта сестры " + card.name + " принадлежит персонажу " + player.name)
                logs.print("")

            while True:
                logs.print("За какую сестру вы хотите сразиться?")
                print("1 - Чума, Мари")
                print("2 - Война, Елена")
                print("3 - Голод, Роксана")
                print("4 - Смерть, Энни")
                print("0 - не хочу сражаться")
                answer2 = input()
                if answer2 in ["1", "2", "3", "4"]:
                    # проверяем корректность введённых данных
                    match answer2:
                        case "1":
                            trophyCard = PlagueTheSister
                        case "2":
                            trophyCard = WarTheSister
                        case "3":
                            trophyCard = HungerTheSister
                        case "4":
                            trophyCard = DeathTheSister
                        case _:
                            logs.print("Произошла ошибка в match-case в выборе сестры для боя")
                            break
                    if attackingPlayer.isHavingCard(trophyCard):
                        logs.print("Вы не можете сражаться за свою собственную карту.")
                        continue
                    while True:
                        logs.print("С кем будете сражаться?")
                        print("1 - Виктор Кастелли")
                        print("2 - Джулиан Медичи")
                        print("3 - Гильдия Разбойников")
                        print("4 - Кровавая Королева")
                        print("0 - не хочу сражаться")
                        print(
                            "Внимание: вы не можете поменять уже выбранную сестру. 0 равносильно нежеланию сражаться.")
                        answer3 = input()
                        if answer3 in ["1", "2", "3", "4"]:
                            match answer3:
                                # проверяем корректность введённых данных
                                case "1":
                                    defPlayer = VictorThePlayer
                                case "2":
                                    defPlayer = JulianThePlayer
                                case "3":
                                    defPlayer = GuildThePlayer
                                case "4":
                                    defPlayer = QueenThePlayer
                                case _:
                                    logs.print("Произошла ошибка в match-case в выборе противника для боя")
                                    break
                            if attackingPlayer == defPlayer:
                                logs.print("Вы не можете сражаться сами с собой.")
                                continue
                            else:
                                # если всё в порядке, инициируем драку!
                                fight(attackingPlayer, defPlayer, trophyCard)
                                return
                        if answer3 == "0":
                            logs.print(
                                "Вы не стали сражаться за сестру.\n")
                            break
                        else:
                            print("Некорректный ввод. Попробуйте ещё раз.")
                if answer2 == "0":
                    logs.print(
                        "Вы не стали сражаться за сестру.\n")
                    break
                else:
                    print("Некорректный ввод. Попробуйте ещё раз.")
        else:
            if answer == "0":
                logs.print(
                    "Вы не стали сражаться за сестру.\n")
                break
            else:
                print("Некорректный ввод. Попробуйте ещё раз.")
        break


def inviteToFight(attackingPlayer):
    print("Желаете сразиться за карту (локация/оружие/артефакт)?")
    while True:
        logs.print("Введите ответ: 1 - да, 0 - нет.")
        answer = input()
        if answer == "1":
            # выводим список всех открытых карт с указанием владельца
            allAvailableCards = []
            availableCardsHolders = []
            for player in [VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer]:
                if player != attackingPlayer:  # проходимся только по противникам
                    for card in player.cards:
                        logs.printtologs("Смотрю карту " + card.name + " владельца " + player.name)
                        # собираем открытые карты, не являющиеся сёстрами
                        if not card.isSister():
                            if attackingPlayer.isHavingCard(EyeTheCard):
                                EyeTheCard.makePublic()  # спалился
                                logs.printtologs("Кладу в глазастый массив карту " + card.name + " владельца " + player.name)
                                allAvailableCards.append(card)
                                # в отдельный массив добавляем владельцев, чтобы их не потерять
                                availableCardsHolders.append(player)
                            else:
                                if not card.isPrivate:
                                    logs.printtologs("Кладу в массив карту " + card.name + " владельца " + player.name)
                                    allAvailableCards.append(card)
                                    # в отдельный массив добавляем владельцев, чтобы их не потерять
                                    availableCardsHolders.append(player)
            if len(allAvailableCards) > 0:  # если есть, за что драться
                logs.print("Открытые карты:\n")
                for card in allAvailableCards:
                    logs.print("ЛОТ №" + str(allAvailableCards.index(card) + 1))
                    card.writeInfo()
                    logs.print("Владелец: " + availableCardsHolders[allAvailableCards.index(card)].name)
                    logs.print("")
                while True:
                    logs.print("Введите номер карты, за которую хотите сразиться, или 0, если передумали сражаться.")
                    answer2 = input()
                    if answer2 == "0":
                        logs.print(
                            "Вы не стали сражаться за карту.\n")
                        break
                    else:
                        try:
                            trophyCard = allAvailableCards[int(answer2) - 1]
                            defPlayer = availableCardsHolders[int(answer2) - 1]
                            fight(attackingPlayer, defPlayer, trophyCard)
                            return
                        except Exception:
                            print("Некорректный ввод номера трофейной карты. Попробуйте ещё раз.")
            else:
                logs.print(
                    "У других игроков нет открытых карт. К сожалению, сражения не будет.\n")
                break
        else:
            if answer == "0":
                logs.print(
                    "Вы не стали сражаться за карту.\n")
                break
            else:
                print("Некорректный ввод. Попробуйте ещё раз.")


def fight(attackingPlayer, defendingPlayer, trophyCard):
    logs.print("ВНИМАНИЕ! ВНИМАНИЕ! НАЧИНАЕТСЯ БИТВА!")
    logs.print(attackingPlayer.name + " нападает на " + defendingPlayer.name + "!\n")

    # атакующий выбирает оружие и сестру
    logs.print(attackingPlayer.name + ", ваши статы:")
    attackingPlayer.fightStats.writeStats()

    logs.print("\n" + attackingPlayer.name + ", пришла пора выбрать оружие.\n")
    attackWeapon = selectWeapon(attackingPlayer)

    logs.print(attackingPlayer.name + ", присоединится ли к вам сестра?\n")
    attackSister = selectSister(attackingPlayer)

    # защищающийся выбирает оружие и сестру
    logs.print(defendingPlayer.name + ", ваши статы:")
    defendingPlayer.fightStats.writeStats()

    logs.print("\n" + defendingPlayer.name + ", пришла пора выбрать оружие.\n")
    defWeapon = selectWeapon(defendingPlayer)

    logs.print(defendingPlayer.name + ", присоединится ли к вам сестра?\n")
    defSister = selectSister(defendingPlayer)

    # всё оружие становится публичным
    attackWeapon.isPrivate = False
    defWeapon.isPrivate = False
    # сёстры протухают
    attackSister.isExpired = True
    defSister.isExpired = True

    logs.print("=== БОЙ ===\n")

    logs.print("Нападающий:")
    logs.print("Имя: " + attackingPlayer.name)
    attackingPlayer.fightStats.writeStats()
    logs.print("Оружие:")
    attackWeapon.writeInfo()
    logs.print("Сестра:")
    attackSister.writeInfo()

    logs.print("\nЗащищающийся:")
    logs.print("Имя: " + defendingPlayer.name)
    defendingPlayer.fightStats.writeStats()
    logs.print("Оружие:")
    defWeapon.writeInfo()
    logs.print("Сестра:")
    defSister.writeInfo()

    logs.print("\nНа кону:")
    trophyCard.writeInfo()
    logs.print("")

    winnerOfTheFight = attackingPlayer.winnerOfTheFight(attackWeapon, attackSister, defendingPlayer, defWeapon,
                                                        defSister)

    if attackingPlayer == winnerOfTheFight:
        logs.print("\n=== ПОБЕДИТЕЛЬ: " + attackingPlayer.name.upper() + " ===\n")
        logs.print("Атакующий выиграл, а потому получает желаемую карту.")
        # если была битва за сестру - карты у проигравшего может не быть
        if trophyCard.isSister:
            if defendingPlayer.isHavingCard(trophyCard):
                attackingPlayer.getCard(trophyCard, defendingPlayer)
                logs.print(
                    "Карта " + trophyCard.name + " передана персонажу " + attackingPlayer.name + ". Предыдущий владелец: " + defendingPlayer.name)
            else:
                logs.print("Вот только у персонажа " + defendingPlayer.name + " нет карты " + trophyCard.name + ".")
                logs.print("Такие дела, " + attackingPlayer.name + ".")
        # иначе - проигравший отдаёт карту
        else:
            attackingPlayer.getCard(trophyCard, defendingPlayer)
            logs.print(
                "Карта " + trophyCard.name + " передана персонажу " + attackingPlayer.name + ". Предыдущий владелец: " + defendingPlayer.name)
    else:
        if defendingPlayer == winnerOfTheFight:
            logs.print("\n=== ПОБЕДИТЕЛЬ: " + defendingPlayer.name.upper() + " ===\n")
            if attackingPlayer.isHavingCard(GloveTheCard):
                logs.print("Атакующий проиграл, но у него есть Перчатка дуэлянта, поэтому ему ничего не будет.\n")
                GloveTheCard.makePublic()  # спалился
            else:
                logs.print("Атакующий проиграл, а потому отдаёт победителю 3 очка влияния.\n")
                attackingPlayer.loseInfluence(3, defendingPlayer)
        else:
            logs.print("\n=== НИЧЬЯ ===\n")
            logs.print("Ничего не происходит.")
    logs.print("\nБой окончен. Участвовавшие в бою сёстры устали, засвеченное оружие перестало быть скрытым.\n")


# ФУНКЦИИ ГЕЙМПЛЕЯ - ЧЕТВЁРТЫЙ ЭТАП ХОДА

def randomCard(player):
    if player == JulianThePlayer:
        cardsToShow = []
        i = 1
        while i <= 3:
            tempCard = random.choice(allRandomEvents)
            if tempCard in cardsToShow:  # чтобы без повторок
                continue
            else:
                cardsToShow.append(tempCard)
                i += 1

        print("Дорогой Джулиан, у вселенной для тебя много вариантов!\n")

        # выводим список для выбора
        for tempCard in cardsToShow:
            logs.print("СОБЫТИЕ №" + str(cardsToShow.index(tempCard) + 1))
            try:
                tempCard.writeInfo()
            except Exception:
                logs.print("БАГ!!! Произошла проблема с картой: " + tempCard.name)
                logs.print("Пожалуйста, не выбирайте её.")
            logs.print("")

        while True:
            logs.print("Введите номер события, которое выбираете.")
            cardIndex = logs.input()
            try:
                if (int(cardIndex) - 1) < 0:  # чтобы не работало на индексе -1
                    raise Exception
                randomEvent = cardsToShow[int(cardIndex) - 1]
                logs.print("Карта выбрана: " + randomEvent.name)
                break
            except Exception:
                print("Некорректный ввод. Попробуйте ещё раз.")
    else:
        randomEvent = random.choice(allRandomEvents)

    print("Случайное событие!\n")
    try:
        randomEvent.writeInfo()
        print("")
        randomEvent.action(player)
    except Exception:
        logs.print("БАГ!!! Произошла проблема с картой: " + randomEvent.name)
    print("Случайное событие завершено.\n")


def intelligence(player):
    logs.print("Добро пожаловать на разведку!\n")

    allChaosCards = []
    for card in ChaosThePlayer.cards:
        allChaosCards.append(card)

    if len(allChaosCards) == 0:  # если у хаоса не осталось свободных карт О__о
        logs.print("Нечего разведывать.\n")
        return

    logs.print("Доступные варианты разведки:")
    logs.print("Короткая разведка: вы получите одну случайную карту и заберёте её на руки.")
    if len(allChaosCards) > 1:
        logs.print("Обычная разведка: вы получите две случайные карты и заберёте на руки любую из них.")
    if len(allChaosCards) > 2:
        logs.print("Длинная разведка: вы получите три случайные карты и заберёте на руки любую из них.")
    print("Случайные карты включают в себя все карты сестёр, локаций, оружия и артефактов, не принадлежащие игрокам.\n")

    if player == GuildThePlayer:  # для гильдии разведка дешевле
        lightIntCost = 5
        middleIntCost = 8
        hardIntCost = 10
    else:
        lightIntCost = 10
        middleIntCost = 16
        hardIntCost = 20

    while True:
        logs.print("У вас " + str(player.money) + " монет.")
        logs.print("На какую разведку вы отправитесь?")
        print("1 - короткая разведка. Стоимость: " + str(lightIntCost) + " монет.")
        if len(allChaosCards) > 1:
            print("2 - обычная разведка. Стоимость: " + str(middleIntCost) + " монет.")
        if len(allChaosCards) > 2:
            print("3 - длинная разведка. Стоимость: " + str(hardIntCost) + " монет.")
        print("Внимание! Если вы отправитесь на разведку не по карману, вас перенаправят на короткую разведку.")
        answer = input()
        if answer in ["1", "2", "3"]:
            match answer:
                # сначала проверяем, хватает ли нам денег на выбранную разведку и хватает ли карт
                case "1":
                    # на 1 у нас точно есть деньги
                    intType = 1
                case "2":
                    if player.money < middleIntCost:
                        intType = 1
                    else:
                        if len(allChaosCards) > 1:
                            intType = 2
                        else:
                            intType = 1
                case "3":
                    if player.money < hardIntCost:
                        intType = 1
                    else:
                        if len(allChaosCards) > 2:
                            intType = 3
                        else:  # ибо нефиг
                            intType = 1
                case _:
                    logs.print("Произошла ошибка в match-case в выборе способа разведки.")
                    break
            # если всё в порядке, идём на разведку
            print("В процессе разведки вы нашли это:\n")

            cardsToShow = []
            i = 1
            while i <= intType:
                tempCard = random.choice(allChaosCards)
                cardsToShow.append(tempCard)
                allChaosCards.remove(tempCard)
                i += 1

            # выводим список для выбора
            for tempCard in cardsToShow:
                logs.print("КАРТА №" + str(cardsToShow.index(tempCard) + 1))
                tempCard.writeInfo()
                logs.print("")

            while True:
                logs.print("Введите номер карты, которую хотите забрать.")
                cardIndex = logs.input()
                try:
                    if (int(cardIndex) - 1) < 0:  # чтобы не работало на индексе -1
                        raise Exception
                    newPlayerCard = cardsToShow[int(cardIndex) - 1]
                    logs.print("Карта выбрана: " + newPlayerCard.name)
                    break
                except Exception:
                    print("Некорректный ввод. Попробуйте ещё раз.")

            # теперь передаём карту игроку
            player.getCard(newPlayerCard, ChaosThePlayer)
            logs.print(newPlayerCard.name + " получено в процессе разведки игроком " + player.name + ".\n")
            break
        else:
            print("Некорректный ввод. Попробуйте ещё раз.")


# ЭТАП ХАОСА

def chaosCardPlay():
    i = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
    if i == 1 or i == 2:
        swapLocations(randomPlayablePlayer(), randomPlayablePlayer())
    if i == 3 or i == 4:
        swapWeapons(randomPlayablePlayer(), randomPlayablePlayer())
    if i == 5 or i == 6:
        swapArtefacts(randomPlayablePlayer(), randomPlayablePlayer())
    if i == 7:
        swapAllCards(randomPlayablePlayer(), randomPlayablePlayer())
    if i == 8:
        swapSisters(randomPlayablePlayer(), randomPlayablePlayer())
    return


def randomPlayablePlayer():
    return random.choice([VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer])


def randomPlayer():
    return random.choice([VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer, ChaosThePlayer])


def swapLocations(player1, player2):
    logs.print("\nХАОС: " + player1.name + " и " + player2.name + " поменяются локациями.")
    if player1 == player2:
        return
    locations1 = []
    locations2 = []
    for card1 in player1.cards:
        if card1.isLocation():
            locations1.append(card1)
    for card2 in player2.cards:
        if card2.isLocation():
            locations2.append(card2)

    for card in locations1:
        player2.getCard(card, player1)
    for card in locations2:
        player1.getCard(card, player2)

    logs.print("Обмен совершён.")


def swapSisters(player1, player2):
    logs.print("\nХАОС: " + player1.name + " и " + player2.name + " поменяются локациями.")
    if player1 == player2:
        return
    sisters1 = []
    sisters2 = []
    for card1 in player1.cards:
        if card1.isSister():
            sisters1.append(card1)
    for card2 in player2.cards:
        if card2.isSister():
            sisters2.append(card2)

    for card in sisters1:
        player2.getCard(card, player1)
    for card in sisters2:
        player1.getCard(card, player2)

    logs.print("Обмен совершён.")


def swapArtefacts(player1, player2):
    logs.print("\nХАОС: " + player1.name + " и " + player2.name + " поменяются артефактами.")
    if player1 == player2:
        return
    artefacts1 = []
    artefacts2 = []
    for card1 in player1.cards:
        if card1.isArtefact():
            artefacts1.append(card1)
    for card2 in player2.cards:
        if card2.isArtefact():
            artefacts2.append(card2)

    for card in artefacts1:
        player2.getCard(card, player1)
    for card in artefacts2:
        player1.getCard(card, player2)

    logs.print("Обмен совершён.")


def swapAllCards(player1, player2):
    logs.print("\nХАОС: " + player1.name + " и " + player2.name + " поменяются картами.")
    if player1 == player2:
        return
    cards1 = []
    cards2 = []
    for card1 in player1.cards:
        cards1.append(card1)
    for card2 in player2.cards:
        cards2.append(card2)

    for card in cards1:
        player2.getCard(card, player1)
    for card in cards2:
        player1.getCard(card, player2)

    logs.print("Обмен совершён.")
