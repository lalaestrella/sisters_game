from writelogs import logs


# ИГРОКИ

class Player:
    def __init__(self, name, influence, money, cards, fightStats, havingSisters, goal, specialTraits):
        self.name = name
        self.influence = influence
        self.money = money
        self.cards = cards
        self.fightStats = fightStats
        self.havingSisters = havingSisters
        self.goal = goal
        self.specialTraits = specialTraits
        self.isKidnapped = False

    def writeInfo(self):
        logs.print("\n=== " + self.name.upper() + " ===")
        logs.print("\n=== СТАТЫ ===\n")
        logs.print("Влияние: " + str(self.influence) + " очков (из них свободных: " + str(self.influenceToSold()) + ")")
        logs.print("Деньги: " + str(self.money) + " монет")
        self.fightStats.writeStats()
        if self.isQueen():
            logs.print("У Королевы нет своих статов, но она может использовать карту Войны для каждого боя.")

        logs.print("\nЧто нужно для победы:")
        logs.print(self.goal)

        logs.print("\nОсобенности:")
        logs.print(self.specialTraits)

        logs.print("\n=== КАРТЫ НА РУКАХ ===\n")
        self.writeInfoAboutSisters()
        self.writeInfoAboutLocations()
        self.writeInfoAboutCards()

        logs.print("\n=== КОНЕЦ ИНФОДАМПА ===\n")

    def writeInfoAboutSisters(self):
        logs.print("СЁСТРЫ: ")
        for card in self.cards:
            if card.isSister():
                card.writeInfo()
                logs.print("")

    def writeInfoAboutLocations(self):
        logs.print("ЛОКАЦИИ: ")
        for card in self.cards:
            if card.isLocation():
                card.writeInfo()
                logs.print("")

    def writeInfoAboutCards(self):
        logs.print("ОРУЖИЕ: ")
        for card in self.cards:
            if card.isWeapon():
                card.writeInfo()
                logs.print("")
        logs.print("АРТЕФАКТЫ: ")
        for card in self.cards:
            if card.isArtefact():
                card.writeInfo()
                logs.print("")

    def writeInfoIntoLogsOnly(self):
        logs.printtologs("\n===" + self.name + "===\n")
        logs.printtologs("\n=== СТАТЫ ===\n")
        logs.printtologs(
            "Влияние: " + str(self.influence) + " очков (из них свободных: " + str(self.influenceToSold()) + ")")
        logs.printtologs("Деньги: " + str(self.money) + " монет")
        self.fightStats.writeStatsToLogs()

        logs.printtologs("\n=== КАРТЫ НА РУКАХ ===\n")
        # пожалуйста, не пишите код так, это очень плохо
        logs.printtologs("СЁСТРЫ: ")
        for card in self.cards:
            if card.isSister():
                card.writeInfoToLogsOnly()
        logs.printtologs("ЛОКАЦИИ: ")
        for card in self.cards:
            if card.isLocation():
                card.writeInfoToLogsOnly()
        logs.printtologs("ОРУЖИЕ: ")
        for card in self.cards:
            if card.isWeapon():
                card.writeInfoToLogsOnly()
        logs.printtologs("АРТЕФАКТЫ: ")
        for card in self.cards:
            if card.isArtefact():
                card.writeInfoToLogsOnly()

        logs.printtologs("\n=== КОНЕЦ ИНФОДАМПА ===\n")

    def writeInfoAboutPublicCards(self):
        logs.print("ОРУЖИЕ: ")
        for card in self.cards:
            if card.isWeapon() and not card.isPrivate:
                card.writeInfo()
                logs.print("")
        logs.print("АРТЕФАКТЫ: ")
        for card in self.cards:
            if card.isArtefact() and not card.isPrivate:
                card.writeInfo()
                logs.print("")

    def isQueen(self):
        return False

    def isVictor(self):
        return False

    def isPlayable(self):
        return True

    def isHavingCard(self, card):
        return card in self.cards

    def influenceToSold(self):
        influenceToSold = self.influence
        for card in self.cards:
            if card.isLocation():
                influenceToSold -= card.influence
        return influenceToSold

    def loseInfluence(self, influenceLost, influenceGetter):
        if self.influenceToSold() >= influenceLost:
            self.influence -= influenceLost
            if influenceGetter.isPlayable():  # если получатель свободного влияния - игрок, то он всё получает
                influenceGetter.influence += influenceLost
                logs.print("Новое количество влияния " + influenceGetter.name + ": " + str(influenceGetter.influence)
                           + ", из них свободно " + str(influenceGetter.influenceToSold()))
            # если не игрок, то это Хаос, и он не должен получать влияние
            logs.print("Новое количество влияния " + self.name + ": " + str(self.influence) + ", из них свободно "
                       + str(self.influenceToSold()))

        else:  # придётся продавать здания
            if influenceGetter.isPlayable():  # если получатель свободного влияния - игрок, то он всё получает
                influenceGetter.influence += self.influenceToSold()
            # если не игрок, то это Хаос, и он не должен получать свободное влияние
            influenceToLose = influenceLost - self.influenceToSold()  # сколько нам останется добрать
            isDebtPaid = False
            self.influence -= self.influenceToSold()
            logs.print("Новое количество влияния " + self.name + ": " + str(self.influence) + ", из них свободно "
                       + str(self.influenceToSold()))
            logs.print("Новое количество влияния " + influenceGetter.name + ": " + str(influenceGetter.influence)
                       + ", из них свободно " + str(influenceGetter.influenceToSold()))
            logs.print("\nПередано всё свободное влияние, нужно передать ещё " + str(influenceToLose))
            logs.print(self.name + " передаст игроку " + influenceGetter.name + " часть своих зданий.\n")
            for card in self.cards:
                if card.isLocation():
                    influenceToLose -= card.influence
                    influenceGetter.getCard(card, self)
                    logs.print(influenceGetter.name + " получает " + card.name + ".")
                    logs.print(
                        "Новое количество влияния " + self.name + ": " + str(self.influence) + ", из них свободно "
                        + str(self.influenceToSold()))
                    logs.print(
                        "Новое количество влияния " + influenceGetter.name + ": " + str(influenceGetter.influence)
                        + ", из них свободно " + str(influenceGetter.influenceToSold()))
                    if influenceToLose >= 0:  # если долг выплачен, больше не перебираем карты
                        logs.print("\nДолг выплачен.")
                        isDebtPaid = True
                        break
            if not isDebtPaid:
                logs.print("\nДолг не выплачен, но влияние у должника кончилось.")
                logs.print("Новое количество влияния " + self.name + ": " + str(self.influence) + ", из них свободно "
                           + str(self.influenceToSold()))
                logs.print("Новое количество влияния " + influenceGetter.name + ": " + str(influenceGetter.influence)
                           + ", из них свободно " + str(influenceGetter.influenceToSold()))

    # Карту можно передать только от игрока к игроку. Все неприкаянные карты на начало игры принадлежат Хаосу
    def getCard(self, card, previousHolder):
        self.cards.append(card)
        previousHolder.cards.remove(card)

        # если артефакт, нужно произвести манипуляции (для артефактов, меняющих статы)
        if card.isArtefact():
            card.actionWhenGiven(newHolder=self, previousHolder=previousHolder)

        # меняем счётчики, если это подразумевает тип карты
        if card.isLocation():
            self.influence += card.influence
            previousHolder.influence -= card.influence
            if previousHolder.influence < 0:
                previousHolder.influence = 0
        if card.isSister():
            self.havingSisters += 1
            previousHolder.havingSisters -= 1
            # если передалась карта Королевы
            if card.name == "Война":
                if self.isQueen():
                    self.isKidnapped = False
                    logs.printtologs("Статус похищения Королевы сменился на False (не похищена).")
                    logs.print("КОРОЛЕВА ВЕРНУЛАСЬ ДОМОЙ!")
                if previousHolder.isQueen():
                    previousHolder.isKidnapped = True
                    logs.printtologs("Статус похищения Королевы сменился на True (похищена).")
                    logs.print("ПОХИЩЕНА КОРОЛЕВА!")

        logs.printtologs(
            "Карта " + card.name + " передана персонажу " + self.name + ". Предыдущий владелец: " + previousHolder.name)

    # найти владельца карты и забрать её себе
    def getTheCardFromAnyPlayer(self, card, Players):
        for player in Players:
            if player.isHavingCard(card):
                self.getCard(card, player)
                break

    # получить статы врага для драки
    # используется в виде
    # я.получитьСтатыВрагаДляДраки(мойВраг, егоОружие, егоСестра)
    # в т.ч. мб использовано в виде мойВраг.получитьСтатыВрагаДляДраки(я, моёОружие, мояСестра)
    # идея в том, что некоторые персонажи (Виктор, Королева) воздействуют на урон, наносимый им врагом
    # важно это предусмотреть и считать т.о. статы, опираясь на врага
    def getEnemyStatsForFight(self, enemy, weapon, sister):
        return FightStats(enemy.fightStats.force + weapon.fightStats.force + sister.fightStats.force,
                          enemy.fightStats.magic + weapon.fightStats.magic + sister.fightStats.magic,
                          enemy.fightStats.mind + weapon.fightStats.mind + sister.fightStats.mind)

    def winnerOfTheFight(self, myWeapon, mySister, enemy, enemyWeapon, enemySister):
        # считаем статы от врага
        myStats = enemy.getEnemyStatsForFight(self, myWeapon, mySister)
        logs.print("Финальные статы " + self.name)
        myStats.writeStats()
        enemyStats = self.getEnemyStatsForFight(enemy, enemyWeapon, enemySister)
        logs.print("Финальные статы " + enemy.name)
        enemyStats.writeStats()
        # для победы нужно превзойти противника в двух статах из трёх
        if myStats.force > enemyStats.force and myStats.magic > enemyStats.magic:
            return self
        if myStats.force < enemyStats.force and myStats.magic < enemyStats.magic:
            return enemy
        if myStats.force > enemyStats.force and myStats.mind > enemyStats.mind:
            return self
        if myStats.force < enemyStats.force and myStats.mind < enemyStats.mind:
            return enemy
        if myStats.magic > enemyStats.magic and myStats.mind > enemyStats.mind:
            return self
        if myStats.magic < enemyStats.magic and myStats.mind < enemyStats.mind:
            return enemy
        # если условия не соблюдены - ничья
        return 0

    def amIWinnerOfTheFightWithNpc(self, weapon, sister, enemyStats, enemyName):
        logs.print("Финальные статы " + enemyName)
        tempEnemyStats = FightStats(enemyStats.force, enemyStats.magic, enemyStats.mind)
        if self.isVictor():
            tempEnemyStats.magic = 0
        tempEnemyStats.writeStats()
        myStats = FightStats(self.fightStats.force + weapon.fightStats.force + sister.fightStats.force,
                             self.fightStats.magic + weapon.fightStats.magic + sister.fightStats.magic,
                             self.fightStats.mind + weapon.fightStats.mind + sister.fightStats.mind)
        logs.print("Финальные статы " + self.name)
        myStats.writeStats()
        # для победы нужно превзойти противника в двух статах из трёх
        if myStats.force > enemyStats.force and myStats.magic > enemyStats.magic:
            return True
        if myStats.force < enemyStats.force and myStats.magic < enemyStats.magic:
            return False
        if myStats.force > enemyStats.force and myStats.mind > enemyStats.mind:
            return True
        if myStats.force < enemyStats.force and myStats.mind < enemyStats.mind:
            return False
        if myStats.magic > enemyStats.magic and myStats.mind > enemyStats.mind:
            return True
        if myStats.magic < enemyStats.magic and myStats.mind < enemyStats.mind:
            return False
        # если условия не соблюдены - ничья. в данном случае считается за проигрыш
        return False


