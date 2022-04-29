from initGameObjects import VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer, ChaosThePlayer, \
    WarTheSister
from gameplayFunctions import currentWinner, buyInfluence, buyWeapon, sellSomething, buyArtefact, inviteToSisterFight, \
    inviteToFight, intelligence, randomCard, chaosCardPlay
from writelogs import logs
from time import gmtime, strftime
import shutil

# обнулить временный лог
with open("templogs.txt", "w") as file:
    file.write("Сёстры Апокалипсиса. Партия от " + strftime("%Y-%m-%d %H-%M-%S", gmtime()) + "\n\n")

# инициализировать игроков
PlayablePlayers = [VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer]
Players = [VictorThePlayer, JulianThePlayer, GuildThePlayer, QueenThePlayer, ChaosThePlayer]

# начало игры
print(f'СЁСТРЫ АПОКАЛИПСИСА\n')

print(f'Давным-давно на свет появилось четыре сестры: красавица Елена, из-за чьей улыбки развязываются Войны, '
      f'\nпутешественница Мари, не раз привозившая из дальних стран Чуму, вспыльчивая Роксана, причина пожаров и '
      f'\nГолода, и малышка Энни, за которой по пятам ходит Смерть.')
print(f'По легенде, если все сёстры соберутся вместе, начнётся апокалипсис, поэтому когда-то давно их растащили по '
      f'\nпо разным концам света - лишь бы они не встретились.')
print(f'Однако время шло, и спустя столетия сёстры оказались в одном городе - а, значит, мир снова на грани гибели!'
      f'\nНо есть и способ предотвратить неизбежное - для этого нужен специальный артефакт, костяной компас с '
      f'\nчетырьмя стрелками, указывающими не на стороны света, а на соответствующих им сестёр. Если показания этого '
      f'\nкомпаса сойдутся с показаниями настоящего компаса, мир будет спасён.\n')

print(f'Виктор Кастелли разочаровался в жизни и хочет устроить апокалипсис. Он считает, что хороший, правильный мир '
      f'\nможно построить только на руинах. В воплощении страшного плана Виктору помогает сама Смерть.')
print(f'Джулиан Медичи всегда стремился помогать людям, а потому легко принял костяной компас, подаренный ему '
      f'\nведьмой, и назначил своей миссией спасение мира. Одна из сестёр, Голод, согласилась ему помочь, но едва ли '
      f'\nостальные будут столь сговорчивы - поговаривают, что Компас не освобождает сестёр, а убивает их...')
print(f'Для Гильдии Разбойников нет ничего святого. Война, чума, да хоть конец света - лишь бы было, чем навариться. '
      f'\nИ что-то подсказывает главам Гильдии, что на ожидании апокалипсиса можно сделать целое состояние.')
print(f'Прекрасная Елена, прозванная Кровавой Королевой за свою любовь к разжиганию войн, намерена подчинить себе '
      f'\nвесь мир. Для этого ей нужно укрепить авторитет своей власти и научить перепуганных разбойниками жителей, '
      f'\nкого на самом деле стоит бояться.')

