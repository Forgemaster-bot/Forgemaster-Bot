USE [LostWorld]
GO
/****** Object:  Table [dbo].[Link_Character_Recipe]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Link_Character_Recipe](
	[Character_ID] [uniqueidentifier] NOT NULL,
	[Skill] [nvarchar](50) NOT NULL,
	[Recipe] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO
