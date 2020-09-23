USE [LostWorld]
GO
/****** Object:  Table [dbo].[Main_Spell_Book]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Main_Spell_Book](
	[ID] [uniqueidentifier] NOT NULL,
	[Owner_ID] [uniqueidentifier] NOT NULL,
	[Name] [nvarchar](50) NOT NULL,
	[Type] [nvarchar](50) NULL
) ON [PRIMARY]
GO
