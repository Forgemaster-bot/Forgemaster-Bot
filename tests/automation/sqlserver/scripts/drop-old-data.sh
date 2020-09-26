#!/usr/bin/env bash

# source environment file to pickup user config
script_path="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"
source "${script_path}/docker-sql-env.sh"

password="$(cat "$sql_secrets" | grep "^SA_PASSWORD" | cut -d '=' -f 2)"

# run the image 
docker exec -it test-server /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "$password" -Q "
 USE LostWorld;
 DELETE FROM Main_Graveyard;
 DELETE FROM Main_Graveyard;
 DELETE FROM Main_Wizard_Spell_Share;
 DELETE FROM Main_Trade;
 DELETE FROM Main_Spell_Book;
 DELETE FROM Link_Spell_book_Spells;
 DELETE FROM Link_Character_Spells;
 DELETE FROM Link_Character_Skills;
 DELETE FROM Link_Character_Recipe;
 DELETE FROM Link_Character_Items;
 DELETE FROM Link_Character_Feats;
 DELETE FROM Link_Character_Class;
 DELETE FROM Error_Messages;
 DELETE FROM Main_Crafting;
 DELETE FROM Info_Discord;
 DELETE FROM Discord_Roll;
 DELETE FROM Main_Characters;
 DELETE FROM Command_Logs;
 "
 
