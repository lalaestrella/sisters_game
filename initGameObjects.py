import random

from gameObjectsClasses import Artefact, FightStats, SisterCard, Player, Victor, LocationCard, Queen, Weapon, \
    RandomEvent
from writelogs import logs

# ОБЪЯВЛЕНИЕ КОМПАСА, СЕСТЁР, СТАРТОВЫХ ЛОКАЦИЙ И ИГРОКОВ

# КОМПАС
CompassTheCard = Artefact("Компас Ведьмы",
                          "Костяной компас с четырьмя стрелками, указывающими на расположение Сестёр.",
                          30)

CompassTheCard.makePublic()  # все знают о существовании компаса и о его владельце на начало игры

# СЁСТРЫ
# Примечание: сёстры всегда приватные, за них идёт особый механизм ведения боя, они не раскрываются в картах противника
WarTheSister = SisterCard("Война",
                          "Красивая рыжая девушка, за любовь которой нужно сражаться."
                          "\nЭту карту должна иметь на руках Королева, чтобы победить.",
                          FightStats(force=1, magic=5, mind=4))

PlagueTheSister = SisterCard("Чума",
                             "Её хобби - собирать безделицы, привезённые моряками с далёких земель.",
                             FightStats(force=3, magic=4, mind=3))

DeathTheSister = SisterCard("Смерть",
                            "Маленькая девочка с большими голубыми глазами и мёртвым голосом.",
                            FightStats(force=1, magic=8, mind=1))

HungerTheSister = SisterCard("Голод",
                             "Если её разозлить, она сожжёт ваши посевы, и вам будет нечего есть.",
                             FightStats(force=4, magic=4, mind=2))

SisterCards = [WarTheSister, PlagueTheSister, DeathTheSister, HungerTheSister]


# СТАРТОВЫЕ ЛОКАЦИИ
# все локации по умолчанию публичные
class Bordel(LocationCard):
    def action(self, player):
        player.money += 2
        logs.print(
            "Бордель принёс вам 2 монеты. Теперь у вас " + str(player.money) + " монет.")


BordelTheCard = Bordel("Бордель",
                       "Каждый ход бордель приносит своему владельцу 2 монеты.",
                       influence=2)


class WitchShop(LocationCard):
    def action(self, player):
        logs.printtologs("Лавка ведьмы не даёт никаких плюшек на старте игры.")


WitchShopTheCard = WitchShop("Лавка Ведьмы",
                             "Владелец лавки ведьмы получает скидку в 5 монет на артефакты и по 5 монет за каждый "
                             "проданный артефакт.",
                             influence=2)


class Tavern(LocationCard):
    def action(self, player):
        player.money += 1
        logs.print(
            "Таверна принесла вам 1 монету. Теперь у вас " + str(player.money) + " монет.")


TavernTheCard = Tavern("Таверна",
                       "Каждый ход таверна приносит своему владельцу 1 монету.",
                       influence=1)


class Palace(LocationCard):
    def action(self, player):
        if player.money >= 1:
            print("Желаете обменять 1 монету на 1 очко влияния? (Дворец)")
            while True:
                print("Введите ответ: 1 - да, 0 - нет.")
                answer = input()
                if answer == "1":
                    player.money -= 1
                    player.influence += 1
                    logs.print(
                        "Обмен совершён. Теперь у вас " + str(player.money) + " монет и "
                        + str(player.influence) + " очков влияния.")
                    break
                else:
                    if answer == "0":
                        logs.print(
                            "Обмен не совершён. У вас " + str(player.money) + " монет и "
                            + str(player.influence) + " очков влияния.")
                        break
                    else:
                        print("Некорректный ввод. Попробуйте ещё раз.")
        else:
            logs.print("У вас нет денег, чтобы обменять их на очки влияния во Дворце.")


PalaceTheCard = Palace("Дворец",
                       "Каждый ход владелец дворца может отдать 1 монету, чтобы получить 1 очко влияния.",
                       influence=3)

# ИГРОКИ
VictorThePlayer = Victor(name="Виктор Кастелли",
                         influence=11,  # 9 + 2 за бордель
                         money=20,
                         cards=[DeathTheSister, BordelTheCard],
                         fightStats=FightStats(force=3, magic=0, mind=4),
                         havingSisters=1,
                         goal="Все сёстры на руках Виктора или Джулиана, компас у Виктора или Королевы.",
                         specialTraits="В бою вы подавляете любую магию, кроме магии сестёр.")

JulianThePlayer = Player(name="Джулиан Медичи",
                         influence=3,  # 1 + 2 за лавку ведьмы
                         money=8,
                         cards=[HungerTheSister, CompassTheCard, WitchShopTheCard],
                         fightStats=FightStats(force=2, magic=0, mind=6),
                         havingSisters=1,
                         goal="Все сёстры на руках Виктора или Джулиана, компас у Джулиана или Гильдии.",
                         specialTraits="Вы достаёте сразу три карты случайных событий и можете выбрать из них одну.")

GuildThePlayer = Player(name="Гильдия Разбойников",
                        influence=9,  # 8 + 1 за таверну
                        money=5,
                        cards=[TavernTheCard],
                        fightStats=FightStats(force=4, magic=2, mind=2),
                        havingSisters=0,
                        goal="Набрать 30 очков влияния, иметь на руках одну любую сестру.\nВнимание: если у вас на "
                             "руках будет 4 сестры, победит Хаос. Если и у вас, и у Королевы будет по 30 очков "
                             "влияния, победит Хаос.",
                        specialTraits="При продаже предметов (оружия и артефактов) вы получаете их полную стоимость.\n"
                                      "Каждый ход перед продажей и покупкой вы получаете случайную украденную карту.\n"
                                      "У вас есть скидки на разведку.")

