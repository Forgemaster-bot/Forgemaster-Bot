USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_Skills]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_Skills](
	[Name] [nvarchar](50) NOT NULL,
	[Ability] [nvarchar](50) NOT NULL,
	[Job] [bit] NOT NULL,
	[Tools] [nvarchar](50) NULL,
	[Consumable_Name] [nvarchar](50) NULL
) ON [PRIMARY]
GO
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Acrobatics', N'Dexterity', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Arcana', N'Intelligence', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Athletics', N'Strength', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Deception', N'Charisma', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'History', N'Intelligence', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Insight', N'Wisdom', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Intimidation', N'Charisma', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Investigation', N'Intelligence', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Medicine', N'Wisdom', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Nature', N'Intelligence', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Perception', N'Wisdom', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Performance', N'Charisma', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Persuasion', N'Charisma', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Religion', N'Intelligence', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Sleight of Hand', N'Dexterity', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Stealth', N'Dexterity', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Survival', N'Wisdom', 0, NULL, NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Alchemist', N'Intelligence', 1, N'Alchemist supplies', N'Bomb')
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Herbalist', N'Intelligence', 1, N'Herbalism Kit', N'Potion')
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Calligrapher', N'Inteligence', 1, N'Calligrapher Supplies', N'Glyph')
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Carpenter', N'Inteligence', 1, N'Carpenters tools', NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Poisoner', N'Inteligence', 1, N'Poisoner Kit', N'Powder')
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Tinker', N'Inteligence', 1, N'Tinker Tools', NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Cook', N'Inteligence', 1, N'Cooks utensils', N'Snack')
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Leatherworker', N'Inteligence', 1, N'Leatherworker tools', NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Smith', N'Inteligence', 1, N'Smiths tools', NULL)
INSERT [dbo].[Info_Skills] ([Name], [Ability], [Job], [Tools], [Consumable_Name]) VALUES (N'Weaver', N'Inteligence', 1, N'Weavers tools', NULL)
GO