class Victor(Player):
    # Виктор поглощает любую магию, кроме магии сестёр
    def getEnemyStatsForFight(self, enemy, weapon, sister):
        return FightStats(enemy.fightStats.force + weapon.fightStats.force + sister.fightStats.force,
                          sister.fightStats.magic,
                          enemy.fightStats.mind + weapon.fightStats.mind + sister.fightStats.mind)

    def isVictor(self):
        return True


class Queen(Player):
    def __init__(self, name, influence, money, cards, fightStats, havingSisters, goal, specialTraits):
        super().__init__(name, influence, money, cards, fightStats, havingSisters, goal, specialTraits)
        self.isKidnapped = False  # при инициации персонажа Королева всегда у себя на руках

    def isQueen(self):
        return True

    # Королева невосприимчива к урону от сестёр
    def getEnemyStatsForFight(self, enemy, weapon, sister):
        return FightStats(enemy.fightStats.force + weapon.fightStats.force,
                          enemy.fightStats.magic + weapon.fightStats.magic,
                          enemy.fightStats.mind + weapon.fightStats.mind)


class Chaos(Player):
    def isPlayable(self):
        return False


# КАРТЫ НА РУКАХ

class Card:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.isPrivate = True
        self.isExpired = False

    def makePublic(self):
        self.isPrivate = False

    def makePrivate(self):
        self.isPrivate = True

    def makeExpired(self):
        self.isExpired = True

    def makeUnexpired(self):
        self.isExpired = False

    def writeInfo(self):
        logs.print("Название: " + self.name)
        logs.print("Описание: " + self.description)

    def writeInfoToLogsOnly(self):
        logs.printtologs("Название: " + self.name)
        logs.printtologs("Описание: " + self.description)

    def isSister(self):
        return False

    def isWeapon(self):
        return False

    def isLocation(self):
        return False

    def isArtefact(self):
        return False