QueenThePlayer = Queen(name="Кровавая Королева",
                       influence=15,  # 12 + 3 за дворец
                       money=10,
                       cards=[WarTheSister, PalaceTheCard],
                       fightStats=FightStats(force=0, magic=0, mind=0),  # все боевые статы - из карты сестры
                       havingSisters=1,
                       goal="Набрать 30 очков влияния, иметь на руках Войну.\nВнимание: если у вас на руках будет 4 "
                            "сестры, победит Хаос. Если и у вас, и у Гильдии будет по 30 очков влияния, победит Хаос.",
                       specialTraits="Если у вас украдут карту Войны (она же - карта вашего персонажа), вы не сможете "
                                     "ходить, пока не получите карту Войны обратно.\nВы невосприимчивы к урону от "
                                     "сестёр.")


# ОБЪЯВЛЕНИЕ ЛОКАЦИЙ
class WeaponShop(LocationCard):
    def action(self, player):
        logs.printtologs("Оружейная лавка не даёт никаких плюшек на старте игры.")


WeaponShopTheCard = WeaponShop("Оружейная лавка",
                               "Владелец оружейной лавки получает скидку в 2 монеты на оружие и по 2 монеты за каждое "
                               "проданное оружие.",
                               influence=2)


class Hospital(LocationCard):
    def action(self, player):
        if player.isHavingCard(PlagueTheSister):
            player.influence += 1
            logs.print(
                "Больница принесла вам 1 очко влияния. Теперь у вас " + str(player.influence) + " очков влияния.")


HospitalTheCard = Hospital("Больница",
                           "Владелец больницы получает 1 очко влияния, если в начале хода у него на руках есть карта "
                           "Чумы.",
                           influence=2)


class Bank(LocationCard):
    def action(self, player):
        for player1 in [VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer]:
            if player1 != player:
                if player1.money > 0:
                    player1.money -= 1
                    player.money += 1
                    logs.print(player1.name + " отдал 1 монету в банк.")
                else:
                    logs.print(player1.name + " объявлен банкротом.")
        logs.print("Банк собрал монеты у игроков. Теперь у вас " + str(player.money) + " монет.")


BankTheCard = Bank("Банк",
                   "Владелец банка получает по одной монете от каждого игрока в начале своего хода.",
                   influence=3)


class Church(LocationCard):
    def action(self, player):
        if player.isHavingCard(BibleTheCard):
            player.influence += 1
            logs.print(
                "Церковь принесла вам 1 очко влияния. Теперь у вас " + str(player.influence) + " очков влияния.")
        if player.havingSisters == 0:
            player.money += 10
            logs.print(
                "Церковь принесла вам 10 монет. Теперь у вас " + str(player.money) + " монет.")


ChurchTheCard = Church("Церковь",
                       "Владелец церкви получает 1 очко влияния, если в начале хода у него на руках есть карта "
                       "Библии. \nВладелец церкви получает 10 монет, если у него нет ни одной карты сестры.",
                       influence=3)


class Barracks(LocationCard):
    def action(self, player):
        if ChaosThePlayer.influence < 10:
            player.influence += 1
            logs.print(
                "Казарма принесла вам 1 очко влияния. Теперь у вас " + str(player.influence) + " очков влияния.")


BarracksTheCard = Barracks("Казарма",
                           "Владелец казармы получает 1 очко влияния, если у Хаоса меньше 10 очков влияния.",
                           influence=2)


class University(LocationCard):
    def action(self, player):
        if player.influenceToSold() >= 1:
            print("Желаете заплатить 1 очко влияния, чтобы поменяться картами с другим игроком?")
            while True:
                print("Введите ответ: 1 - да, 0 - нет.")
                answer = input()
                if answer == "1":
                    player.influence -= 1
                    while True:
                        logs.print("С кем будете меняться?")
                        print("1 - Виктор Кастелли")
                        print("2 - Джулиан Медичи")
                        print("3 - Гильдия Разбойников")
                        print("4 - Кровавая Королева")
                        answer2 = input()
                        if answer2 in ["1", "2", "3", "4"]:
                            match answer2:
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
                                    logs.print(
                                        "Произошла ошибка в match-case в выборе противника для универского свопа")
                                    break
                            if player == defPlayer:
                                logs.print("Вы не можете меняться сами с собой.")
                                continue
                            else:
                                # если всё в порядке, инициируем обмен!
                                swapWeapons(player, defPlayer, isChaos=False)
                                return
                        else:
                            print("Некорректный ввод. Попробуйте ещё раз.")
                else:
                    if answer == "0":
                        logs.print(
                            "Обмен не совершён. У вас " + str(player.influence) + " очков влияния.")
                        break
                    else:
                        print("Некорректный ввод. Попробуйте ещё раз.")
        else:
            logs.print("У вас нет очков влияния, чтобы совершить обмен с помощью Университета.")


UniversityTheCard = University("Университет",
                               "Владелец университета может отдать очко влияния, чтобы поменяться картами оружия с "
                               "другим игроком.",
                               influence=3)


class PictureGallery(LocationCard):
    def action(self, player):
        logs.printtologs("Картинная галерея не даёт никаких плюшек на старте игры.")


PictureGalleryTheCard = PictureGallery("Картинная галерея",
                                       "Картинная галерея делает своего владельца влиятельным человеком.",
                                       influence=5)


