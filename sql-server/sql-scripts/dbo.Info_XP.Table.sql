USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_XP]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_XP](
	[Level] [int] NOT NULL,
	[XP] [int] NULL,
	[XP_To_Level] [int] NULL,
	[Proficiency_Bonus] [int] NULL
) ON [PRIMARY]
GO
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (1, 300, 300, 2)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (2, 900, 600, 2)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (3, 2700, 1800, 2)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (4, 6500, 3800, 2)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (5, 14000, 7500, 3)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (6, 23000, 9000, 3)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (7, 34000, 11000, 3)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (8, 48000, 14000, 3)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (9, 64000, 16000, 4)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (10, 85000, 21000, 4)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (11, 100000, 15000, 4)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (12, 120000, 20000, 4)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (13, 140000, 20000, 5)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (14, 165000, 25000, 5)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (15, 195000, 30000, 5)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (16, 225000, 30000, 5)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (17, 265000, 40000, 6)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (18, 305000, 50000, 6)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (19, 355000, 50000, 6)
INSERT [dbo].[Info_XP] ([Level], [XP], [XP_To_Level], [Proficiency_Bonus]) VALUES (20, 0, NULL, 6)
GO
