import sqlite3

animal_db = sqlite3.connect('animal_crossing.db')


def get_stats(name):
    """
    Get name, strength, weaknessses, special moves, gear, record, and category
    """
    sql = '''
    SELECT name, species, strengths, weaknesses, specialMoves, boxingGear, record, category
    FROM villager
    WHERE name = ?
    '''
    return animal_db.execute(sql, (name,)).fetchone()

def get_villager_name(name):
    """
    Get villager name
    """
    sql = '''
    SELECT name
    FROM villager
    WHERE name = ?
    '''
    return animal_db.execute(sql, (name,)).fetchone()[0]



def add_villager(highest_id, name, species, strengths, weaknesses, boxingGear):
    """
    add a villager
    """
    sql = '''
    INSERT OR REPLACE INTO villager (id, name, species, strengths, weaknesses, boxingGear, record)
    VALUES (?, ?, ?, ?, ?, ?, NULL)
    '''
    animal_db.execute(sql, (highest_id, name, species, strengths, weaknesses, boxingGear))
    animal_db.commit()


def show_specialmoves(name):
    """
    show special move
    """
    sql = '''
    SELECT specialMoves
    FROM villager
    WHERE specialMoves = ?
    '''
    animal_db.execute(sql, (name,))
    animal_db.commit()


def get_top10():
    """
    Display top 10 fighters based on record
    """
    sql = '''
    SELECT name, record
    FROM villager
    ORDER BY CAST(SUBSTR(record, 1, INSTR(record, '-')-1) AS INT) DESC
    LIMIT 10
    
    '''
    return animal_db.execute(sql, ()).fetchall()



def fighting_match(villager1, villager2):
    """
    fight
    """

    sql = '''
    SELECT vs1.name, vs1.totalScore, vs2.name, vs2.totalScore
    FROM villagerScores3 vs1
    JOIN villagerScores3 vs2 ON vs1.villagerID = vs2.villagerID AND vs2.villagerID != vs1.villagerID
    WHERE vs1.name = ?
    AND vs2.name = ?
    AND vs1.totalScore > vs2.totalScore;


    '''
    animal_db.execute(sql, (villager1, villager2)).fetchone()

    

def show_gear():
    """
    show gear
    """
    sql = '''
    SELECT name, description 
    FROM boxingGear
    '''
    animal_db.execute(sql, ())
    animal_db.commit()


def show_losers():
    """
    show villagers with no wins
    """
    sql = '''
    SELECT name
    FROM villager
    WHERE record = 0-?
    
    '''
    animal_db.execute(sql, ())
    animal_db.commit()


def display_past_winning_matches(winner):
    """
    Display past matches
    """
    sql = '''

    SELECT *
    FROM matches
    WHERE winner = ?
    
    '''
    return animal_db.execute(sql, (winner,)).fetchall()


def display_category():
    """
    Display category info
    """
    sql = '''
    SELECT category, minimumWeight, maximumWeight
    FROM category3
    
    '''
    return animal_db.execute(sql, ()).fetchall()

def display_members_category(category):
    """
    Display all animals that belong to category 
    """
    sql = '''
    SELECT name
    FROM villager
    WHERE category = ?
    '''
    return animal_db.execute(sql, ( category,)).fetchall()

def villagers_list():
    """
    List all users.
    """
    sql = '''
    SELECT name
    FROM villager
    '''
    return animal_db.execute(sql).fetchall()

def cleaner_villager_list():
    villager_list = villagers_list()
    better_list = []
    for user in villager_list:
        better_list.append(user[0])
    return better_list


def main():
    print('Welcome to the animal crossing fighting ring!')
    print('Enter the villager you would like to see fight')
    all_villagers = cleaner_villager_list()
    print(all_villagers)
    villager_name = input('Villager name: ')
    
    
    if (villager_name) in all_villagers:
        fighter1 = get_villager_name(villager_name)
        print(get_stats(fighter1))
    else:
        print('villager does not exist')
        print('Add villager now')
        name = input('Name: ')
        species = input('species: ')
        highest_id = animal_db.execute(
            'SELECT MAX(id) FROM villager').fetchone()[0]
        #print("printing highest id" + str(highest_id))
        highest_id = highest_id + 1
        add_villager(highest_id, name, species)
    while True:
        print('What would you like to do?')
        print('1. Add a villager to database')
        print('2. View villagers')
        print('3. Get villagers stats')
        print('4. Get top10 fighters')
        print('5. Show category info')
        print('6. View past winning matches')
        #print('6. show prizes')
        print('7. Start a match')
        print('8. Exit')
        choice = input('Choice: ')
        if choice == '1':
            print('add new villagers information: ')
            name = input('name: ')
            species = input('species: ')
            strengths = input('strengths: ')
            weaknesses = input('weaknesses: ')
            boxingGear = input('boxing gear: ')
            highest_id = animal_db.execute(
                'SELECT MAX(villagerID) FROM villager').fetchone()[0]
            #print("printing highest id" + str(highest_id))
            highest_id = highest_id + 1
            add_villager(highest_id, name, species, strengths, weaknesses, boxingGear)
            print('villager was successfully added')
        elif choice == '2':
            all_villagers = cleaner_villager_list()
            print(all_villagers)

        elif choice == '3':
            print('Villager stats:')
            villager_name = input('enter name of villager: ')
            if villager_name in all_villagers:
                fighter1 = get_villager_name(villager_name)
                stats = get_stats(fighter1)
                print(f"Name: {stats[0]}")
                print(f"Species: {stats[1]}")
                print(f"Strengths: {stats[2]}")
                print(f"Weaknesses: {stats[3]}")
                print(f"Special Moves: {stats[4]}")
                print(f"Boxing Gear: {stats[5]}")
                print(f"Record: {stats[6]}")
                print(f"Category: {stats[7]}")
            else:
                print('Villager does not exist in the database.')
        elif choice == '4':
            print('top 10 villagers:')
            top10 = get_top10()
            for i, (name, record) in enumerate(top10):
                print(f"{i+1}. {name} - {record}")
                
        elif choice == '5':
            print('category info:')
            
            for villager in (display_category()):
                print('category name: ', villager[0])
                print('min weight: ', villager[1])
                print('max weight: ', villager[2])

        elif choice == '6':
            winner = input('Enter the name of the winner: ')
            matches = display_past_winning_matches(winner)
            if matches:
                print('The following are the past winning matches for ' + winner + ':')
                for match in matches:
                    print('location: ', match[1])
                    print('winner: ', match[2])
                    print('loser: ', match[3])
                    print('prize: ', match[4])
            else:
                print('No matches found for ' + winner)
        #elif choice == '6':
            #match = input(
                #'show top prizes ')
            #show_prizes(get_user_id(person))
            #print('top prizes')
        elif choice == '7':
            fighter1 = input('Enter first villager: ')
            fighter2 = input('Enter second villager: ')
            result = fighting_match(fighter1, fighter2)
            if result:
                print('match results...')
                print(result[0], 'wins!')
            else:
                print('match results...')
                print('Its a tie!')
        
            #print(fighting_match(fighter1, fighter2))
        elif choice == '8':
            print('Goodbye!')
            return


main()