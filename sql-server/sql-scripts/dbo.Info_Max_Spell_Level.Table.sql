USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_Max_Spell_Level]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_Max_Spell_Level](
	[Class] [nvarchar](255) NULL,
	[level_1] [int] NULL,
	[level_2] [int] NULL,
	[level_3] [int] NULL,
	[level_4] [int] NULL,
	[level_5] [int] NULL,
	[level_6] [int] NULL,
	[level_7] [int] NULL,
	[level_8] [int] NULL,
	[level_9] [int] NULL,
	[level_10] [int] NULL,
	[level_11] [int] NULL,
	[level_12] [int] NULL,
	[level_13] [int] NULL,
	[level_14] [int] NULL,
	[level_15] [int] NULL,
	[level_16] [int] NULL,
	[level_17] [int] NULL,
	[level_18] [int] NULL,
	[level_19] [int] NULL,
	[level_20] [int] NULL
) ON [PRIMARY]
GO
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Artificer', 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Bard', 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 9)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Blood Hunter', 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Cleric', 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 9)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Druid', 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 9)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Fighter', 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Paladin', 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Ranger', 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Rogue', 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Sorcerer', 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 9)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Warlock', 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)
INSERT [dbo].[Info_Max_Spell_Level] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Wizard', 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 9)
GO
