USE [LostWorld]
GO
/****** Object:  Table [dbo].[Main_Wizard_Spell_Share]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Main_Wizard_Spell_Share](
	[Target_ID] [uniqueidentifier] NOT NULL,
	[Spell] [nvarchar](50) NOT NULL,
	[Owner] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO
