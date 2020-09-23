USE [LostWorld]
GO
/****** Object:  Table [dbo].[Link_Spell_book_Spells]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Link_Spell_book_Spells](
	[Spell_Book_ID] [uniqueidentifier] NOT NULL,
	[Spell] [nvarchar](50) NOT NULL,
	[Known] [bit] NOT NULL
) ON [PRIMARY]
GO
