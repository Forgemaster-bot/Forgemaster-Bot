USE [LostWorld]
GO
/****** Object:  Table [dbo].[Link_Skills_Recipies]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Link_Skills_Recipies](
	[Skill] [nvarchar](50) NOT NULL,
	[Craft] [nvarchar](max) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Alchemist', N'Consumable from a recipe')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Calligrapher', N'Consumable from a recipe')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Cook', N'Consumable from a recipe')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Herbalist', N'Consumable from a recipe')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Poisoner', N'Consumable from a recipe')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Alchemist', N'Experiment with ingredients')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Calligrapher', N'Experiment with ingredients')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Cook', N'Experiment with ingredients')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Herbalist', N'Experiment with ingredients')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Poisoner', N'Experiment with ingredients')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Alchemist', N'Mundane item')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Carpenter', N'Mundane item')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Cook', N'Mundane item')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Leatherworker', N'Mundane item')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Smith', N'Mundane item')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Tinker', N'Mundane item')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Weaver', N'Mundane item')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Alchemist', N'Look at recipe book')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Calligrapher', N'Look at recipe book')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Cook', N'Look at recipe book')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Herbalist', N'Look at recipe book')
INSERT [dbo].[Link_Skills_Recipies] ([Skill], [Craft]) VALUES (N'Poisoner', N'Look at recipe book')
GO
