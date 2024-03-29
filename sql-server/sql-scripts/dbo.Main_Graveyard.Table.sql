USE [LostWorld]
GO
/****** Object:  Table [dbo].[Main_Graveyard]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Main_Graveyard](
	[ID] [uniqueidentifier] NOT NULL,
	[Discord_ID] [nvarchar](50) NOT NULL,
	[Character_Name] [nvarchar](50) NOT NULL,
	[Race] [nvarchar](50) NOT NULL,
	[Background] [nvarchar](50) NOT NULL,
	[XP] [int] NOT NULL,
	[Strength] [int] NOT NULL,
	[Dexterity] [int] NOT NULL,
	[Constitution] [int] NOT NULL,
	[Intelligence] [int] NOT NULL,
	[Wisdom] [int] NOT NULL,
	[Charisma] [int] NOT NULL,
	[Gold] [float] NOT NULL,
	[Reason] [nvarchar](max) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