class Farm(LocationCard):
    def action(self, player):
        newMoney = random.choice([1, 2, 3])
        player.money += newMoney
        logs.print(
            "Ферма принесла вам " + str(newMoney) + " монет. Теперь у вас " + str(player.money) + " монет.")


FarmTheCard = Farm("Ферма",
                   "Каждый ход ферма приносит своему владельцу от 1 до 3 монет.",
                   influence=2)

# ОБЪЯВЛЕНИЕ АРТЕФАКТОВ

# артефактов в игре всего 6 штук, включая компас

GloveTheCard = Artefact("Перчатка дуэлянта",
                        "Владелец перчатки не теряет очки влияния, когда проигрывает в битвах.",
                        20)

EyeTheCard = Artefact("Глаз древнего бога",
                      "Вы видите все карты игроков, открытые и закрытые.",
                      25)


class FieryCloak(Artefact):
    def actionWhenGiven(self, newHolder, previousHolder):
        newHolder.fightStats = FightStats(newHolder.fightStats.force + 5, newHolder.fightStats.magic,
                                          newHolder.fightStats.mind)
        if newHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStats()
            self.makePublic()  # такое не спрячешь
        else:
            logs.printtologs("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStatsToLogs()
        previousHolder.fightStats = FightStats(previousHolder.fightStats.force - 5, previousHolder.fightStats.magic,
                                               previousHolder.fightStats.mind)
        if previousHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStats()
        else:
            logs.printtologs("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStatsToLogs()
        print("")


FieryCloakTheCard = FieryCloak("Огненный плащ",
                               "Сила владельца увеличивается на 5.",
                               30)


class Wiki(Artefact):
    def actionWhenGiven(self, newHolder, previousHolder):
        newHolder.fightStats = FightStats(newHolder.fightStats.force, newHolder.fightStats.magic,
                                          newHolder.fightStats.mind + 5)
        if newHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStats()
            self.makePublic()  # такое не спрячешь
        else:
            logs.printtologs("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStatsToLogs()
        previousHolder.fightStats = FightStats(previousHolder.fightStats.force, previousHolder.fightStats.magic,
                                               previousHolder.fightStats.mind - 5)
        if previousHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStats()
        else:
            logs.printtologs("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStatsToLogs()
        print("")


WikiTheCard = Wiki("Полное собрание книг Виконта Тедди",
                   "Разум владельца увеличивается на 5.",
                   30)


class FairyDust(Artefact):
    def actionWhenGiven(self, newHolder, previousHolder):
        newHolder.fightStats = FightStats(newHolder.fightStats.force, newHolder.fightStats.magic + 5,
                                          newHolder.fightStats.mind)
        if newHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStats()
            self.makePublic()  # такое не спрячешь
        else:
            logs.printtologs("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStatsToLogs()
        previousHolder.fightStats = FightStats(previousHolder.fightStats.force, previousHolder.fightStats.magic - 5,
                                               previousHolder.fightStats.mind)
        if previousHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStats()
        else:
            logs.printtologs("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStatsToLogs()
        print("")


FairyDustTheCard = FairyDust("Пыльца феи",
                             "Магия владельца увеличивается на 5.",
                             30)


class Ring(Artefact):
    def actionWhenGiven(self, newHolder, previousHolder):
        newHolder.fightStats = FightStats(newHolder.fightStats.force + 2, newHolder.fightStats.magic + 2,
                                          newHolder.fightStats.mind + 2)
        if newHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStats()
            self.makePublic()  # такое не спрячешь
        else:
            logs.printtologs("Новые характеристики персонажа " + newHolder.name)
            newHolder.fightStats.writeStatsToLogs()
        previousHolder.fightStats = FightStats(previousHolder.fightStats.force - 2, previousHolder.fightStats.magic - 2,
                                               previousHolder.fightStats.mind - 2)
        if previousHolder != ChaosThePlayer:
            logs.print("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStats()
        else:
            logs.printtologs("Новые характеристики персонажа " + previousHolder.name)
            previousHolder.fightStats.writeStatsToLogs()
        print("")


RingTheCard = Ring("Кольцо всевластия",
                   "Все характеристики владельца увеличиваются на 2.",
                   35)

# ОБЪЯВЛЕНИЕ ОРУЖИЯ

# слабое оружие (по 3 штуки на каждую стату, урон 3)

LittleAxeTheCard = Weapon("Маленький топорик",
                          "Этот маленький топорик может причинить большие проблемы.",
                          fightStats=FightStats(force=3, magic=0, mind=0),
                          cost=4)

ThiefKnifeTheCard = Weapon("Нож карманника",
                           "Маленький и незаметный ножик.",
                           fightStats=FightStats(force=3, magic=0, mind=0),
                           cost=5)

HorseShoeTheCard = Weapon("Метательная подкова",
                          "Удача в бою будет на стороне метателя!",
                          fightStats=FightStats(force=3, magic=0, mind=0),
                          cost=4)

MagicWandTheCard = Weapon("Волшебная палочка",
                          "То, что поможет вам в магии.",
                          fightStats=FightStats(force=0, magic=3, mind=0),
                          cost=5)

CharmedKnifeTheCard = Weapon("Заколдованный нож",
                             "Этот нож может то, чего не могут ваши руки!",
                             fightStats=FightStats(force=2, magic=3, mind=0),
                             cost=6)

LuckyAceTheCard = Weapon("Счастливый туз",
                         "С этой картой вселенная вам подыгрывает.",
                         fightStats=FightStats(force=0, magic=3, mind=0),
                         cost=3)

RunesBookTheCard = Weapon("Толкователь рун",
                          "Научитесь читать знаки судьбы... или попросту ударьте кого-нибудь книгой по голове!",
                          fightStats=FightStats(force=1, magic=0, mind=3),
                          cost=5)

SmartRatTheCard = Weapon("Разумная крыса",
                         "С таким помощником вам по зубам даже рецепт рататуя.",
                         fightStats=FightStats(force=0, magic=0, mind=3),
                         cost=4)

StupidTranslatorTheCard = Weapon("Переводчик с дебильного",
                                 "Научитесь говорить на языке черни.",
                                 fightStats=FightStats(force=0, magic=0, mind=3),
                                 cost=4)

# среднее оружие (по 2шт на стату)

BigAxeTheCard = Weapon("Большой топор",
                       "Большим топором можно проламывать большие дыры.",
                       fightStats=FightStats(force=5, magic=0, mind=0),
                       cost=8)

CourtSwordTheCard = Weapon("Дуэльная шпага",
                           "Продаётся в комплекте с перчаткой.",
                           fightStats=FightStats(force=5, magic=0, mind=0),
                           cost=9)

DoctorsCloakTheCard = Weapon("Плащ доктора Фаустуса",
                             "Этот странный доктор научил свой плащ драться с врагами и обнимать друзей.",
                             fightStats=FightStats(force=0, magic=5, mind=0),
                             cost=9)

HowToMeetDevilTheCard = Weapon('Самоучитель "Вызов дьявола для чайников"',
                               "Вам понадобятся только мел, свечи и базовое знание латыни.",
                               fightStats=FightStats(force=1, magic=5, mind=0),
                               cost=8)

BibleTheCard = Weapon("Библия",
                      "Впечатлите противника своей мудростью, и он сам подставит под ваш удар вторую щёку.",
                      fightStats=FightStats(force=2, magic=0, mind=5),
                      cost=10)

MasterKeyTheCard = Weapon("Отмычка",
                          "Взломайте мозги своего противника.",
                          fightStats=FightStats(force=0, magic=0, mind=5),
                          cost=8)

# сильное оружие (по 1шт на стату)

SwordTheCard = Weapon("Меч из дамасской стали",
                      "Острый и лёгкий, этот меч просто идеален для сражений.",
                      fightStats=FightStats(force=9, magic=0, mind=0),
                      cost=15)

DruidStaffTheCard = Weapon("Посох друида",
                           "Этот посох способен пробудить древнейшую магию.",
                           fightStats=FightStats(force=1, magic=8, mind=0),
                           cost=14)

CrownOfMadnessTheCard = Weapon("Корона безумия",
                               "Надев эту корону, вы станете гением... или безумцем!",
                               fightStats=FightStats(force=0, magic=1, mind=8),
                               cost=12)

# вундервафли - по 1шт на стату

IceSwordTheCard = Weapon("Ледяной меч",
                         "О силе этого меча ходят легенды среди живых и среди мёртвых.",
                         fightStats=FightStats(force=15, magic=2, mind=0),
                         cost=30)

ScytheOfDeathTheCard = Weapon("Коса смерти",
                              "Эта невероятная коса уничтожает всё живое на своём пути.",
                              fightStats=FightStats(force=2, magic=15, mind=0),
                              cost=30)

PortraitOfHeleneTheCard = Weapon("Портрет Елены Троянской",
                                 "Такая красота сведёт с ума кого угодно, даже саму Елену.",
                                 fightStats=FightStats(force=0, magic=2, mind=14),
                                 cost=30)

# смешное оружие (по 1 шт на каждую стату)

HobnailTheCard = Weapon("Старый гвоздь",
                        "Им тоже можно поцарапать.",
                        fightStats=FightStats(force=1, magic=0, mind=0),
                        cost=1)

MagicianHandkerchiefTheCard = Weapon("Платок фокусника",
                                     "Говорят, на нём ещё остались следы магии.",
                                     fightStats=FightStats(force=0, magic=1, mind=0),
                                     cost=1)

CookieTheCard = Weapon("Печенье с предсказанием",
                       "Не стоит недооценивать силу морального эффекта.",
                       fightStats=FightStats(force=0, magic=0, mind=1),
                       cost=1)

# ОБЪЯВЛЕНИЕ ХАОСА И ПУСТЫХ КАРТ

EmptySister = SisterCard(name="Без сестры", description="Этот персонаж сражается один.", fightStats=FightStats(0, 0, 0))
EmptyWeapon = Weapon(name="Без оружия", description="Этот персонаж сражается без оружия.",
                     fightStats=FightStats(0, 0, 0), cost=0)

ChaosThePlayer = Player(name="ПЕРВОЗДАННЫЙ ХАОС",
                        influence=22,
                        money=0,
                        cards=[PlagueTheSister,  # Чума
                               GloveTheCard, EyeTheCard, FieryCloakTheCard, WikiTheCard, FairyDustTheCard,  # артефакты
                               RingTheCard,
                               WeaponShopTheCard, HospitalTheCard, BankTheCard, ChurchTheCard,  # локации
                               BarracksTheCard, UniversityTheCard, PictureGalleryTheCard, FarmTheCard,
                               LittleAxeTheCard, ScytheOfDeathTheCard, BigAxeTheCard, ThiefKnifeTheCard,  # оружие
                               MagicWandTheCard, CrownOfMadnessTheCard, CookieTheCard, HorseShoeTheCard,
                               CharmedKnifeTheCard, LuckyAceTheCard, RunesBookTheCard, SmartRatTheCard,
                               StupidTranslatorTheCard, CourtSwordTheCard, PortraitOfHeleneTheCard,
                               MagicianHandkerchiefTheCard, HobnailTheCard, IceSwordTheCard, SwordTheCard,
                               DruidStaffTheCard, DoctorsCloakTheCard, HowToMeetDevilTheCard, BibleTheCard,
                               MasterKeyTheCard],
                        fightStats=FightStats(force=7, magic=7, mind=7),  # все статы - от артефактов
                        havingSisters=1,
                        goal="Набрать 30 очков влияния ИЛИ и у Гильдии, и у Королевы 30 очков влияния\n"
                             "ИЛИ Королева собрала 4 сестры ИЛИ Гильдия собрала 4 сестры.",
                        specialTraits="Неигровой персонаж, способный, однако, победить в игре.")


# ОБЪЯВЛЕНИЕ КАРТ РАНДОМА

class Herald(RandomEvent):
    def action(self, player):
        for card in player.cards:
            card.makePublic()
        logs.print("Все карты на ваших руках теперь известны.\n")


HeraldTheEvent = Herald("Глашатай Джонни",
                        "Глашатай Джонни раструбил всем обо всём.",
                        "Все карты на ваших руках становятся открытыми.")


class EvilWitch(RandomEvent):
    def action(self, player):
        if fightWithNPC(player, FightStats(force=3, magic=9, mind=3), self):
            logs.print("\nВы одолели ведьму.\n")
        else:
            for card in player.cards:
                if card.isArtefact():
                    ChaosThePlayer.getCard(card, player)
                    card.makePrivate()  # карта теперь не засвечена
            logs.print("\nВы не одолели ведьму и потеряли все артефакты.\n")


EvilWitchTheEvent = EvilWitch("Злая ведьма Анастазия",
                              "Анастазия считает, что не все достойны магии.",
                              "Победите Анастазию или потеряйте все свои карты артефактов.")


class Alex(RandomEvent):
    def action(self, player):
        playerToFight = ChaosThePlayer  # на всякий случай. хаос всегда проиграет, но вообще трэш
        if QueenThePlayer.isKidnapped:
            for player1 in [VictorThePlayer, JulianThePlayer, GuildThePlayer]:
                if player1.isHavingCard(WarTheSister):
                    playerToFight = player1

            if fightWithNPC(playerToFight, FightStats(force=6, magic=0, mind=7), self):
                logs.print("\nВы победили принца Александра. Карта Войны остаётся у вас.\n")
            else:
                logs.print("\nВы не смогли победить принца Александра. Королева теперь свободна.\n")
                QueenThePlayer.getCard(WarTheSister, playerToFight)
        else:
            logs.print("Королева не похищена. Принц Александр уехал обратно во дворец.\n")


AlexTheEvent = Alex("Принц Александр",
                    "Принц Александр отправился спасать свою королеву!",
                    "Если королева в беде, её тюремщику придётся сразиться с принцем.")


class James(RandomEvent):
    def action(self, player):
        playerToFight = ChaosThePlayer  # на всякий случай. хаос всегда проиграет, но вообще трэш
        if QueenThePlayer.isKidnapped:
            for player1 in [VictorThePlayer, JulianThePlayer, GuildThePlayer]:
                if player1.isHavingCard(WarTheSister):
                    playerToFight = player1

            if fightWithNPC(playerToFight, FightStats(force=8, magic=0, mind=5), self):
                logs.print("\nВы победили принца Джеймса. Карта Войны остаётся у вас.\n")
            else:
                logs.print("\nВы не смогли победить принца Джеймса. Королева теперь свободна.\n")
                QueenThePlayer.getCard(WarTheSister, playerToFight)
        else:
            logs.print("Королева не похищена. Принц Джеймс уехал обратно во дворец.\n")


JamesTheEvent = James("Принц Джеймс",
                      "Принц Джеймс отправился спасать свою королеву!",
                      "Если королева в беде, её тюремщику придётся сразиться с принцем.")


class Margaret(RandomEvent):
    def action(self, player):
        if QueenThePlayer.isKidnapped and player.isHavingCard(WarTheSister):
            player.money += 10
            logs.print("Вы получили 10 монет от маркизы Маргариты. Всего монет: "
                       + str(player.money) + "\n")
        else:
            if player.isQueen():
                player.influence += 2
                logs.print("Вы получили 2 очка влияния от маркизы Маргариты. Всего влияния: "
                           + str(player.influence) + "\n")
            else:
                logs.print("Вы не заинтересовали маркизу, её экипаж проехал мимо.\n")


MargaretTheEvent = Margaret("Маркиза Маргарита",
                            "Маркиза плетёт интригу против новой королевы. Или с ней?",
                            "Если у вас есть карта Войны и вы не Королева, получите 10 монет."
                            "\nЕсли вы - Королева, получите 2 очка влияния.")


class EndOfTheRainbow(RandomEvent):
    def action(self, player):
        player.money += 30
        logs.print("Вы нашли 30 монет на конце радуги. Всего монет: "
                   + str(player.money) + "\n")


EndOfTheRainbowTheEvent = EndOfTheRainbow("Конец радуги",
                                          "Вы обнаружили горшок с золотом.",
                                          "Получите 30 монет.")


class DonReggiani(RandomEvent):
    def action(self, player):
        player.money += 15
        logs.print("Вы получили 15 монет. Всего монет: " + str(player.money))
        if not player.isHavingCard(WeaponShopTheCard):
            player.getTheCardFromAnyPlayer(WeaponShopTheCard, [VictorThePlayer, JulianThePlayer, GuildThePlayer,
                                                               QueenThePlayer, ChaosThePlayer])
        logs.print("Новый владелец Оружейной лавки: " + player.name + "\n")


DonReggianiTheEvent = DonReggiani("Дон Реджани",
                                  "Вы выпили с доном Реджани, и он переписал Оружейную лавку на вас.",
                                  "Получите 15 монет и Оружейную лавку.")


class InquisitorGottlieb(RandomEvent):
    def action(self, player):
        players = [VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer, ChaosThePlayer]
        if not VictorThePlayer.isHavingCard(DeathTheSister):
            VictorThePlayer.getTheCardFromAnyPlayer(DeathTheSister, players)
            logs.print("Новый владелец карты " + DeathTheSister.name + ": " + VictorThePlayer.name)
        if not JulianThePlayer.isHavingCard(HungerTheSister):
            JulianThePlayer.getTheCardFromAnyPlayer(HungerTheSister, players)
            logs.print("Новый владелец карты " + HungerTheSister.name + ": " + JulianThePlayer.name)
        if not QueenThePlayer.isHavingCard(WarTheSister):
            QueenThePlayer.getTheCardFromAnyPlayer(WarTheSister, players)
            logs.print("Новый владелец карты " + WarTheSister.name + ": " + QueenThePlayer.name)
        if not ChaosThePlayer.isHavingCard(PlagueTheSister):
            ChaosThePlayer.getTheCardFromAnyPlayer(PlagueTheSister, players)
            logs.print("Новый владелец карты " + PlagueTheSister.name + ": " + ChaosThePlayer.name)
        logs.print("")


InquisitorGottliebTheEvent = InquisitorGottlieb("Инквизитор Готлиб",
                                                "Святая инквизиция! Срочно прячьте ведьм!",
                                                "Все сёстры, включая Чуму, возвращаются к своим изначальным "
                                                "владельцам.")


class GoodWitch(RandomEvent):
    def action(self, player):
        if not player.isHavingCard(CompassTheCard):
            player.getTheCardFromAnyPlayer(CompassTheCard, [VictorThePlayer, JulianThePlayer, GuildThePlayer,
                                                            QueenThePlayer, ChaosThePlayer])
            CompassTheCard.makePrivate()  # теперь он не засвечен
        logs.print("Новый владелец Компаса Ведьмы: " + player.name + "\n")


GoodWitchTheEvent = GoodWitch("Ведьма Ларисса",
                              "Ведьма Ларисса решила, что именно вы достойны спасти мир.",
                              "Получите Компас Ведьмы.")


class Victoria(RandomEvent):
    def action(self, player):
        if not ChaosThePlayer.isHavingCard(PlagueTheSister):
            ChaosThePlayer.getTheCardFromAnyPlayer(PlagueTheSister, [VictorThePlayer, JulianThePlayer, GuildThePlayer,
                                                                     QueenThePlayer])
            logs.print("Новый владелец карты Чума: " + ChaosThePlayer.name + "\n")
        else:
            player.getCard(PlagueTheSister, ChaosThePlayer)
            logs.print("Новый владелец карты Чума: " + player.name + "\n")


VictoriaTheEvent = Victoria("Дон Реджани спасает мир",
                            "Дон Реджани узнал про апокалипсис и решил срочно выкрасть Чуму, чтобы его "
                            "не допустить.",
                            "Если карта Чумы на руках, она возвращается к Хаосу. Иначе получите карту Чумы.")


class Marie(RandomEvent):
    def action(self, player):
        if not player.isHavingCard(PlagueTheSister):
            player.getTheCardFromAnyPlayer(PlagueTheSister, [VictorThePlayer, JulianThePlayer, GuildThePlayer,
                                                             QueenThePlayer, ChaosThePlayer])
        logs.print("Новый владелец карты Чума: " + player.name + "\n")


MarieTheEvent = Marie("Путешественница Мари",
                      "Гуляя по рынку, вы завели беседу с путешественницей, и она захотела уехать с вами.",
                      "Получите карту Чумы.")


class LittleMoney(RandomEvent):
    def action(self, player):
        player.money += 10
        logs.print("Вы получили 10 монет. Всего монет: "
                   + str(player.money) + "\n")


LittleMoneyTheEvent = LittleMoney("Потерянный кошелёк",
                                  "Вы нашли чей-то кошелёк.",
                                  "Получите 10 монет.")


class GuildLeader(RandomEvent):
    def action(self, player):
        if player == GuildThePlayer:
            logs.print("Разбойники не грабят своих.\n")
            return
        if fightWithNPC(player, FightStats(force=8, magic=2, mind=5), self):
            logs.print("\nВы победили разбойника.\n")
        else:
            for card in player.cards:
                if card.isLocation():
                    GuildThePlayer.getCard(card, player)
                    logs.print("\nВы не одолели разбойника. Новый владелец здания " + card.name + ": "
                               + GuildThePlayer.name + ".\n")
                    return
            logs.print("\nВы не одолели разбойника, но забирать ему нечего.\n")


GuildLeaderTheEvent = GuildLeader("Взломщик Романо",
                                  "Знаменитый взломщик Романо хочет забраться в ваш дом!",
                                  "Победите Романо или потеряйте одну из своих локаций.")


class Alice(RandomEvent):
    def action(self, player):
        if player == GuildThePlayer:
            logs.print("Разбойники не грабят своих.\n")
            return
        if fightWithNPC(player, FightStats(force=4, magic=6, mind=7), self):
            logs.print("\nВы победили разбойницу.\n")
        else:
            for card in player.cards:
                if card.isWeapon():
                    GuildThePlayer.getCard(card, player)
                    card.makePrivate()  # теперь оно не засвечено
                    logs.print("\nВы не одолели разбойницу. Новый владелец оружия " + card.name + ": "
                               + GuildThePlayer.name + ".\n")
                    return
            logs.print("\nВы не одолели разбойницу, но забирать ей нечего.\n")


AliceTheEvent = Alice("Карманница Алиса",
                      "Алиса хочет украсть у вас часы... или что-то подороже!",
                      "Победите Алису или потеряйте одну из своих карт оружия.")


class Basilio(RandomEvent):
    def action(self, player):
        if player == GuildThePlayer:
            logs.print("Разбойники не грабят своих.\n")
            return
        if fightWithNPC(player, FightStats(force=4, magic=7, mind=10), self):
            logs.print("\nВы победили разбойника.\n")
        else:
            for card in player.cards:
                if card.isSister():
                    GuildThePlayer.getCard(card, player)
                    logs.print("\nВы не одолели разбойника. Новый владелец карты " + card.name + ": "
                               + GuildThePlayer.name + ".\n")
                    return
            logs.print("\nВы не одолели разбойника, но уводить ему некого.\n")


BasilioTheEvent = Basilio("Мошенник Базилио",
                          "Кажется, этот мужчина пытается загипнотизировать вашу подругу!",
                          "Победите Базилио или потеряйте одну из сестёр.")


class GodDreaming(RandomEvent):
    def action(self, player):
        player.influence += 10
        logs.print("Получено 10 очков влияния. Всего очков влияния: "
                   + str(player.influence) + "\n")


GodDreamingTheEvent = GodDreaming("Божественное откровение",
                                  "Вам приснилось, что вы говорили с богом, и люди начали считать вас пророком.",
                                  "Получите 10 очков влияния.")


class Epidemic(RandomEvent):
    def action(self, player):
        if player == JulianThePlayer:
            if not player.isHavingCard(HospitalTheCard):
                player.getTheCardFromAnyPlayer(HospitalTheCard, [VictorThePlayer, JulianThePlayer, GuildThePlayer,
                                                                 QueenThePlayer, ChaosThePlayer])
            logs.print("Новый владелец карты Больница: " + player.name + "\n")
        else:
            freeInfluence = player.influenceToSold()
            player.influence -= freeInfluence
            logs.print("Потеряно " + str(freeInfluence) + " очков влияния. Всего очков влияния: "
                       + str(player.influence) + "\n")


EpidemicTheEvent = Epidemic("Эпидемия",
                            "В ваш край пришла болезнь... всё перестало иметь значение.",
                            "Если вы Джулиан, получите Больницу. Иначе потеряйте все свободные очки влияния.")


class Hunger(RandomEvent):
    def action(self, player):
        if player.isHavingCard(HungerTheSister):
            ChaosThePlayer.getCard(HungerTheSister, player)
            logs.print("Новый владелец карты Голод: " + ChaosThePlayer.name + "\n")
        else:
            moneyLost = player.money
            player.money = 0
            logs.print("Потеряно " + str(moneyLost) + " монет.\n")


HungerTheEvent = Hunger("Голод",
                        "Начался голод. Еда теперь стоит в разы дороже.",
                        "Если у вас есть карта Голода, отдайте её Хаосу. Иначе потеряйте все монеты.")


class Lucy(RandomEvent):
    def action(self, player):
        if player.isHavingCard(WarTheSister):
            for card in player.cards:
                if card.isArtefact():
                    ChaosThePlayer.getCard(card, player)
                    logs.print("Новый владелец карты " + card.name + ": " + ChaosThePlayer.name + ".\n")
                    return
            logs.print("У вас нет артефактов, поэтому вы ничего не теряете.\n")
        else:
            player.money += 2
            logs.print("Получено 2 монеты. Всего монет: " + str(player.money) + "\n")


LucyTheEvent = Lucy("Фрейлина Люси",
                    "Фрейлине Люси очень не нравится новая королева.",
                    "Если у вас есть карта Войны, потеряйте один артефакт. Иначе получите две монеты.")


class Andrew(RandomEvent):
    def action(self, player):
        for card in ChaosThePlayer.cards:
            if card.isArtefact():
                player.getCard(card, ChaosThePlayer)
                logs.print("Новый владелец карты " + card.name + ": " + player.name + ".\n")
                return
        logs.print("Нет доступных для получения артефактов.\n")


AndrewTheEvent = Andrew("Артефактор Эндрю",
                        "Вы получили подарок от светлого мага Эндрю.",
                        "Получите артефакт из запасов игры.")


class AlsoLittleMoney(RandomEvent):
    def action(self, player):
        player.money += 3
        logs.print("Вы получили 3 монет. Всего монет: "
                   + str(player.money) + "\n")


AlsoLittleMoneyTheEvent = AlsoLittleMoney("Потерянный кошелёк",
                                          "Вы нашли чей-то кошелёк.",
                                          "Получите 3 монет.")


class AnotherLittleMoney(RandomEvent):
    def action(self, player):
        player.money += 5
        logs.print("Вы получили 5 монет. Всего монет: "
                   + str(player.money) + "\n")


AnotherLittleMoneyTheEvent = AnotherLittleMoney("Потерянный кошелёк",
                                                "Вы нашли чей-то кошелёк.",
                                                "Получите 5 монет.")


class AnotherOneLittleMoney(RandomEvent):
    def action(self, player):
        player.money += 2
        logs.print("Вы получили 2 монеты. Всего монет: "
                   + str(player.money) + "\n")


AnotherOneLittleMoneyTheEvent = AnotherOneLittleMoney("Потерянный кошелёк",
                                                      "Вы нашли чей-то кошелёк.",
                                                      "Получите 2 монеты.")


allRandomEvents = [HeraldTheEvent, EvilWitchTheEvent, AlexTheEvent, JamesTheEvent, MargaretTheEvent,
                   EndOfTheRainbowTheEvent, DonReggianiTheEvent, InquisitorGottliebTheEvent, GoodWitchTheEvent,
                   VictoriaTheEvent, MarieTheEvent, LittleMoneyTheEvent, GuildLeaderTheEvent, AliceTheEvent,
                   BasilioTheEvent, GodDreamingTheEvent, EpidemicTheEvent, HungerTheEvent, LucyTheEvent,
                   AndrewTheEvent, AlsoLittleMoneyTheEvent, AnotherLittleMoneyTheEvent, AnotherOneLittleMoney]


# ФУНКЦИЯ ДЛЯ РАНДОМА: СРАЖЕНИЕ С НПС

def fightWithNPC(player, npcStats, randomEventCard):
    logs.print("ВНИМАНИЕ! ВНИМАНИЕ! НАЧИНАЕТСЯ БИТВА!")
    logs.print(randomEventCard.name + " нападает на " + player.name + "!\n")

    # выводим статы нападающего
    logs.print("Статы нападающего:")
    npcStats.writeStats()
    logs.print("")

    # защищающийся выбирает оружие и сестру
    logs.print(player.name + ", ваши статы:")
    player.fightStats.writeStats()

    logs.print("\nНичья в данной битве будет считаться проигрышем.")

    logs.print("\n" + player.name + ", пришла пора выбрать оружие.\n")
    defWeapon = selectWeapon(player)

    logs.print(player.name + ", присоединится ли к вам сестра?\n")
    defSister = selectSister(player)

    # оружие становится публичным
    defWeapon.isPrivate = False
    # сёстры протухают
    defSister.isExpired = True

    logs.print("=== БОЙ ===\n")

    logs.print("Нападающий:")
    logs.print("Имя: " + randomEventCard.name)
    npcStats.writeStats()

    logs.print("\nЗащищающийся:")
    logs.print("Имя: " + player.name)
    player.fightStats.writeStats()
    logs.print("Оружие:")
    defWeapon.writeInfo()
    logs.print("Сестра:")
    defSister.writeInfo()

    logs.print("\nБой окончен. Участвовавшие в бою сёстры устали, засвеченное оружие перестало быть скрытым.\n")
    return player.amIWinnerOfTheFightWithNpc(defWeapon, defSister, npcStats, randomEventCard.name)


def selectWeapon(attackingPlayer):
    # никогда так не делайте, но: собираем массив из всего оружия на руках
    allWeapons = []
    for card in attackingPlayer.cards:
        if card.isWeapon():
            allWeapons.append(card)
    if len(allWeapons) > 0:  # если есть, что использовать
        for weaponCard in allWeapons:
            logs.print("ЛОТ №" + str(allWeapons.index(weaponCard) + 1))
            weaponCard.writeInfo()
            logs.print("")
        while True:
            logs.print("Введите номер лота, который будете использовать.")
            attackWeaponIndex = logs.input()
            try:
                if (int(attackWeaponIndex) - 1) < 0:  # чтобы не работало на индексе -1
                    raise Exception
                attackWeapon = allWeapons[int(attackWeaponIndex) - 1]
                logs.print("Оружие выбрано: " + attackWeapon.name + "\n")
                break
            except Exception:
                print("Некорректный ввод. Попробуйте ещё раз.")
    else:  # если оружия нет, будем драться ничем
        attackWeapon = EmptyWeapon
        logs.print("У вас нет оружия.\n")
    return attackWeapon


def selectSister(attackingPlayer):
    allAvailableSisters = []
    for card in attackingPlayer.cards:
        if card.isSister():
            if attackingPlayer.isQueen() and card.name == "Война":  # Война может пользоваться собой сколько угодно раз
                allAvailableSisters.append(card)
            else:
                if not card.isExpired:  # если это не война, проверяем, не протухла ли сестра
                    allAvailableSisters.append(card)
    if len(allAvailableSisters) > 0:  # если есть, что использовать
        for sisterCard in allAvailableSisters:
            logs.print("СЕСТРА №" + str(allAvailableSisters.index(sisterCard) + 1))
            sisterCard.writeInfo()
            logs.print("")
        while True:
            logs.print("Введите номер сестры, которую будете использовать. 0 - без сестры.")
            attackSisterIndex = logs.input()
            if attackSisterIndex == "0":
                attackSister = EmptySister
                logs.print("Сестра не будет помогать вам в этом бою.\n")
                break
            try:
                attackSister = allAvailableSisters[int(attackSisterIndex) - 1]
                logs.print("Сестра выбрана: " + attackSister.name + "\n")
                break
            except Exception:
                print("Некорректный ввод. Попробуйте ещё раз.")
    else:  # если сестры нет, будем драться ничем
        attackSister = EmptySister
        logs.print("У вас нет доступных сестёр.\n")
    return attackSister


# ФУНКЦИЯ ДЛЯ УНИВЕРСИТЕТА: СВОП ОРУЖИЕМ

def swapWeapons(player1, player2, isChaos=True):
    if isChaos:
        logs.print("\nХАОС: " + player1.name + " и " + player2.name + " поменяются оружием.")
    if player1 == player2:
        return
    weapons1 = []
    weapons2 = []
    for card1 in player1.cards:
        if card1.isWeapon():
            weapons1.append(card1)
    for card2 in player2.cards:
        if card2.isWeapon():
            weapons2.append(card2)

    for card in weapons1:
        player2.getCard(card, player1)
    for card in weapons2:
        player1.getCard(card, player2)

    logs.print("Обмен совершён.")