class LocationCard(Card):
    def __init__(self, name, description, influence):
        super().__init__(name, description)
        self.influence = influence
        self.isPrivate = False  # все локации по умолчанию публичные

    def makeExpired(self):
        self.isExpired = False  # локация не может протухнуть

    def writeInfo(self):
        super().writeInfo()
        logs.print("Стоимость: " + str(self.influence) + " очков влияния")

    def writeInfoToLogsOnly(self):
        super().writeInfoToLogsOnly()
        logs.printtologs("Стоимость: " + str(self.influence) + " очков влияния")

    def isLocation(self):
        return True

    def action(self, player):
        logs.print("Выполняется функция родительского класса. Это баг, название локации: " + self.name)


class SisterCard(Card):
    def __init__(self, name, description, fightStats):
        super().__init__(name, description)
        self.fightStats = fightStats

    def writeInfo(self):
        super().writeInfo()
        self.fightStats.writeStats()

    def writeInfoToLogsOnly(self):
        super().writeInfoToLogsOnly()
        self.fightStats.writeStatsToLogs()

    def isSister(self):
        return True


class Weapon(Card):
    def __init__(self, name, description, fightStats, cost):
        super().__init__(name, description)
        self.fightStats = fightStats
        self.cost = cost

    def writeInfo(self):
        super().writeInfo()
        logs.print("Стоимость: " + str(self.cost) + " монет")
        self.fightStats.writeStats()

    def writeInfoToLogsOnly(self):
        super().writeInfoToLogsOnly()
        logs.printtologs("Стоимость: " + str(self.cost) + " монет")
        self.fightStats.writeStatsToLogs()

    def isWeapon(self):
        return True


