USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_Feats]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_Feats](
	[Name] [nvarchar](50) NOT NULL,
	[Prerequisite] [nvarchar](50) NOT NULL,
	[Description] [nvarchar](max) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Magic Initiate', N'', N'You learn two cantrips and one 1st-level spell from one class.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Martial Adept', N'', N'You learn two maneuvers from Battle Master archetype and gain one superiority die (d6).')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Medium Armor Master', N'', N'Proficiency with medium armor No disadvantage to Stealth checks wearing medium armor and Dexterity bonus max to +3 instead of +2.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Mobile', N'', N'Your speed increase by 10 ft, you can Dash on difficult terrain without malus, and do not provoke opportunity attacks in melee.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Moderately Armored', N'Proficiency with light armor', N'	+1 in Str. or Dex. and you gain proficiency with medium armor and shields.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Mounted Combatant', N'', N'Advantage on melee attacks against unmounted creature and force an attack to target you instead of your mount.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Observant', N'', N'+1 in Int. or Wis., you can read on lips, and you have a +5 bonus in passive Perception and passive Investigation.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Orcish Fury', N'Half-orc', N'+1 in Str. or Con., add one of the weapon damage dice, and use a reaction to attack after using Relentless Endurance.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Polearm Master', N'', N'You can make an extra attack with a polearm weapon, and make an opportunity attack if a creature enter your reach.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Prodigy', N'Half-elf, half-orc, or human', N'	You gain proficiency with one skill, one tool or one language, and you gain expertise with one skill.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Resilient', N'', N'+1 in one ability and you gain proficiency in saving throws using this ability.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Ritual Caster', N'Intelligence or Wisdom 13 or higher', N'You have a ritual book with two 1-st level ritual spells from one class and you can later on add other ritual spells you found.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Savage Attacker', N'', N'You can reroll melee weapon attack damage once per turn.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Second Chance', N'Halfling', N'+1 in Dex., Con., or Cha., and you can force a creature to reroll its attack roll if it hits you.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Sentinel', N'', N'A successful OA reduce creature speed to 0 for this turn and possibility to make an OA even if the ennemy take Disengage.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Sharpshooter', N'', N'Your ranged attacks ignore some cover, no disavantage at long range, and possibility to take -5 to hit for +10 on ranged damage.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Shield Master', N'', N'Attack also allows to shove, shield bonus to Dex. saving throws againts spells, and no 1/2 damage on successful saving throw.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Skilled', N'', N'You gain proliciency with three skills or tools.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Skulker', N'Dexterity 13 or higher', N'Ranged weapon attack does not reveal your position and possibility to hide in a lighlly obscured area.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Spell Sniper', N'The ability to cast at least one spell', N'Offensive spell range doubled, these spells ignore some cover, and you learn one offensive cantrip.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Squat Nimbleness', N'Dwarf or a Small race', N'+1 in Str. or Dex., your speed increases by 5 ft, and proficiency and advantage to escape with Acrobatics or Athletics checks.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Tavern Brawler', N'', N'+1 in Str. or Con., proficiency with improvised weapons, d4 for unarmed strike, and grapple with a bonus action.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Tough', N'', N'Your hit point maximum increases by an amount equal to twice your level then by +2 at each level.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'War Caster', N'The ability to cast at least one spell', N'You have advantage on saving throws to maintain concentration and you can cast some spells as part of an OA with a reaction.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Weapon Master', N'', N'+1 in Str. or Dex. and you gain profociency with four weapons.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Wood Elf Magic', N'Elf (wood)', N'You learn one druid cantrip and can cast the longstrider and pass without trace spells (1/long rest).')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'ASL', N'', N'Increase a stat')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Actor', N'', N'+1 in Cha., advantage on Deception and Performance checks, mimic the speech of a person or the sounds made by a creature.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Alert', N'', N'+5 to initiative, you cannot be surprised, and creatures you do not see do not gain advantage on attack roll against you.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Athlete', N'', N'+1 in Str. or Dex. you stand up and climb more quickly, and you can jump with only a 5-ft run.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Bountiful Luck', N'Halfling', N'You can let an ally within 30 ft of you to reroll a 1 on a d20.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Charger', N'', N'As part of the Dash action you can make a melee attack with a +5 bonus if you move at least 10 ft before.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Crossbow Expert', N'', N'You ignore the loading property of crossbows and do not have disadvantage for being in contact with a creature when you shoot.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Defensive Duelist', N'Dexterity 13 or higher', N'You can add you proficiency bonus to your AC if you are wielding a finesse weapon.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Dragon Fear', N'Dragonborn', N'+1 in Str., Con., or Cha. and your Breath Weapon can frighten instead of inflicting damages.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Dragon Hide', N'Dragonborn', N'+1 in Str., Con., or Cha., your AC becomes 13+Dex. modifier and your retractable claws deal 1d4+Str. modifier slashing damage.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Drow High Magic', N'Elf (drow)', N'You can cast the detect magic spell (at will) and the levitate and dispel magic spells (1/long rest).')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Dual Wielder', N'', N'+1 to CA if you are wielding a melee weapon in each hand, two-weapon fighting with non-light weapon, draw two weapons.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Dungeon Delver', N'', N'Advantage to Perception and Investigation checks, to saving throws vs traps, and search for traps at normal pace.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Durable', N'', N'+1 in Con. and for each Hit Dice you regain a minimum of hit points equals to 2 x your Constitution modifier.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Dwarf Fortitude', N'Dwarf', N'+1 in Con., and you can spend one Hit Die to heal yourself taking the Dodge action.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Elemental Adept', N'The ability to cast at least one spell', N'Your spells ignore resistance to a damage type (acid, cold, fire, lightning, or thunder) and treat any 1 in damage as a 2.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Elven Accuracy', N'Elf or half-elf', N'+1 in Dex., Int., Wis., or Cha., and you can reroll one attack roll if you have advantage.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Fade away	Gnome', N'', N'	+1 in Dex. or Int., and you can use your reaction to become invisible if you take damage.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Fey Teleportation', N'Elf (high)', N'+1 in Int. or Cha., you speak Sylvan, and you can cast the misty step spell (1/short rest).')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Flames of Phlegethos', N'Tiefling', N'+1 in Int. or Cha., reroll any 1 on fire spell damage, and cause flames to wreathe you if you cast a fire spell.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Grappler', N'Strength 13 or higher', N'You have advantage on attack rolls when grappling, and can try to restrained a creature grappled by you.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Great Weapon Master', N'', N'Extra attack after a melee critical hit and you can choose to take -5 to attack roll to add +10 to damage with an heavy weapon.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Healer', N'', N'You can stabilize a creature and restore it to 1 hp, or restore [1d6+4+its number of Hit Dice] hp to it.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Heavily Armored', N'Proficiency with medium armor', N'+1 in Str. and you gain proficiency with heavy armor.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Heavy Armor Master', N'Proficiency with heavy armor', N'+1 in Str. and bludgeoning, piercing, and slashing damage are reduced by 3 if you are wearing an heavy armor.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Infernal Constitution', N'Tiefling', N'+1 in Con., resistance to cold and poison damage, and you have advantage on saving throws against being poisoned.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Inspiring Leader', N'Charisma 13 or higher', N'	Up to 6 creatures within 30 ft of you can gain temporary hp equal to your levei + your Cha. modifier.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Keen Mind', N'', N'+1 in Int., you know which way is north, when is the next sunrise/sunset, and recall any events within the past month.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Lightly Armored', N'', N'+1 in Str. or Dex. and you gain profociency with light armor.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Linguist', N'', N'+1 in Int., you learn three languages, and you can ably create ciphers.')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Lucky', N'', N'You can reroll one d20 or force to reroll an attack roll against you (3/long rest).')
INSERT [dbo].[Info_Feats] ([Name], [Prerequisite], [Description]) VALUES (N'Mage Slayer', N'', N'You can use a reaction to make a melee attack against a spellcaster and advantage on saving throws against spell within 5 ft.')
GO
