USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_Spells_Known]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_Spells_Known](
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
INSERT [dbo].[Info_Spells_Known] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Bard', 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 15, 16, 18, 19, 19, 20, 22, 22, 22)
INSERT [dbo].[Info_Spells_Known] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Blood Hunter', 0, 0, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10)
INSERT [dbo].[Info_Spells_Known] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Fighter', 0, 0, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 11, 11, 12, 13)
INSERT [dbo].[Info_Spells_Known] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Ranger', 0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11)
INSERT [dbo].[Info_Spells_Known] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Rogue', 0, 0, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 11, 11, 12, 13)
INSERT [dbo].[Info_Spells_Known] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Sorcerer', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15)
INSERT [dbo].[Info_Spells_Known] ([Class], [level_1], [level_2], [level_3], [level_4], [level_5], [level_6], [level_7], [level_8], [level_9], [level_10], [level_11], [level_12], [level_13], [level_14], [level_15], [level_16], [level_17], [level_18], [level_19], [level_20]) VALUES (N'Warlock', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15)
GO
