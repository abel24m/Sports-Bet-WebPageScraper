import mysql.connector
from pick_handler import Pick_Handler, League


#establishing the connection
conn = mysql.connector.connect(
                                user='root', 
                                password='33Raider', 
                                host='127.0.0.1', 
                                database='Sports_Picks')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
cursor.execute("SELECT DATABASE()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

drop_table = "DROP TABLE IF EXISTS nba_picks, nfl_picks, nhl_picks, ncaab_picks, ncaaf_picks"

cursor.execute(drop_table)


def build_fields(num_fields):
    fields = "away VARCHAR(100), home VARCHAR(100)"
    for x in range(1,num_fields - 1):
        temp = ", pick" + str(x) + " VARCHAR(100)"
        fields += temp
    return fields


def get_total_cols(matchups):
    total_cols = 0
    for matchup in matchups:
        if len(matchup) > total_cols:
            total_cols = len(matchup)
    return total_cols


def insert_values(matchups, total_cols, table_name):
    for matchup in matchups:
        away_team = matchup[0].replace("'","")
        value_string = "( '" + away_team + "'" 
        for field in range(1, total_cols):
            try:
                value = matchup[field]
                value = value.replace("'","")
                value_string += ", '" + value + "'"
            except IndexError:
                value_string += ", NULL "
        value_string += ");"
        insert_into_table = "INSERT INTO " + table_name + " VALUES " + value_string    
        cursor.execute(insert_into_table)
        conn.commit()


def enter_picks_into_database(phand):
    for league in League:
        match (league):
            case League.NBA:
                table_name = "nba_picks"
                total_cols = get_total_cols(phand.nba_picks)
                fields = build_fields(total_cols)
                create_table = "CREATE TABLE " + table_name + " (" + fields + ")"
                cursor.execute(create_table)
                insert_values(phand.nba_picks, total_cols, table_name)
            case League.NFL:
                table_name = "nfl_picks"
                total_cols = get_total_cols(phand.nfl_picks)
                fields = build_fields(total_cols)
                create_table = "CREATE TABLE " + table_name + " (" + fields + ")"
                cursor.execute(create_table)
                insert_values(phand.nfl_picks, total_cols, table_name)
            case League.NHL:
                table_name = "nhl_picks"
                total_cols = get_total_cols(phand.nhl_picks)
                fields = build_fields(total_cols)
                create_table = "CREATE TABLE " + table_name + " (" + fields + ")"
                cursor.execute(create_table)
                insert_values(phand.nhl_picks, total_cols, table_name)
            case League.NCAAB:
                table_name = "ncaab_picks"
                total_cols = get_total_cols(phand.ncaab_picks)
                fields = build_fields(total_cols)
                create_table = "CREATE TABLE " + table_name + " (" + fields + ")"
                cursor.execute(create_table)
                insert_values(phand.ncaab_picks, total_cols, table_name)
            case League.NCAAF:
                table_name = "ncaaf_picks"
                total_cols = get_total_cols(phand.ncaaf_picks)
                fields = build_fields(total_cols)
                create_table = "CREATE TABLE " + table_name + " (" + fields + ")"
                cursor.execute(create_table)
                insert_values(phand.ncaaf_picks, total_cols, table_name)      
        

