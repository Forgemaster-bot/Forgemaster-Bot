USE [LostWorld]
GO
/****** Object:  Table [dbo].[Link_Character_Class]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Link_Character_Class](
	[Character_ID] [uniqueidentifier] NOT NULL,
	[Class] [nvarchar](50) NOT NULL,
	[Level] [int] NOT NULL,
	[Number] [int] NOT NULL,
	[Sub_Class] [nvarchar](50) NULL,
	[Free_Book_Spells] [int] NULL,
	[Replace_Spell] [bit] NULL,
	[Class_Choice] [bit] NULL
) ON [PRIMARY]
GO