# игра идёт бесконечно, пока кто-нибудь не победит
movesCount = 0  # счётчик ходов
isGameEnded = False  # флаг выхода из игры
while True:
    movesCount += 1
    logs.print("\n=============================================")
    logs.print("РАУНД #" + str(movesCount))
    logs.print("=============================================\n")
    for Player in Players:
        if Player in PlayablePlayers:
            # игра
            logs.print("\nХОДИТ " + Player.name.upper())
            Player.writeInfo()

            # в начале круга все твои карты восстанавливаются
            for card in Player.cards:
                if card.isExpired:
                    card.makeUnexpired()

            # сначала собираем плюшки со своих локаций
            logs.print("=== Первый этап хода: Сбор плюшек со своих локаций.\n")
            for card in Player.cards:
                if card.isLocation():
                    card.action(Player)
                    logs.print("")
            logs.print("Первый этап хода окончен. ===\n")

            logs.print("=== Второй этап хода: Торговля.\n")
            if Player.isQueen() and Player.isKidnapped:
                logs.print("Вас похитили, вы не можете торговать.\n")
            else:
                # начинаем с продажи
                sellSomething(Player)
                # покупаем очки влияния
                buyInfluence(Player)
                # покупаем оружие
                buyWeapon(Player)
                # покупаем артефакты
                buyArtefact(Player)
            logs.print("Второй этап хода окончен. ===\n")

            logs.print("=== Третий этап хода: Сражение.\n")
            if Player.isQueen() and Player.isKidnapped:
                logs.print("Вас похитили, вы не можете драться.\n")
            else:
                print("Подсказка: для победы в бою нужно превзойти противника в 2х статах из 3х.\n")
                # боёвки: можно один раз подраться за сестру
                inviteToSisterFight(Player)
                # боёвки: можно один раз подраться за предмет
                inviteToFight(Player)
            logs.print("Третий этап хода окончен. ===\n")

            logs.print("=== Четвёртый этап хода: Разведка.\n")
            if Player.isQueen() and Player.isKidnapped:
                logs.print("Вас похитили, вы обязаны вытянуть карту случайного события.\n")
                # здесь рандом
                randomCard(Player)
                if Player.isKidnapped:
                    logs.print("Случайное событие не помогло, вы всё похищены.\n")
                    while True:
                        logs.print("Желаете отдать все свои локации, чтобы освободиться?\n"
                                   "Введите ответ: 1 - да, 0 - нет.")
                        answer = logs.input()
                        if answer == "1":
                            for card in Player.cards:
                                if card.isLocation():
                                    ChaosThePlayer.getCard(card, QueenThePlayer)
                                    logs.print("Королева потеряла локацию " + card.name)
                            Player.getTheCardFromAnyPlayer(WarTheSister, Players)
                            logs.print("\nКоролева оcвободилась благодаря Хаосу.\n")
                            break
                        else:
                            if answer == "0":
                                logs.print("Королева отказалась от освобождения.\n")
                                break
                            else:
                                print("Некорректный ввод. Попробуйте ещё раз.")
            else:  # если ходит не похищенная королева
                if Player == GuildThePlayer:  # для гильдии разведка дешевле
                    intelligenceMinCost = 5
                else:
                    intelligenceMinCost = 10
                logs.print("Вы можете вытянуть случайное событие (бесплатно) или отправиться на разведку (от "
                           + str(intelligenceMinCost) + " монет).")
                # рандом или разведка
                while True:
                    logs.print("Что выберете? 1 - случайное событие, 2 - разведка.")
                    answer = logs.input()
                    if answer == "1":
                        logs.print("Вы вытягиваете карту случайного события.\n")
                        randomCard(Player)
                        break
                    else:
                        if answer == "2":
                            # здесь проверка на деньги и разведка
                            if Player.money >= intelligenceMinCost:
                                # разведка
                                intelligence(Player)
                            else:
                                logs.print("Не пытайтесь обмануть судьбу, у вас нет денег на разведку!")
                                logs.print("Вы вытягиваете карту случайного события.\n")
                                randomCard(Player)
                            break
                        else:
                            print("Некорректный ввод. Попробуйте ещё раз.")
            logs.print("Четвёртый этап хода окончен. ===\n")
            logs.print("=============================================\n")
        else:
            logs.print("=== ВРЕМЯ ХАОСА! ===")

            print("\n=== СТАТЫ ===\n")
            print("Влияние: " + str(Player.influence) + " очков\n")

            print("Что нужно для победы Хаоса:")
            print(Player.goal)

            logs.print("\n=== КОНЕЦ ИНФОДАМПА ===\n")
            Player.writeInfoIntoLogsOnly()
            # ход Хаоса
            chaosCount = 0  # не, ну вдруг баганёт
            if ChaosThePlayer.influence > 20:
                chaosCount = 4
                logs.print("Поскольку влияние Хаоса > 20, будет разыграно " + str(chaosCount) + " карт Хаоса.")
            if 16 <= ChaosThePlayer.influence <= 20:
                chaosCount = 3
                logs.print("Поскольку влияние Хаоса в диапазоне 16-20, будет разыграно " + str(chaosCount) + " карт "
                                                                                                             "Хаоса.")
            if 11 <= ChaosThePlayer.influence <= 15:
                chaosCount = 2
                logs.print("Поскольку влияние Хаоса в диапазоне 11-15, будет разыграно " + str(chaosCount) + " карт "
                                                                                                             "Хаоса.")
            if 5 <= ChaosThePlayer.influence <= 10:
                chaosCount = 1
                logs.print("Поскольку влияние Хаоса в диапазоне 5-10, будет разыграно " + str(chaosCount) + " карт "
                                                                                                            "Хаоса.")
            if ChaosThePlayer.influence < 5:
                chaosCount = 0
                logs.print("Поскольку влияние Хаоса < 5, будет разыграно " + str(chaosCount) + " карт Хаоса.")

            i = 0
            while i < chaosCount:
                chaosCardPlay()
                i += 1

            logs.print("\n=== ЭТАП ХАОСА ОКОНЧЕН ===")
        # после каждого хода проверяем, не случилось ли победы
        if currentWinner() != 0:
            logs.print("\n=============================================")
            logs.print("=== ИГРА ЗАКОНЧЕНА ===")
            logs.print("=============================================\n")
            logs.print("Победитель: " + currentWinner().name)
            logs.print("")
            isGameEnded = True
            break
        # если не случилось, передаём ход; также есть возможность закончить игру без объявления победы
        print(f'\nХод окончен. 1 или 0 - продолжить игру, 9 - закончить игру.')
        isQuit = input()
        if isQuit == "9":
            logs.print("\n=============================================")
            logs.print("=== ИГРА ЗАКОНЧЕНА БЕЗ ПОБЕДИТЕЛЯ ===")
            logs.print("=============================================\n")
            isGameEnded = True
            break

    if isGameEnded:
        break

# после конца игры предлагаем посмотреть на финальные статы
print(f'Хотите посмотреть на статы игроков? Введите 1, если да. Иначе введите любой другой символ')
isStates = input()
if isStates == "1":
    for Player in Players:
        Player.writeInfo()
    else:  # если пользователь отказывается посмотреть статы, всё равно выводим их в логи
        for Player in Players:
            Player.writeInfoIntoLogsOnly()

# сохранить файл с логами
print(f'\nСохранить лог? Введите 1, если да. Иначе введите любой другой символ')
areLogsSaved = input()
if areLogsSaved == "1":
    newLogFileName = "logs " + strftime("%Y-%m-%d %H-%M-%S", gmtime()) + ".txt"
    shutil.copyfile("templogs.txt", newLogFileName)
    print(f'Лог успешно сохранён.')
else:
    print(f'Лог не будет сохранён. Если он вам всё-таки нужен, скопируйте содержимое файла templogs.txt до запуска '
          f'новой партии. Хорошего дня!')