class Artefact(Card):
    def __init__(self, name, description, cost):
        super().__init__(name, description)
        self.cost = cost

    def writeInfo(self):
        super().writeInfo()
        logs.print("Стоимость: " + str(self.cost) + " монет")

    def writeInfoToLogsOnly(self):
        super().writeInfoToLogsOnly()
        logs.printtologs("Стоимость: " + str(self.cost) + " монет")

    def actionWhenGiven(self, newHolder, previousHolder):
        return

    def isArtefact(self):
        return True


# СТАТЫ

class FightStats:
    def __init__(self, force, magic, mind):
        self.force = force
        self.magic = magic
        self.mind = mind

    def writeStats(self):
        logs.print("Сила: " + str(self.force) + ". Магия: " + str(self.magic) + ". Разум: " + str(self.mind) + ".")

    def writeStatsToLogs(self):
        logs.printtologs(
            "Сила: " + str(self.force) + ". Магия: " + str(self.magic) + ". Разум: " + str(self.mind) + ".")


# КАРТЫ СОБЫТИЙ

class Event:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class RandomEvent(Event):
    def __init__(self, name, description, actionDesc):
        super().__init__(name, description)
        self.actionDesc = actionDesc

    def writeInfo(self):
        logs.print(self.name.upper())
        logs.print(self.description)
        logs.print(self.actionDesc)

    def action(self, player):
        logs.print("Вызвана родительская функция карты случайного события. Это баг, так быть не должно.")
        return


class ChaosEvent(Event):
    def __init__(self, name, description):
        super().__init__(name, description)
