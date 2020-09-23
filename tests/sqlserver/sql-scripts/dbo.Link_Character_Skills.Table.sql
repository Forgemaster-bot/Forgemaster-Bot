USE [LostWorld]
GO
/****** Object:  Table [dbo].[Link_Character_Skills]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Link_Character_Skills](
	[Character_ID] [uniqueidentifier] NOT NULL,
	[Skill] [nvarchar](50) NOT NULL,
	[Proficiency] [int] NOT NULL
) ON [PRIMARY]
GO
