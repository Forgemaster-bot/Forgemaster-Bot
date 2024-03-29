USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_Classes]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_Classes](
	[Class] [nvarchar](50) NOT NULL,
	[Sub_Class_Level] [int] NOT NULL,
	[All_Spells_known] [bit] NOT NULL
) ON [PRIMARY]
GO
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Artificer', 3, 1)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Barbarian', 3, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Bard', 3, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Blood Hunter', 3, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Cleric', 1, 1)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Druid', 2, 1)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Fighter', 3, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Monk', 3, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Paladin', 3, 1)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Ranger', 3, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Rogue', 3, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Sorcerer', 1, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Warlock', 1, 0)
INSERT [dbo].[Info_Classes] ([Class], [Sub_Class_Level], [All_Spells_known]) VALUES (N'Wizard', 2, 0)
GO
